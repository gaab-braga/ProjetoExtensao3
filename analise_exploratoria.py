"""
analise_exploratoria.py — Experimentos estatísticos do Dossiê de Evidências (Grupo 1).

Entrada : data/processed/pns2019_telas_saude_mental.csv  (gerado por etl_processor.py)
Saídas  : outputs/graficos/*.png
          outputs/resultados_estatisticos.json
          outputs/resultados_estatisticos.md

Métodos
  1. Correlação de Spearman (ordinal x ordinal) e Pearson (horas aproximadas x escore), com IC 95%.
  2. Correlação parcial de Spearman controlando idade, sexo, escolaridade e renda (confundidores).
  3. Prevalências ponderadas (peso V00291) com erro-padrão por linearização de Taylor
     (estratos V0024 + UPA), i.e. respeitando o plano amostral complexo da PNS.
  4. Regressão logística ponderada (OR ajustados, EP robusto por conglomerado/UPA):
     PHQ-9 >= 10 e "dificuldade de concentração frequente" ~ tempo de tela + controles.
  5. Teste de interação tela x sexo (pergunta do ODS 5) e comparação de correlações entre sexos.
"""
from __future__ import annotations

import json
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
import statsmodels.api as sm
from matplotlib.colors import LinearSegmentedColormap
from scipy import stats

warnings.filterwarnings("ignore", category=FutureWarning)
# GLM com var_weights + EP sanduíche por UPA: estimativas pontuais = pseudo-máxima verossimilhança ponderada;
# o EP é uma aproximação ao desenho (conglomerado UPA, sem estratos -> levemente conservador).
# Para confirmação formal do desenho completo, ver survey::svyglm no R (documentado no Dossiê).
warnings.filterwarnings("ignore", message="cov_type not fully supported with var_weights")

ROOT = Path(__file__).resolve().parent
DADOS = ROOT / "data" / "processed" / "pns2019_telas_saude_mental.csv"
OUT = ROOT / "outputs"
GRAF = OUT / "graficos"

TELA_ROTULO = {0: "Não usa", 1: "<1h", 2: "1–2h", 3: "2–3h", 4: "3–6h", 5: "6h+"}
FAIXAS = ["15–17", "18–24", "25–34", "35–44", "45–59", "60+"]

# ---- paleta (validada: azul/laranja são par adjacente aprovado para daltonismo) ----
SURFACE, INK, INK2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
GRID, AXIS = "#e1e0d9", "#c3c2b7"
COR_SEXO = {"Homem": "#2a78d6", "Mulher": "#eb6834"}
AZUL, NEUTRO = "#2a78d6", "#b5b3ab"
DIVERGENTE = LinearSegmentedColormap.from_list("div", ["#184f95", "#6da7ec", "#f0efec", "#ef8a7e", "#b82d2c"])

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "font.family": "DejaVu Sans", "font.size": 10, "text.color": INK,
    "axes.labelcolor": INK2, "axes.edgecolor": AXIS, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "axes.grid.axis": "y",
    "grid.color": GRID, "grid.linewidth": 0.6, "axes.titleweight": "bold", "axes.titlesize": 11,
    "legend.frameon": False,
})


# ===========================================================================
# Utilitários estatísticos
# ===========================================================================
def classificar_efeito(r: float) -> str:
    a = abs(r)
    if a < 0.10:
        return "desprezível"
    if a < 0.30:
        return "fraca"
    if a < 0.50:
        return "moderada"
    return "forte"


def spearman_ic(x: pd.Series, y: pd.Series) -> dict:
    m = x.notna() & y.notna()
    x, y = x[m].astype(float), y[m].astype(float)
    n = len(x)
    rho, p = stats.spearmanr(x, y)
    se = np.sqrt((1 + rho**2 / 2) / (n - 3))          # Bonett & Wright (2000)
    z = np.arctanh(rho)
    lo, hi = np.tanh(z - 1.96 * se), np.tanh(z + 1.96 * se)
    return {"rho": float(rho), "ic95": [float(lo), float(hi)], "p": float(p), "n": int(n),
            "efeito": classificar_efeito(rho)}


def pearson_ic(x: pd.Series, y: pd.Series) -> dict:
    m = x.notna() & y.notna()
    res = stats.pearsonr(x[m].astype(float), y[m].astype(float))
    ci = res.confidence_interval(0.95)
    return {"r": float(res.statistic), "ic95": [float(ci.low), float(ci.high)], "p": float(res.pvalue),
            "n": int(m.sum()), "efeito": classificar_efeito(res.statistic)}


