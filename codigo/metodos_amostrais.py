"""
metodos_amostrais.py — Inferência baseada no desenho amostral complexo da PNS 2019.

A PNS é uma amostra por conglomerados em múltiplos estágios, estratificada (V0024 = estrato,
UPA_PNS = unidade primária de amostragem), com pesos calibrados (V00291). Ignorar esse desenho
subestima os erros-padrão. Este módulo implementa, sem dependências além de numpy/pandas/statsmodels/patsy:

  media_amostral   média/proporção ponderada + EP por linearização de Taylor
  svyglm           GLM (Poisson-log -> razão de prevalência; Gauss-identidade -> diferença de prevalências)
                   com variância sanduíche linearizada por estrato + UPA ("with replacement", como
                   survey::svyglm no R) e estimação por DOMÍNIO (subpopulação)
  wald             teste de Wald conjunto
  reri             interação aditiva (Relative Excess Risk due to Interaction) com IC pelo método delta
  e_value          robustez a confundimento não medido (VanderWeele & Ding, 2017)
  fap              fração atribuível populacional (Miettinen) — supõe causalidade, uso hipotético

Estimação por domínio: as observações fora do subgrupo recebem peso 0 mas suas UPAs continuam
contando na variância (recortar a base antes de estimar distorce o EP). Estratos com uma única UPA
no arquivo não contribuem para a variância e são reportados.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
import patsy
from scipy import stats

Z95 = stats.norm.ppf(0.975)


# ---------------------------------------------------------------------------
# Núcleo: variância linearizada a partir de escores individuais
# ---------------------------------------------------------------------------
def _meat(escores: np.ndarray, estrato: np.ndarray, upa: np.ndarray) -> tuple[np.ndarray, int]:
    """Σ_h n_h/(n_h-1) Σ_c (U_hc - Ū_h)(U_hc - Ū_h)'  — totais por UPA dentro do estrato."""
    p = escores.shape[1]
    tot = (pd.DataFrame(escores).assign(_h=estrato, _c=upa)
           .groupby(["_h", "_c"], sort=False).sum())
    h = tot.index.get_level_values(0)
    n_h = tot.groupby(level=0)[tot.columns[0]].transform("size").to_numpy()
    media_h = tot.groupby(level=0).transform("mean").to_numpy()
    dev = tot.to_numpy() - media_h
    validos = n_h > 1
    fator = np.sqrt(n_h[validos] / (n_h[validos] - 1))[:, None]
    D = dev[validos] * fator
    estratos_uma_upa = int((pd.Series(n_h, index=h).groupby(level=0).first() == 1).sum())
    return (D.T @ D) if p else np.zeros((0, 0)), estratos_uma_upa


def media_amostral(df: pd.DataFrame, y: str, dominio: pd.Series | None = None,
                   peso: str = "peso", estrato: str = "estrato", upa: str = "upa") -> tuple[float, float, int]:
    """Média/proporção ponderada no domínio + EP linearizado (desenho completo). Retorna (est, ep, n)."""
    em = df[y].notna() & df[peso].notna()
    if dominio is not None:
        em &= dominio.fillna(False).astype(bool)
    if not em.any():
        return np.nan, np.nan, 0
    w = df[peso].to_numpy(float) * em.to_numpy()
    v = df[y].fillna(0).to_numpy(float)
    W = w.sum()
    est = (w * v).sum() / W
    z = (w * (v - est) / W)[:, None]
    M, _ = _meat(z, df[estrato].to_numpy(), df[upa].to_numpy())
    return float(est), float(np.sqrt(M[0, 0])), int(em.sum())


@dataclass
class AjusteAmostral:
    formula: str
    familia: str
    nomes: list[str]
    b: np.ndarray
    V: np.ndarray
    n: int
    n_upas: int
    estratos_uma_upa: int
    notas: list[str] = field(default_factory=list)

    @property
    def ep(self) -> np.ndarray:
        return np.sqrt(np.diag(self.V))

    def idx(self, termo: str) -> int:
        return self.nomes.index(termo)

    def coef(self, termo: str) -> dict:
        """Para Poisson-log devolve RP (exp); para Gauss-identidade devolve diferença em p.p. (x100)."""
        i = self.idx(termo)
        b, se = self.b[i], self.ep[i]
        p = float(2 * stats.norm.sf(abs(b / se)))
        if self.familia == "poisson-log":
            return {"RP": float(np.exp(b)), "ic95": [float(np.exp(b - Z95 * se)), float(np.exp(b + Z95 * se))], "p": p}
        return {"dif_pp": float(100 * b), "ic95": [float(100 * (b - Z95 * se)), float(100 * (b + Z95 * se))], "p": p}

    def tabela(self) -> dict:
        return {t: self.coef(t) for t in self.nomes if t != "Intercept"}