def spearman_parcial(df: pd.DataFrame, x: str, y: str, controles: list[str]) -> dict:
    """Spearman parcial: Pearson entre resíduos dos postos de x e y regredidos nos postos dos controles."""
    d = df[[x, y] + controles].dropna().astype(float).rank()
    Z = sm.add_constant(d[controles].values)
    rx = d[x].values - Z @ np.linalg.lstsq(Z, d[x].values, rcond=None)[0]
    ry = d[y].values - Z @ np.linalg.lstsq(Z, d[y].values, rcond=None)[0]
    r = float(np.corrcoef(rx, ry)[0, 1])
    n, k = len(d), len(controles)
    t = r * np.sqrt((n - 2 - k) / (1 - r**2))
    p = float(2 * stats.t.sf(abs(t), n - 2 - k))
    se = 1 / np.sqrt(n - 3 - k)
    lo, hi = np.tanh(np.arctanh(r) - 1.96 * se), np.tanh(np.arctanh(r) + 1.96 * se)
    return {"rho_parcial": r, "ic95": [float(lo), float(hi)], "p": p, "n": n, "controles": controles,
            "efeito": classificar_efeito(r)}


def spearman_ponderado(df: pd.DataFrame, x: str, y: str, w: str = "peso") -> float:
    d = df[[x, y, w]].dropna()
    rx, ry, ww = d[x].rank().values, d[y].rank().values, d[w].values
    mx, my = np.average(rx, weights=ww), np.average(ry, weights=ww)
    cov = np.average((rx - mx) * (ry - my), weights=ww)
    return float(cov / np.sqrt(np.average((rx - mx) ** 2, weights=ww) * np.average((ry - my) ** 2, weights=ww)))


def comparar_correlacoes(a: dict, b: dict) -> dict:
    za, zb = np.arctanh(a["rho"]), np.arctanh(b["rho"])
    se = np.sqrt((1 + a["rho"] ** 2 / 2) / (a["n"] - 3) + (1 + b["rho"] ** 2 / 2) / (b["n"] - 3))
    z = (za - zb) / se
    return {"z": float(z), "p": float(2 * stats.norm.sf(abs(z)))}


def media_amostral(d: pd.DataFrame, y: str) -> tuple[float, float, int]:
    """Média/proporção ponderada + EP por linearização de Taylor (estrato + UPA, PSU c/ reposição)."""
    d = d[[y, "peso", "estrato", "upa"]].dropna()
    if d.empty:
        return np.nan, np.nan, 0
    w, v = d["peso"].values, d[y].astype(float).values
    W = w.sum()
    est = (w * v).sum() / W
    z = w * (v - est) / W
    tot = pd.DataFrame({"h": d["estrato"].values, "c": d["upa"].values, "z": z}).groupby(["h", "c"])["z"].sum()
    var = 0.0
    for _, g in tot.groupby(level=0):
        nh = len(g)
        if nh > 1:
            var += nh / (nh - 1) * ((g - g.mean()) ** 2).sum()
    return float(est), float(np.sqrt(var)), len(d)


def tabela_prevalencia(df: pd.DataFrame, y: str, grupos: list[str]) -> pd.DataFrame:
    linhas = []
    for chave, g in df.groupby(grupos, observed=True):
        est, se, n = media_amostral(g, y)
        chave = chave if isinstance(chave, tuple) else (chave,)
        linhas.append({**dict(zip(grupos, chave)), "pct": 100 * est, "ic_inf": 100 * (est - 1.96 * se),
                       "ic_sup": 100 * (est + 1.96 * se), "n": n})
    return pd.DataFrame(linhas)


def logit_ponderado(df: pd.DataFrame, formula: str) -> dict:
    vars_ = [v for v in df.columns if v in formula]
    d = df[vars_ + ["peso", "upa"]].dropna().copy()
    d["w"] = d["peso"] / d["peso"].mean()
    mod = smf.glm(formula, data=d, family=sm.families.Binomial(), var_weights=d["w"]).fit(
        cov_type="cluster", cov_kwds={"groups": d["upa"].astype(int)})
    ic = mod.conf_int()
    tabela = {t: {"OR": float(np.exp(mod.params[t])), "ic95": [float(np.exp(ic.loc[t, 0])), float(np.exp(ic.loc[t, 1]))],
                  "p": float(mod.pvalues[t])} for t in mod.params.index if t != "Intercept"}
    return {"formula": formula, "n": int(mod.nobs), "coeficientes": tabela}