def svyglm(df: pd.DataFrame, formula: str, familia: str = "poisson-log", dominio: pd.Series | None = None,
           peso: str = "peso", estrato: str = "estrato", upa: str = "upa", ponderar: bool = True,
           max_iter: int = 100, tol: float = 1e-10) -> AjusteAmostral:
    """GLM ponderado com variância de Taylor (estrato + UPA) e estimação por domínio.

    familia: "poisson-log" (Poisson robusto -> razão de prevalência; Barros & Hirakata, 2003)
             "gauss-identidade" (modelo linear -> diferença de prevalências / interação aditiva)
    ponderar=False usa peso 1 (mantém o desenho de conglomerados) — usado só na specification curve.
    """
    em = pd.Series(True, index=df.index) if dominio is None else dominio.reindex(df.index).fillna(False).astype(bool)
    y_df, X_df = patsy.dmatrices(formula, df[em], return_type="dataframe", NA_action="drop")
    linhas = X_df.index
    y = y_df.iloc[:, 0].to_numpy(float)
    X = X_df.to_numpy(float)
    w = df.loc[linhas, peso].to_numpy(float) if ponderar else np.ones(len(linhas))
    w = w / w.mean()                                   # escala não altera estimativas nem EP linearizado

    # IRLS
    if familia == "poisson-log":
        b = np.zeros(X.shape[1]); b[0] = np.log(max(np.average(y, weights=w), 1e-12))
        for _ in range(max_iter):
            eta = X @ b
            mu = np.exp(eta)
            z = eta + (y - mu) / mu
            Wd = w * mu
            b_novo = np.linalg.solve(X.T @ (X * Wd[:, None]), X.T @ (Wd * z))
            if np.max(np.abs(b_novo - b)) < tol:
                b = b_novo
                break
            b = b_novo
        mu = np.exp(X @ b)
        bread = np.linalg.inv(X.T @ (X * (w * mu)[:, None]))
    elif familia == "gauss-identidade":
        b = np.linalg.solve(X.T @ (X * w[:, None]), X.T @ (w * y))
        mu = X @ b
        bread = np.linalg.inv(X.T @ (X * w[:, None]))
    else:
        raise ValueError(familia)

    # Escores no arquivo inteiro: zero fora do domínio, mas UPA/estrato preservados.
    U = np.zeros((len(df), X.shape[1]))
    pos = df.index.get_indexer(linhas)
    U[pos] = X * (w * (y - mu))[:, None]
    M, uma_upa = _meat(U, df[estrato].to_numpy(), df[upa].to_numpy())
    V = bread @ M @ bread
    return AjusteAmostral(formula=formula, familia=familia, nomes=list(X_df.columns), b=b, V=V,
                          n=len(linhas), n_upas=int(df.loc[linhas, upa].nunique()), estratos_uma_upa=uma_upa)


# ---------------------------------------------------------------------------
# Testes e medidas derivadas
# ---------------------------------------------------------------------------
def wald(ajuste: AjusteAmostral, termos: list[str]) -> dict:
    i = [ajuste.idx(t) for t in termos]
    b, V = ajuste.b[i], ajuste.V[np.ix_(i, i)]
    chi2 = float(b @ np.linalg.solve(V, b))
    return {"chi2": chi2, "gl": len(i), "p": float(stats.chi2.sf(chi2, len(i))), "termos": termos}


def combinacao(ajuste: AjusteAmostral, pesos: dict[str, float]) -> dict:
    """Combinação linear de coeficientes (ex.: efeito da exposição no estrato 'mulher' = b_E + b_E:mulher)."""
    i = [ajuste.idx(t) for t in pesos]
    g = np.array(list(pesos.values()), dtype=float)
    est = float(g @ ajuste.b[i])
    se = float(np.sqrt(g @ ajuste.V[np.ix_(i, i)] @ g))
    p = float(2 * stats.norm.sf(abs(est / se)))
    if ajuste.familia == "poisson-log":
        return {"RP": float(np.exp(est)), "ic95": [float(np.exp(est - Z95 * se)), float(np.exp(est + Z95 * se))], "p": p}
    return {"dif_pp": 100 * est, "ic95": [100 * (est - Z95 * se), 100 * (est + Z95 * se)], "p": p}


def reri(ajuste: AjusteAmostral, a: str, b_: str, ab: str) -> dict:
    """RERI = RP11 − RP10 − RP01 + 1 (escala aditiva). IC pelo método delta. Requer Poisson-log."""
    i = [ajuste.idx(t) for t in (a, b_, ab)]
    b1, b2, b3 = ajuste.b[i]
    rr10, rr01, rr11 = np.exp(b1), np.exp(b2), np.exp(b1 + b2 + b3)
    valor = rr11 - rr10 - rr01 + 1
    g = np.array([rr11 - rr10, rr11 - rr01, rr11])
    se = float(np.sqrt(g @ ajuste.V[np.ix_(i, i)] @ g))
    return {"RERI": float(valor), "ic95": [float(valor - Z95 * se), float(valor + Z95 * se)],
            "p": float(2 * stats.norm.sf(abs(valor / se))), "RP10": float(rr10), "RP01": float(rr01), "RP11": float(rr11)}


def e_value(rp: float, limite_ic: float | None = None) -> dict:
    """E-value (VanderWeele & Ding, 2017): força mínima (em RP) que um confundidor não medido precisaria ter,
    com exposição E desfecho, para anular a associação. Para desfecho comum (>15%) é conservador."""
    def ev(r: float) -> float:
        r = 1 / r if r < 1 else r
        return float(r + np.sqrt(r * (r - 1)))
    out = {"estimativa": ev(rp)}
    if limite_ic is not None:
        out["limite_ic"] = 1.0 if (rp >= 1 and limite_ic <= 1) or (rp < 1 and limite_ic >= 1) else ev(limite_ic)
    return out


def fap(prop_casos_expostos: dict[str, float], rp: dict[str, float]) -> float:
    """Fração atribuível populacional (Miettinen): Σ pc_k (RP_k − 1)/RP_k.
    HIPOTÉTICA: só tem interpretação de 'casos evitáveis' se a associação for causal."""
    return float(sum(prop_casos_expostos[k] * (rp[k] - 1) / rp[k] for k in rp))