def ols_ponderado(df: pd.DataFrame, formula: str) -> dict:
    vars_ = [v for v in df.columns if v in formula]
    d = df[vars_ + ["peso", "upa"]].dropna().copy()
    mod = smf.wls(formula, data=d, weights=d["peso"] / d["peso"].mean()).fit(
        cov_type="cluster", cov_kwds={"groups": d["upa"].astype(int)})
    ic = mod.conf_int()
    return {"formula": formula, "n": int(mod.nobs), "r2": float(mod.rsquared),
            "coeficientes": {t: {"b": float(mod.params[t]), "ic95": [float(ic.loc[t, 0]), float(ic.loc[t, 1])],
                                 "p": float(mod.pvalues[t])} for t in mod.params.index if t != "Intercept"}}


# ===========================================================================
# Gráficos
# ===========================================================================
def _rotulos_tela(ax):
    ax.set_xticks(range(6))
    ax.set_xticklabels([TELA_ROTULO[i] for i in range(6)])
    ax.set_xlabel("Tempo livre/dia em celular, tablet ou computador para lazer (PNS P04502)")


def grafico_scatter(df: pd.DataFrame, cor: dict) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
    rng = np.random.default_rng(42)
    amostra = df.sample(min(len(df), 12_000), random_state=42)
    paineis = [("phq9_escore", "Escore PHQ-9 (0–27)", cor["tela_x_phq9"]),
               ("phq_concentracao", "Dificuldade de concentração (0 = nenhum dia … 3 = quase todos)",
                cor["tela_x_concentracao"])]
    for ax, (y, rot, c) in zip(axes, paineis):
        xj = amostra["tela_lazer_ord"] + rng.uniform(-0.28, 0.28, len(amostra))
        yj = amostra[y] + rng.uniform(-0.25, 0.25, len(amostra))
        ax.scatter(xj, yj, s=4, color=NEUTRO, alpha=0.18, linewidths=0, rasterized=True, label="Respondentes (amostra, com jitter)")
        medias = [media_amostral(df[df["tela_lazer_ord"] == k], y) for k in range(6)]
        mu = np.array([m[0] for m in medias]); se = np.array([m[1] for m in medias])
        ax.errorbar(range(6), mu, yerr=1.96 * se, color=AZUL, lw=2, marker="o", ms=8, capsize=4,
                    markeredgecolor=SURFACE, markeredgewidth=2, label="Média ponderada (IC 95%)", zorder=5)
        d = df[["tela_lazer_ord", y]].dropna().astype(float)
        b1, b0 = np.polyfit(d["tela_lazer_ord"], d[y], 1)
        xs = np.linspace(-0.3, 5.3, 50)
        ax.plot(xs, b0 + b1 * xs, color=INK2, lw=1.5, ls="--", label="Tendência linear (MQO)", zorder=4)
        ax.set_ylim(-0.5, float(np.nanpercentile(df[y], 99)) + 1)
        _rotulos_tela(ax)
        ax.set_ylabel(rot)
        ax.set_title(f"Spearman ρ = {c['rho']:.3f}  [IC95% {c['ic95'][0]:.3f}; {c['ic95'][1]:.3f}]   n = {c['n']:,}".replace(",", "."),
                     fontsize=10, loc="left", color=INK2, fontweight="normal")
    axes[0].legend(loc="upper left", fontsize=8.5)
    fig.suptitle("Tempo de tela de lazer × sintomas de saúde mental — PNS 2019 (IBGE)", x=0.01, ha="left",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(GRAF / "01_scatter_correlacao.png", dpi=160)
    plt.close(fig)


def grafico_heatmap(df: pd.DataFrame) -> pd.DataFrame:
    cols = {"tela_lazer_ord": "Tela lazer (celular/PC)", "tv_ord": "Televisão",
            "phq9_escore": "PHQ-9 (escore)", "phq_concentracao": "Concentração (N013)",
            "phq_sono": "Sono (N010)", "phq_agitacao": "Agitação (N015)",
            "phq_humor_deprimido": "Humor deprimido (N016)", "diag_depressao": "Diag. depressão",
            "diag_outro_transtorno_mental": "Diag. ansiedade/outros", "idade": "Idade",
            "sexo_feminino": "Sexo feminino", "escolaridade": "Escolaridade", "renda_faixa": "Renda per capita"}
    m = df[list(cols)].astype(float).corr(method="spearman").rename(index=cols, columns=cols)
    fig, ax = plt.subplots(figsize=(11, 9))
    mask = np.triu(np.ones_like(m, dtype=bool), k=1)
    sns.heatmap(m, mask=mask, cmap=DIVERGENTE, vmin=-0.6, vmax=0.6, center=0, annot=True, fmt=".2f",
                annot_kws={"size": 8}, linewidths=2, linecolor=SURFACE, square=True,
                cbar_kws={"label": "ρ de Spearman", "shrink": 0.7}, ax=ax)
    ax.grid(False)
    ax.tick_params(colors=INK2)
    ax.set_title("Matriz de correlações de Spearman — PNS 2019 (n = {:,})".format(len(df)).replace(",", "."),
                 loc="left", fontsize=13)
    fig.tight_layout()
    fig.savefig(GRAF / "02_heatmap_correlacoes.png", dpi=160)
    plt.close(fig)
    return m


def grafico_barras_sexo(prev_dep: pd.DataFrame, prev_conc: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), sharey=False)
    largura = 0.38
    for ax, tab, tit in [(axes[0], prev_dep, "Rastreio positivo para depressão (PHQ-9 ≥ 10)"),
                         (axes[1], prev_conc, "Dificuldade de concentração em mais da metade dos dias")]:
        for i, sexo in enumerate(["Homem", "Mulher"]):
            t = tab[tab["sexo"] == sexo].sort_values("tela_lazer_ord")
            x = t["tela_lazer_ord"].values + (i - 0.5) * (largura + 0.02)
            ax.bar(x, t["pct"], width=largura, color=COR_SEXO[sexo], label=sexo, edgecolor=SURFACE, linewidth=1)
            ax.errorbar(x, t["pct"], yerr=[t["pct"] - t["ic_inf"], t["ic_sup"] - t["pct"]], fmt="none",
                        ecolor=INK2, elinewidth=1, capsize=2.5)
        ax.set_ylim(0, tab["ic_sup"].max() * 1.22)
        ax.legend(loc="upper left", ncol=2)
        _rotulos_tela(ax)
        ax.set_ylabel("% da população (ponderado, IC 95%)")
        ax.set_title(tit, loc="left")
    fig.suptitle("Impacto demográfico: tempo de tela × saúde mental por sexo (ODS 3 e ODS 5) — PNS 2019",
                 x=0.01, ha="left", fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(GRAF / "03_barras_sexo.png", dpi=160)
    plt.close(fig)


def grafico_barras_idade(prev_uso: pd.DataFrame, prev_dep_idade: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
    t = prev_uso.set_index("faixa_etaria").loc[FAIXAS].reset_index()
    ax = axes[0]
    ax.bar(range(len(t)), t["pct"], color=AZUL, width=0.6)
    ax.errorbar(range(len(t)), t["pct"], yerr=[t["pct"] - t["ic_inf"], t["ic_sup"] - t["pct"]], fmt="none",
                ecolor=INK2, elinewidth=1, capsize=3)
    for i, v in enumerate(t["pct"]):
        ax.annotate(f"{v:.1f}%", (i, t["ic_sup"].iloc[i]), xytext=(0, 4), textcoords="offset points",
                    ha="center", fontsize=8.5, color=INK2)
    ax.set_ylim(0, t["ic_sup"].max() * 1.15)
    ax.set_xticks(range(len(t))); ax.set_xticklabels(FAIXAS); ax.set_xlabel("Faixa etária")
    ax.set_ylabel("% com 3h+ por dia de tela de lazer"); ax.set_title("Uso intenso de tela de lazer (3h+/dia)", loc="left")

    ax = axes[1]
    largura = 0.38
    for i, (grupo, cor) in enumerate([(0, NEUTRO), (1, AZUL)]):
        g = prev_dep_idade[prev_dep_idade["tela_lazer_3h_mais"] == grupo].set_index("faixa_etaria").reindex(FAIXAS)
        x = np.arange(len(FAIXAS)) + (i - 0.5) * (largura + 0.02)
        ax.bar(x, g["pct"], width=largura, color=cor, label=["Menos de 3h/dia", "3h ou mais/dia"][grupo])
        ax.errorbar(x, g["pct"], yerr=[g["pct"] - g["ic_inf"], g["ic_sup"] - g["pct"]], fmt="none",
                    ecolor=INK2, elinewidth=1, capsize=2.5)
    ax.set_xticks(range(len(FAIXAS))); ax.set_xticklabels(FAIXAS); ax.set_xlabel("Faixa etária")
    ax.set_ylabel("% com PHQ-9 ≥ 10 (ponderado, IC 95%)")
    ax.set_title("Rastreio de depressão por idade e tempo de tela", loc="left")
    ax.set_ylim(0, prev_dep_idade["ic_sup"].max() * 1.22)
    ax.legend(loc="upper left", ncol=2)
    fig.suptitle("Impacto demográfico por idade — PNS 2019 (IBGE)", x=0.01, ha="left", fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(GRAF / "04_barras_idade.png", dpi=160)
    plt.close(fig)


def grafico_dose_resposta(modelos: dict) -> None:
    """OR ajustado por faixa de tela (ref. <1h) — evidencia a curva em J que a correlação linear não capta."""
    ordem = ["Não usa", "<1h", "1–2h", "2–3h", "3–6h", "6h+"]
    series = [("PHQ-9>=10 ~ faixas de tela (ref. <1h)", "Rastreio de depressão (PHQ-9 ≥ 10)", AZUL, "o"),
              ("Concentração frequente ~ faixas de tela (ref. <1h)", "Dificuldade de concentração frequente", "#eb6834", "s")]
    fig, ax = plt.subplots(figsize=(11, 5.4))
    ax.axhline(1, color=AXIS, lw=1.2, zorder=1)
    for i, (chave, rotulo, cor, marc) in enumerate(series):
        coefs = modelos[chave]["coeficientes"]
        ors, lo, hi = [], [], []
        for cat in ordem:
            if cat == "<1h":
                ors.append(1.0); lo.append(1.0); hi.append(1.0)
            else:
                c = coefs[f"tela_cat[T.{cat}]"]
                ors.append(c["OR"]); lo.append(c["ic95"][0]); hi.append(c["ic95"][1])
        x = np.arange(6) + (i - 0.5) * 0.18
        ors, lo, hi = map(np.array, (ors, lo, hi))
        ax.errorbar(x, ors, yerr=[ors - lo, hi - ors], fmt=marc, color=cor, ms=9, lw=2, capsize=4,
                    markeredgecolor=SURFACE, markeredgewidth=2, label=rotulo, zorder=3)
        ax.plot(x[1:], ors[1:], color=cor, lw=1.2, alpha=0.6, zorder=2)
        ax.annotate(f"OR {ors[-1]:.2f}", (x[-1], hi[-1]), xytext=(0, 6), textcoords="offset points",
                    ha="center", fontsize=9, color=INK2)
    ax.set_xticks(range(6)); ax.set_xticklabels(ordem)
    ax.set_xlabel("Tempo livre/dia em celular, tablet ou computador para lazer (PNS P04502)")
    ax.set_ylabel("Odds ratio ajustado (IC 95%) — ref. < 1h/dia")
    ax.set_title("Ajustado por sexo, idade, escolaridade, renda, TV e zona rural; pesos amostrais da PNS",
                 loc="left", fontsize=10, color=INK2, fontweight="normal")
    ax.legend(loc="upper left")
    fig.suptitle("Dose-resposta: o risco sobe a partir de 3h/dia e é máximo em 6h+ — PNS 2019 (IBGE)",
                 x=0.01, ha="left", fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(GRAF / "05_dose_resposta_OR.png", dpi=160)
    plt.close(fig)


# ===========================================================================
# Relatório
# ===========================================================================
def fmt_p(p: float) -> str:
    return "< 0,001" if p < 0.001 else f"{p:.3f}".replace(".", ",")


def escrever_markdown(res: dict) -> None:
    L = ["# Resultados estatísticos (gerado automaticamente por `analise_exploratoria.py`)", "",
         f"Base: PNS 2019 — {res['n_total']:,} adultos (15+) com tempo de tela e PHQ-9 completos.".replace(",", "."), "",
         "## 1. Correlações bivariadas (Spearman)", "",
         "| Tecnologia | Desfecho | ρ | IC 95% | p | n | Força |", "|---|---|---:|---|---:|---:|---|"]
    for k, c in res["correlacoes_spearman"].items():
        x, y = k.split("_x_")
        L.append(f"| {x} | {y} | {c['rho']:.3f} | [{c['ic95'][0]:.3f}; {c['ic95'][1]:.3f}] | {fmt_p(c['p'])} | {c['n']:,} | {c['efeito']} |")
    p = res["pearson_horas_x_phq9"]
    L += ["", f"Pearson (horas aproximadas × escore PHQ-9): r = {p['r']:.3f} [IC95% {p['ic95'][0]:.3f}; {p['ic95'][1]:.3f}], p {fmt_p(p['p'])}.",
          "", "## 2. Correlação parcial (controle: idade, sexo, escolaridade, renda)", "",
          "| Par | ρ parcial | IC 95% | p | Força |", "|---|---:|---|---:|---|"]
    for k, c in res["correlacoes_parciais"].items():
        L.append(f"| {k} | {c['rho_parcial']:.3f} | [{c['ic95'][0]:.3f}; {c['ic95'][1]:.3f}] | {fmt_p(c['p'])} | {c['efeito']} |")
    L += ["", "## 3. Correlação por subgrupo (tela × PHQ-9)", "", "| Grupo | ρ | IC 95% | n |", "|---|---:|---|---:|"]
    for k, c in res["spearman_por_grupo"].items():
        L.append(f"| {k} | {c['rho']:.3f} | [{c['ic95'][0]:.3f}; {c['ic95'][1]:.3f}] | {c['n']:,} |")
    cmp_ = res["comparacao_sexos"]
    L += ["", f"Diferença Homem vs Mulher: z = {cmp_['z']:.2f}, p {fmt_p(cmp_['p'])}.", "",
          "## 4. Regressão logística ponderada (OR ajustado; EP robusto por UPA)", ""]
    for nome, mod in res["regressoes_logisticas"].items():
        L += [f"**{nome}** — `{mod['formula']}` (n = {mod['n']:,})", "", "| Termo | OR | IC 95% | p |", "|---|---:|---|---:|"]
        for t, c in mod["coeficientes"].items():
            L.append(f"| {t} | {c['OR']:.2f} | [{c['ic95'][0]:.2f}; {c['ic95'][1]:.2f}] | {fmt_p(c['p'])} |")
        L.append("")
    L += ["## 4b. Sensibilidade — apenas usuários de tela (exclui 'não usa')", "",
          "| Recorte | ρ | IC 95% | p | n |", "|---|---:|---|---:|---:|"]
    for k, c in res["sensibilidade_apenas_usuarios"].items():
        rho = c.get("rho", c.get("rho_parcial"))
        L.append(f"| {k} | {rho:.3f} | [{c['ic95'][0]:.3f}; {c['ic95'][1]:.3f}] | {fmt_p(c['p'])} | {c['n']:,} |")
    L += ["", "## 4c. Perfil por faixa de tela", "", pd.DataFrame(res["perfil_por_faixa_de_tela"]).to_markdown(index=False), ""]
    L += ["## 5. Prevalências ponderadas", ""]
    for nome, tab in res["prevalencias"].items():
        L += [f"**{nome}**", "", pd.DataFrame(tab).round(2).to_markdown(index=False), ""]
    (OUT / "resultados_estatisticos.md").write_text("\n".join(L))


# ===========================================================================
def main() -> None:
    GRAF.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DADOS)
    print(f"[INFO] {len(df):,} registros carregados de {DADOS.name}")
    res: dict = {"n_total": int(len(df))}

    # --- 1. Correlações bivariadas ---------------------------------------
    desfechos = {"phq9": "phq9_escore", "concentracao": "phq_concentracao", "sono": "phq_sono",
                 "agitacao": "phq_agitacao", "humor_deprimido": "phq_humor_deprimido",
                 "diag_depressao": "diag_depressao", "diag_ansiedade_outros": "diag_outro_transtorno_mental"}
    cor = {}
    for tec, col_tec in [("tela", "tela_lazer_ord"), ("tv", "tv_ord")]:
        for nome, col in desfechos.items():
            c = spearman_ic(df[col_tec], df[col])
            c["rho_ponderado"] = spearman_ponderado(df, col_tec, col)
            cor[f"{tec}_x_{nome}"] = c
    res["correlacoes_spearman"] = cor
    res["pearson_horas_x_phq9"] = pearson_ic(df["tela_lazer_horas"], df["phq9_escore"])
    res["pearson_horas_x_concentracao"] = pearson_ic(df["tela_lazer_horas"], df["phq_concentracao"])

    controles = ["idade", "sexo_feminino", "escolaridade", "renda_faixa"]
    res["correlacoes_parciais"] = {
        f"tela_x_{n}": spearman_parcial(df, "tela_lazer_ord", desfechos[n], controles)
        for n in ["phq9", "concentracao", "sono", "agitacao"]}

    # --- 2. Subgrupos (ODS 5 / idade) ---------------------------------------
    grp = {}
    for sexo in ["Homem", "Mulher"]:
        grp[f"sexo={sexo}"] = spearman_ic(df.loc[df.sexo == sexo, "tela_lazer_ord"], df.loc[df.sexo == sexo, "phq9_escore"])
    for f in FAIXAS:
        s = df[df.faixa_etaria == f]
        grp[f"idade={f}"] = spearman_ic(s["tela_lazer_ord"], s["phq9_escore"])
    res["spearman_por_grupo"] = grp
    res["comparacao_sexos"] = comparar_correlacoes(grp["sexo=Homem"], grp["sexo=Mulher"])

    # --- 3. Prevalências ponderadas ----------------------------------------
    prev_dep = tabela_prevalencia(df, "phq9_depressao", ["sexo", "tela_lazer_ord"])
    prev_conc = tabela_prevalencia(df, "concentracao_frequente", ["sexo", "tela_lazer_ord"])
    prev_uso = tabela_prevalencia(df, "tela_lazer_3h_mais", ["faixa_etaria"])
    prev_uso_sexo = tabela_prevalencia(df, "tela_lazer_3h_mais", ["sexo"])
    prev_dep_idade = tabela_prevalencia(df, "phq9_depressao", ["faixa_etaria", "tela_lazer_3h_mais"])
    prev_dep_sexo = tabela_prevalencia(df, "phq9_depressao", ["sexo"])
    prev_geral = {y: media_amostral(df, y) for y in ["phq9_depressao", "concentracao_frequente", "tela_lazer_3h_mais"]}
    res["prevalencias"] = {
        "PHQ-9>=10 por sexo e tela": prev_dep.to_dict("records"),
        "Concentracao frequente por sexo e tela": prev_conc.to_dict("records"),
        "Uso 3h+ por faixa etaria": prev_uso.to_dict("records"),
        "Uso 3h+ por sexo": prev_uso_sexo.to_dict("records"),
        "PHQ-9>=10 por faixa etaria e uso 3h+": prev_dep_idade.to_dict("records"),
        "PHQ-9>=10 por sexo": prev_dep_sexo.to_dict("records"),
        "Geral": [{"indicador": k, "pct": 100 * v[0], "ic_inf": 100 * (v[0] - 1.96 * v[1]),
                   "ic_sup": 100 * (v[0] + 1.96 * v[1]), "n": v[2]} for k, v in prev_geral.items()],
    }

    # --- 4. Regressões ajustadas -------------------------------------------
    df["tela_cat"] = pd.Categorical(df["tela_lazer_ord"].map(TELA_ROTULO), categories=[TELA_ROTULO[i] for i in [1, 0, 2, 3, 4, 5]])
    ctrl = "sexo_feminino + C(faixa_etaria) + escolaridade + C(renda_faixa) + tv_ord + zona_rural"
    res["regressoes_logisticas"] = {
        "PHQ-9>=10 ~ faixas de tela (ref. <1h)": logit_ponderado(df, f"phq9_depressao ~ tela_cat + {ctrl}"),
        "PHQ-9>=10 ~ tendência ordinal de tela": logit_ponderado(df, f"phq9_depressao ~ tela_lazer_ord + {ctrl}"),
        "Concentração frequente ~ faixas de tela (ref. <1h)": logit_ponderado(df, f"concentracao_frequente ~ tela_cat + {ctrl}"),
        "Interação ODS 5: PHQ-9>=10 ~ tela 3h+ × sexo": logit_ponderado(
            df, "phq9_depressao ~ tela_lazer_3h_mais * sexo_feminino + C(faixa_etaria) + escolaridade + C(renda_faixa) + tv_ord + zona_rural"),
        "Interação idade: PHQ-9>=10 ~ tela 3h+ × jovem (15-24)": logit_ponderado(
            df.assign(jovem=df["faixa_etaria"].isin(["15–17", "18–24"]).astype(int)),
            "phq9_depressao ~ tela_lazer_3h_mais * jovem + sexo_feminino + escolaridade + C(renda_faixa) + tv_ord + zona_rural"),
    }
    res["regressoes_logisticas"]["Diag. ansiedade/outros (Q11006) ~ faixas de tela (ref. <1h)"] = logit_ponderado(
        df, f"diag_outro_transtorno_mental ~ tela_cat + {ctrl}")
    # Jovens: poucos usam <1h (referência instável) -> tendência ordinal entre usuários, por faixa etária
    for rot, faixas in [("15-24", ["15–17", "18–24"]), ("25-44", ["25–34", "35–44"]), ("45+", ["45–59", "60+"])]:
        sub = df[df["faixa_etaria"].isin(faixas) & (df["tela_lazer_ord"] >= 1)]
        res["regressoes_logisticas"][f"Usuários {rot} anos: PHQ-9>=10 ~ tendência por faixa de tela"] = logit_ponderado(
            sub, "phq9_depressao ~ tela_lazer_ord + sexo_feminino + idade + escolaridade + C(renda_faixa) + tv_ord + zona_rural")
    res["regressao_linear_phq9"] = ols_ponderado(df, f"phq9_escore ~ tela_lazer_ord + {ctrl}")

    # --- 4b. Sensibilidade: apenas usuários (exclui "não usa", grupo de perfil distinto) ----
    usuarios = df[df["tela_lazer_ord"] >= 1]
    sens = {"todas_idades": spearman_ic(usuarios["tela_lazer_ord"], usuarios["phq9_escore"]),
            "parcial_todas_idades": spearman_parcial(usuarios, "tela_lazer_ord", "phq9_escore", controles),
            "concentracao_todas_idades": spearman_ic(usuarios["tela_lazer_ord"], usuarios["phq_concentracao"])}
    for f in FAIXAS:
        s = usuarios[usuarios.faixa_etaria == f]
        sens[f"idade={f}"] = spearman_ic(s["tela_lazer_ord"], s["phq9_escore"])
    res["sensibilidade_apenas_usuarios"] = sens

    # --- 4c. Perfil de cada faixa de tela (explica o confundimento do grupo "não usa") ----
    perfil = []
    for k in range(6):
        g = df[df["tela_lazer_ord"] == k]
        perfil.append({"tela": TELA_ROTULO[k], "n": len(g),
                       "idade_media": round(float(np.average(g["idade"], weights=g["peso"])), 1),
                       "pct_60_mais": round(100 * media_amostral(g.assign(v=(g["idade"] >= 60).astype(int)), "v")[0], 1),
                       "pct_ate_1SM": round(100 * media_amostral(g.assign(v=(g["renda_faixa"] <= 3).astype(float).where(g["renda_faixa"].notna())), "v")[0], 1),
                       "pct_mulheres": round(100 * media_amostral(g, "sexo_feminino")[0], 1)})
    res["perfil_por_faixa_de_tela"] = perfil

    # --- 5. Gráficos --------------------------------------------------------
    grafico_scatter(df, {"tela_x_phq9": cor["tela_x_phq9"], "tela_x_concentracao": cor["tela_x_concentracao"]})
    res["matriz_spearman"] = grafico_heatmap(df).round(4).to_dict()
    grafico_barras_sexo(prev_dep, prev_conc)
    grafico_barras_idade(prev_uso, prev_dep_idade)
    grafico_dose_resposta(res["regressoes_logisticas"])

    (OUT / "resultados_estatisticos.json").write_text(json.dumps(res, ensure_ascii=False, indent=2, default=float))
    escrever_markdown(res)

    # --- resumo no terminal -------------------------------------------------
    print("\n=== CORRELAÇÕES (Spearman) ===")
    for k, c in cor.items():
        print(f"{k:<32} ρ={c['rho']:+.3f} [{c['ic95'][0]:+.3f};{c['ic95'][1]:+.3f}] p={c['p']:.2g} ({c['efeito']})")
    print("\n=== PARCIAIS (controle idade/sexo/escolaridade/renda) ===")
    for k, c in res["correlacoes_parciais"].items():
        print(f"{k:<32} ρ={c['rho_parcial']:+.3f} p={c['p']:.2g} ({c['efeito']})")
    print(f"\nHomem vs Mulher (tela×PHQ-9): {res['comparacao_sexos']}")
    print(f"[OK] Gráficos em {GRAF}; tabelas em {OUT}/resultados_estatisticos.(md|json)")


if __name__ == "__main__":
    main()
