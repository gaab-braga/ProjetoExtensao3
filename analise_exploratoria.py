"""
analise_exploratoria.py — Análise estatística do Dossiê de Evidências (Grupo 1).

Entrada : data/processed/pns2019_telas_saude_mental.csv  (gerado por etl_processor.py)
Saídas  : outputs/graficos/01..06_*.png
          outputs/resultados_estatisticos.json / .md

PLANO DE ANÁLISE (hierarquia declarada — ver docs/04_Rigor_Metodologico.md)
  Exposição primária : P04502 (tempo livre/dia em celular, tablet ou computador para lazer), 6 categorias.
  Desfecho primário  : rastreio positivo para depressão, PHQ-9 >= 10.
  Hipótese primária  : H1 — entre usuários, mais tempo de tela associa-se a maior prevalência do desfecho
                       primário (tendência dose-resposta), após ajuste por confundidores.
  Secundários        : dificuldade de concentração frequente (N013 >= "mais da metade dos dias");
                       diagnóstico autorreferido de ansiedade/outros transtornos (Q11006);
                       interações tela x sexo e tela x idade (escalas multiplicativa e aditiva).
                       -> correção de multiplicidade por Benjamini-Hochberg (FDR).
  Exploratório       : limiar de 3h/dia (surgiu da inspeção dos dados; não é hipótese a priori).
  Sensibilidade      : PHQ-9 por algoritmo; modelo estendido (estado civil, ocupação, região);
                       E-value; specification curve (144 especificações).

MÉTODOS
  - Razão de prevalência (RP) por regressão de Poisson com variância robusta (Barros & Hirakata, 2003),
    porque o desfecho é comum (~11%) e o OR o superestimaria.
  - Toda inferência respeita o desenho complexo (estrato + UPA + peso), com estimação por domínio
    (metodos_amostrais.py; validado em tests/).
  - Correlações de Spearman/Pearson ficam como DESCRITIVAS.
"""
from __future__ import annotations

import json
import warnings
from itertools import product
from pathlib import Path

import matplotlib
import matplotlib.ticker

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from matplotlib.colors import LinearSegmentedColormap
from scipy import stats
from statsmodels.stats.multitest import multipletests

from metodos_amostrais import combinacao, e_value, fap, media_amostral, reri, svyglm, wald

warnings.filterwarnings("ignore", category=FutureWarning)

ROOT = Path(__file__).resolve().parent
DADOS = ROOT / "data" / "processed" / "pns2019_telas_saude_mental.csv"
OUT = ROOT / "outputs"
GRAF = OUT / "graficos"

TELA_ROTULO = {0: "Não usa", 1: "<1h", 2: "1–2h", 3: "2–3h", 4: "3–6h", 5: "6h+"}
ORDEM_TELA = ["Não usa", "<1h", "1–2h", "2–3h", "3–6h", "6h+"]
FAIXAS = ["15–17", "18–24", "25–34", "35–44", "45–59", "60+"]

CTRL_MIN = "sexo_feminino + C(faixa_etaria)"
CTRL = "sexo_feminino + C(faixa_etaria) + escolaridade + C(renda_faixa) + tv_ord + zona_rural"
CTRL_EXT = CTRL + " + C(estado_civil) + C(ocupacao) + C(regiao)"
CTRL_SEM_IDADE = "sexo_feminino + escolaridade + C(renda_faixa) + tv_ord + zona_rural + idade"
CTRL_SEM_SEXO = "C(faixa_etaria) + escolaridade + C(renda_faixa) + tv_ord + zona_rural"

DESFECHOS = {"phq9_depressao": "Rastreio de depressão (PHQ-9 ≥ 10)",
             "concentracao_frequente": "Dificuldade de concentração frequente (N013)",
             "diag_outro_transtorno_mental": "Diagnóstico de ansiedade/outros transtornos (Q11006)"}

# ---- paleta (validada: slots 1–3 passam todos os pares para daltonismo) ----
SURFACE, INK, INK2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
GRID, AXIS = "#e1e0d9", "#c3c2b7"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a"]
COR_SEXO = {"Homem": SERIES[0], "Mulher": SERIES[1]}
AZUL, NEUTRO = SERIES[0], "#b5b3ab"
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
# Estatística descritiva (correlações)
# ===========================================================================
def classificar_efeito(r: float) -> str:
    a = abs(r)
    return "desprezível" if a < 0.10 else "fraca" if a < 0.30 else "moderada" if a < 0.50 else "forte"


def spearman_ic(x: pd.Series, y: pd.Series) -> dict:
    m = x.notna() & y.notna()
    x, y = x[m].astype(float), y[m].astype(float)
    n = len(x)
    rho, p = stats.spearmanr(x, y)
    se = np.sqrt((1 + rho**2 / 2) / (n - 3))          # Bonett & Wright (2000)
    z = np.arctanh(rho)
    return {"rho": float(rho), "ic95": [float(np.tanh(z - 1.96 * se)), float(np.tanh(z + 1.96 * se))],
            "p": float(p), "n": int(n), "efeito": classificar_efeito(rho)}


def spearman_parcial(df: pd.DataFrame, x: str, y: str, controles: list[str]) -> dict:
    d = df[[x, y] + controles].dropna().astype(float).rank()
    Z = sm.add_constant(d[controles].values)
    rx = d[x].values - Z @ np.linalg.lstsq(Z, d[x].values, rcond=None)[0]
    ry = d[y].values - Z @ np.linalg.lstsq(Z, d[y].values, rcond=None)[0]
    r = float(np.corrcoef(rx, ry)[0, 1])
    n, k = len(d), len(controles)
    p = float(2 * stats.t.sf(abs(r * np.sqrt((n - 2 - k) / (1 - r**2))), n - 2 - k))
    se = 1 / np.sqrt(n - 3 - k)
    return {"rho_parcial": r, "ic95": [float(np.tanh(np.arctanh(r) - 1.96 * se)), float(np.tanh(np.arctanh(r) + 1.96 * se))],
            "p": p, "n": n, "controles": controles, "efeito": classificar_efeito(r)}


def tabela_prevalencia(df: pd.DataFrame, y: str, grupos: list[str]) -> pd.DataFrame:
    linhas = []
    for chave, _ in df.groupby(grupos, observed=True):
        chave = chave if isinstance(chave, tuple) else (chave,)
        dom = np.logical_and.reduce([df[g] == v for g, v in zip(grupos, chave)])
        est, se, n = media_amostral(df, y, dominio=pd.Series(dom, index=df.index))
        linhas.append({**dict(zip(grupos, chave)), "pct": 100 * est, "ic_inf": 100 * (est - 1.96 * se),
                       "ic_sup": 100 * (est + 1.96 * se), "n": n})
    return pd.DataFrame(linhas)


def tela_coefs(aj) -> dict:
    return {c: aj.coef(f"tela_cat[T.{c}]") for c in ORDEM_TELA if c != "<1h"}


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
               ("phq_concentracao", "Dificuldade de concentração (0 = nenhum dia … 3 = quase todos)", cor["tela_x_concentracao"])]
    for ax, (y, rot, c) in zip(axes, paineis):
        xj = amostra["tela_lazer_ord"] + rng.uniform(-0.28, 0.28, len(amostra))
        yj = amostra[y] + rng.uniform(-0.25, 0.25, len(amostra))
        ax.scatter(xj, yj, s=4, color=NEUTRO, alpha=0.18, linewidths=0, rasterized=True, label="Respondentes (amostra, com jitter)")
        medias = [media_amostral(df, y, dominio=df["tela_lazer_ord"] == k) for k in range(6)]
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
    fig.suptitle("Correlação descritiva: tempo de tela de lazer × sintomas — PNS 2019 (IBGE)", x=0.01, ha="left",
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
    ax.set_title("Matriz de correlações de Spearman — PNS 2019 (n = {:,})".format(len(df)).replace(",", "."), loc="left", fontsize=13)
    fig.tight_layout()
    fig.savefig(GRAF / "02_heatmap_correlacoes.png", dpi=160)
    plt.close(fig)
    return m


def grafico_barras_sexo(prev_dep: pd.DataFrame, prev_conc: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
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
    fig, ax = plt.subplots(figsize=(11.5, 5.6))
    ax.axhline(1, color=AXIS, lw=1.2, zorder=1)
    marcadores = ["o", "s", "D"]
    for i, (y, rotulo) in enumerate(DESFECHOS.items()):
        coefs = modelos[y]["RP_por_faixa"]
        rp = np.array([1.0 if c == "<1h" else coefs[c]["RP"] for c in ORDEM_TELA])
        lo = np.array([1.0 if c == "<1h" else coefs[c]["ic95"][0] for c in ORDEM_TELA])
        hi = np.array([1.0 if c == "<1h" else coefs[c]["ic95"][1] for c in ORDEM_TELA])
        x = np.arange(6) + (i - 1) * 0.2
        ax.errorbar(x, rp, yerr=[rp - lo, hi - rp], fmt=marcadores[i], color=SERIES[i], ms=8, lw=2, capsize=3.5,
                    markeredgecolor=SURFACE, markeredgewidth=1.5, label=rotulo, zorder=3)
        ax.plot(x[1:], rp[1:], color=SERIES[i], lw=1.1, alpha=0.55, zorder=2)
    ax.set_xticks(range(6)); ax.set_xticklabels(ORDEM_TELA)
    ax.set_xlabel("Tempo livre/dia em celular, tablet ou computador para lazer (PNS P04502)")
    ax.set_ylabel("Razão de prevalência ajustada (IC 95%) — ref. < 1h/dia")
    ax.set_title("Poisson com variância pelo desenho amostral (estrato + UPA + peso); ajuste por sexo, idade, escolaridade, "
                 "renda, TV e zona rural", loc="left", fontsize=9.5, color=INK2, fontweight="normal")
    ax.legend(loc="upper left", fontsize=9)
    fig.suptitle("Dose-resposta: prevalências estáveis até 3h/dia e mais altas acima disso — PNS 2019",
                 x=0.01, ha="left", fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(GRAF / "05_dose_resposta_RP.png", dpi=160)
    plt.close(fig)


def grafico_spec_curve(specs: pd.DataFrame, dims: dict) -> None:
    s = specs.sort_values("RP").reset_index(drop=True)
    linhas = [(dim, op) for dim, ops in dims.items() for op in ops]
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(13, 9.5), sharex=True, gridspec_kw={"height_ratios": [1.1, 1.5]})
    sig = s["ic_inf"] > 1
    x = np.arange(len(s))
    for mask, cor, rot in [(sig, AZUL, "IC 95% acima de 1"), (~sig, NEUTRO, "IC 95% inclui 1")]:
        a1.errorbar(x[mask], s.loc[mask, "RP"], yerr=[s.loc[mask, "RP"] - s.loc[mask, "ic_inf"], s.loc[mask, "ic_sup"] - s.loc[mask, "RP"]],
                    fmt="o", ms=3.5, color=cor, elinewidth=0.8, label=rot)
    a1.axhline(1, color=INK2, lw=1)
    a1.axhline(s["RP"].median(), color=AZUL, lw=1, ls="--")
    a1.annotate(f"mediana RP = {s['RP'].median():.2f}", (len(s) * 0.02, s["RP"].median()), xytext=(0, 5),
                textcoords="offset points", fontsize=9, color=INK2)
    a1.set_yscale("log")
    ticks = [0.8, 1, 1.25, 1.5, 2, 2.5]
    a1.set_yticks([t for t in ticks if s["ic_inf"].min() * 0.9 <= t <= s["ic_sup"].max() * 1.1] + [1])
    a1.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}".replace(".", ",")))
    a1.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    a1.set_ylabel("Razão de prevalência (escala log)")
    a1.legend(loc="upper left")
    a1.set_title(f"{len(s)} especificações analíticas defensáveis — cada ponto é um modelo", loc="left", fontsize=10,
                 color=INK2, fontweight="normal")
    for j, (dim, op) in enumerate(linhas):
        ativo = s[dim] == op
        a2.scatter(x[ativo], np.full(ativo.sum(), j), s=6, color=INK2, marker="s")
    a2.set_yticks(range(len(linhas)))
    a2.set_yticklabels([f"{op}" for _, op in linhas], fontsize=8.5)
    a2.invert_yaxis()
    a2.grid(False)
    a2.set_xlabel("Especificações ordenadas pela RP")
    y0 = 0
    for dim, ops in dims.items():
        a2.axhline(y0 - 0.5, color=GRID, lw=0.8)
        a2.annotate(dim.upper(), (1.005, y0 + (len(ops) - 1) / 2), xycoords=("axes fraction", "data"), ha="left",
                    va="center", fontsize=8, color=MUTED, fontweight="bold", annotation_clip=False)
        y0 += len(ops)
    fig.suptitle("Specification curve: a associação sobrevive às escolhas do analista?", x=0.01, ha="left",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(GRAF / "06_specification_curve.png", dpi=160)
    plt.close(fig)


# ===========================================================================
# Relatório markdown
# ===========================================================================
def fmt_p(p: float) -> str:
    return "< 0,001" if p < 0.001 else f"{p:.3f}".replace(".", ",")


def fmt_rp(c: dict, chave: str = "RP", dec: int = 2) -> str:
    return f"{c[chave]:.{dec}f} [{c['ic95'][0]:.{dec}f}; {c['ic95'][1]:.{dec}f}]"


def escrever_markdown(res: dict) -> None:
    L = ["# Resultados estatísticos (gerado automaticamente por `analise_exploratoria.py`)", "",
         f"Base: PNS 2019 — {res['n_total']:,} pessoas de 15+ anos com tempo de tela e PHQ-9 completos. "
         "Toda inferência usa o desenho amostral (estrato + UPA + peso V00291).".replace(",", "."), ""]
    v = res["validacao_externa"]
    L += ["## 0. Validação externa", "", "| Indicador | Este pipeline | Literatura |", "|---|---|---|",
          f"| PHQ-9 ≥ 10 | {v['phq9_10']['pct']:.2f}% [{v['phq9_10']['ic'][0]:.2f}; {v['phq9_10']['ic'][1]:.2f}] | 10,8% [10,4; 11,0] |",
          f"| PHQ-9 algoritmo | {v['phq9_alg']['pct']:.2f}% [{v['phq9_alg']['ic'][0]:.2f}; {v['phq9_alg']['ic'][1]:.2f}] | 5,7% [5,4; 6,0] |", ""]
    L += ["## 1. Hipótese primária — RP ajustada de PHQ-9 ≥ 10 por faixa de tela (ref. < 1h)", "",
          "| Faixa | Bruta | Ajustada (principal) | Ajustada (estendida) |", "|---|---|---|---|"]
    p = res["primario"]
    for c in ORDEM_TELA:
        if c == "<1h":
            continue
        L.append(f"| {c} | {fmt_rp(p['bruto'][c])} | {fmt_rp(p['ajustado'][c])} | {fmt_rp(p['estendido'][c])} |")
    t = p["tendencia_usuarios"]
    L += ["", f"**H1 — tendência entre usuários (RP por faixa):** {fmt_rp(t)}, p {fmt_p(t['p'])} (n = {p['n_usuarios']:,}).".replace(",", "."),
          f"Não linearidade (Wald, 3 gl): χ² = {p['nao_linearidade']['chi2']:.1f}, p {fmt_p(p['nao_linearidade']['p'])}.",
          f"Exploratório — faixas abaixo de 3h (1–2h e 2–3h = 1): p {fmt_p(p['wald_abaixo_3h']['p'])}; "
          f"faixas acima de 3h (3–6h e 6h+ = 1): p {fmt_p(p['wald_acima_3h']['p'])}.", ""]
    L += ["## 2. Desfechos secundários e interações (q = FDR de Benjamini-Hochberg)", "",
          "| Teste | Estimativa | p | q (FDR) |", "|---|---|---:|---:|"]
    for t in res["testes_secundarios"]:
        L.append(f"| {t['teste']} | {t['estimativa']} | {fmt_p(t['p'])} | {fmt_p(t['q'])} |")
    L += ["", "## 3. Interações (domínio: usuários; exposição 3h+ vs <3h)", ""]
    for nome, it in res["interacoes"].items():
        L += [f"**{nome}**", "",
              f"- RP no grupo de referência: {fmt_rp(it['RP_ref'])}; no grupo comparado: {fmt_rp(it['RP_comp'])}",
              f"- Interação multiplicativa (razão de RPs): {fmt_rp(it['multiplicativa'])}, p {fmt_p(it['multiplicativa']['p'])}",
              f"- Excesso absoluto da exposição (p.p.): referência {it['DP_ref']['dif_pp']:.2f} [{it['DP_ref']['ic95'][0]:.2f}; {it['DP_ref']['ic95'][1]:.2f}]; "
              f"comparado {it['DP_comp']['dif_pp']:.2f} [{it['DP_comp']['ic95'][0]:.2f}; {it['DP_comp']['ic95'][1]:.2f}]",
              f"- Interação aditiva (diferença das diferenças, p.p.): {it['aditiva_pp']['dif_pp']:.2f} "
              f"[{it['aditiva_pp']['ic95'][0]:.2f}; {it['aditiva_pp']['ic95'][1]:.2f}], p {fmt_p(it['aditiva_pp']['p'])}",
              f"- RERI: {it['RERI']['RERI']:.2f} [{it['RERI']['ic95'][0]:.2f}; {it['RERI']['ic95'][1]:.2f}], p {fmt_p(it['RERI']['p'])}", ""]
    L += ["## 4. Robustez", "", "| Medida | Valor |", "|---|---|"]
    for k, e in res["e_values"].items():
        L.append(f"| E-value {k} | {e['estimativa']:.2f} (limite do IC: {e['limite_ic']:.2f}) |")
    for k, f in res["fap_hipotetica"].items():
        L.append(f"| FAP hipotética {k} | {100 * f:.1f}% |")
    sc = res["specification_curve"]["resumo"]
    L += [f"| Specification curve | {sc['n']} modelos; mediana RP {sc['mediana_RP']:.2f}; "
          f"{sc['pct_RP_acima_1']:.0f}% com RP > 1; {sc['pct_IC_acima_1']:.0f}% com IC acima de 1 |", ""]
    L += ["| Desfecho (spec curve) | n | Mediana RP | % IC > 1 |", "|---|---:|---:|---:|"]
    for k, d in res["specification_curve"]["por_desfecho"].items():
        L.append(f"| {k} | {d['n']} | {d['mediana_RP']:.2f} | {d['pct_IC_acima_1']:.0f}% |")
    L += ["", "| Exposição (spec curve) | n | Mediana RP | % IC > 1 |", "|---|---:|---:|---:|"]
    for k, d in res["specification_curve"]["por_exposicao"].items():
        L.append(f"| {k} | {d['n']} | {d['mediana_RP']:.2f} | {d['pct_IC_acima_1']:.0f}% |")
    L += ["", "## 5. Correlações (descritivas)", "", "| Par | ρ | IC 95% | p | Força |", "|---|---:|---|---:|---|"]
    for k, c in res["correlacoes_spearman"].items():
        L.append(f"| {k} | {c['rho']:.3f} | [{c['ic95'][0]:.3f}; {c['ic95'][1]:.3f}] | {fmt_p(c['p'])} | {c['efeito']} |")
    for k, c in res["correlacoes_parciais"].items():
        L.append(f"| {k} (parcial) | {c['rho_parcial']:.3f} | [{c['ic95'][0]:.3f}; {c['ic95'][1]:.3f}] | {fmt_p(c['p'])} | {c['efeito']} |")
    L += ["", "| Usuários, por idade (tela × PHQ-9) | ρ | IC 95% | n |", "|---|---:|---|---:|"]
    for k, c in res["spearman_usuarios_por_idade"].items():
        L.append(f"| {k} | {c['rho']:.3f} | [{c['ic95'][0]:.3f}; {c['ic95'][1]:.3f}] | {c['n']:,} |")
    L += ["", "## 6. Perfil por faixa de tela", "", pd.DataFrame(res["perfil_por_faixa_de_tela"]).to_markdown(index=False), "",
          "## 7. Prevalências ponderadas", ""]
    for nome, tab in res["prevalencias"].items():
        L += [f"**{nome}**", "", pd.DataFrame(tab).round(2).to_markdown(index=False), ""]
    (OUT / "resultados_estatisticos.md").write_text("\n".join(L))


# ===========================================================================
def main() -> None:
    GRAF.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DADOS)
    print(f"[INFO] {len(df):,} registros carregados de {DADOS.name}")
    df["tela_cat"] = pd.Categorical(df["tela_lazer_ord"].map(TELA_ROTULO), categories=["<1h"] + [c for c in ORDEM_TELA if c != "<1h"])
    df["usuario"] = df["tela_lazer_ord"] >= 1
    df["tela_3h"] = (df["tela_lazer_ord"] >= 4).astype(int)
    df["jovem"] = df["faixa_etaria"].isin(["15–17", "18–24"]).astype(int)
    for k in (3, 4, 5):
        df[f"d{k}"] = (df["tela_lazer_ord"] == k).astype(int)
    usuarios = df["usuario"]
    res: dict = {"n_total": int(len(df))}

    # --- 0. Validação externa ----------------------------------------------
    v = {}
    for nome, y in [("phq9_10", "phq9_depressao"), ("phq9_alg", "phq9_algoritmo")]:
        est, se, _ = media_amostral(df, y)
        v[nome] = {"pct": 100 * est, "ic": [100 * (est - 1.96 * se), 100 * (est + 1.96 * se)]}
    res["validacao_externa"] = v

    # --- 1. Hipótese primária -----------------------------------------------
    print("[INFO] Modelos principais (RP, desenho completo)…")
    m_bruto = svyglm(df, "phq9_depressao ~ tela_cat")
    m_aj = svyglm(df, f"phq9_depressao ~ tela_cat + {CTRL}")
    m_ext = svyglm(df, f"phq9_depressao ~ tela_cat + {CTRL_EXT}")
    m_lin = svyglm(df, f"phq9_depressao ~ tela_lazer_ord + {CTRL}", dominio=usuarios)
    m_nl = svyglm(df, f"phq9_depressao ~ tela_lazer_ord + d3 + d4 + d5 + {CTRL}", dominio=usuarios)
    res["primario"] = {
        "bruto": tela_coefs(m_bruto), "ajustado": tela_coefs(m_aj), "estendido": tela_coefs(m_ext),
        "ajustado_completo": m_aj.tabela(), "n": m_aj.n, "n_upas": m_aj.n_upas, "estratos_uma_upa": m_aj.estratos_uma_upa,
        "tendencia_usuarios": m_lin.coef("tela_lazer_ord"), "n_usuarios": m_lin.n,
        "nao_linearidade": wald(m_nl, ["d3", "d4", "d5"]),
        "wald_abaixo_3h": wald(m_aj, ["tela_cat[T.1–2h]", "tela_cat[T.2–3h]"]),
        "wald_acima_3h": wald(m_aj, ["tela_cat[T.3–6h]", "tela_cat[T.6h+]"]),
    }
    modelos_rp = {"phq9_depressao": {"RP_por_faixa": res["primario"]["ajustado"]}}

    # --- 2. Secundários -------------------------------------------------------
    testes = []
    secundarios = {}
    for y in ["concentracao_frequente", "diag_outro_transtorno_mental"]:
        aj = svyglm(df, f"{y} ~ tela_cat + {CTRL}")
        lin = svyglm(df, f"{y} ~ tela_lazer_ord + {CTRL}", dominio=usuarios)
        nl = svyglm(df, f"{y} ~ tela_lazer_ord + d3 + d4 + d5 + {CTRL}", dominio=usuarios)
        secundarios[y] = {"RP_por_faixa": tela_coefs(aj), "tendencia_usuarios": lin.coef("tela_lazer_ord"),
                          "nao_linearidade": wald(nl, ["d3", "d4", "d5"]), "n": aj.n}
        modelos_rp[y] = {"RP_por_faixa": secundarios[y]["RP_por_faixa"]}
        rot = DESFECHOS[y]
        for faixa in ["3–6h", "6h+"]:
            c = secundarios[y]["RP_por_faixa"][faixa]
            testes.append({"teste": f"{rot}: RP {faixa} vs <1h", "estimativa": fmt_rp(c), "p": c["p"]})
        c = secundarios[y]["tendencia_usuarios"]
        testes.append({"teste": f"{rot}: tendência entre usuários", "estimativa": fmt_rp(c), "p": c["p"]})
        testes.append({"teste": f"{rot}: não linearidade", "estimativa": f"χ² = {secundarios[y]['nao_linearidade']['chi2']:.1f}",
                       "p": secundarios[y]["nao_linearidade"]["p"]})
    res["secundarios"] = secundarios

    # --- 3. Interações (ODS 5 e idade) ----------------------------------------
    print("[INFO] Interações…")
    interacoes = {}
    for nome, mod, ctrl in [("Sexo (ref. homens; comparado: mulheres)", "sexo_feminino", CTRL_SEM_SEXO),
                            ("Idade (ref. 25+; comparado: 15–24 anos)", "jovem", CTRL_SEM_IDADE)]:
        f = f"phq9_depressao ~ tela_3h * {mod} + {ctrl}"
        mp = svyglm(df, f, dominio=usuarios)
        ma = svyglm(df, f, familia="gauss-identidade", dominio=usuarios)
        it = f"tela_3h:{mod}"
        interacoes[nome] = {
            "RP_ref": mp.coef("tela_3h"), "RP_comp": combinacao(mp, {"tela_3h": 1, it: 1}),
            "multiplicativa": mp.coef(it), "RERI": reri(mp, "tela_3h", mod, it),
            "DP_ref": ma.coef("tela_3h"), "DP_comp": combinacao(ma, {"tela_3h": 1, it: 1}),
            "aditiva_pp": ma.coef(it), "n": mp.n}
        testes.append({"teste": f"Interação multiplicativa — {nome}", "estimativa": fmt_rp(mp.coef(it)), "p": mp.coef(it)["p"]})
        c = ma.coef(it)
        testes.append({"teste": f"Interação aditiva (p.p.) — {nome}",
                       "estimativa": f"{c['dif_pp']:.2f} [{c['ic95'][0]:.2f}; {c['ic95'][1]:.2f}]", "p": c["p"]})
    res["interacoes"] = interacoes

    q = multipletests([t["p"] for t in testes], method="fdr_bh")[1]
    for t, qq in zip(testes, q):
        t["q"] = float(qq)
    res["testes_secundarios"] = testes

    # --- 4. Robustez: E-value e FAP --------------------------------------------
    aj = res["primario"]["ajustado"]
    res["e_values"] = {f"PHQ-9 ≥ 10, {k} vs <1h": e_value(aj[k]["RP"], aj[k]["ic95"][0]) for k in ["3–6h", "6h+"]}
    for y in ["concentracao_frequente", "diag_outro_transtorno_mental"]:
        c = secundarios[y]["RP_por_faixa"]["6h+"]
        res["e_values"][f"{DESFECHOS[y]}, 6h+ vs <1h"] = e_value(c["RP"], c["ic95"][0])
    casos = df["phq9_depressao"] == 1
    w_casos = df.loc[casos, "peso"].sum()
    pc = {k: df.loc[casos & (df["tela_cat"] == k), "peso"].sum() / w_casos for k in ["3–6h", "6h+"]}
    res["fap_hipotetica"] = {"PHQ-9 ≥ 10 atribuível a 3h+ (supõe causalidade)": fap(pc, {k: aj[k]["RP"] for k in pc})}
    res["proporcao_casos_por_faixa"] = pc

    # --- 5. Specification curve -------------------------------------------------
    print("[INFO] Specification curve (144 modelos)…")
    dims = {
        "desfecho": {"PHQ-9 ≥ 10": "phq9_depressao", "PHQ-9 algoritmo": "phq9_algoritmo",
                     "Escore PHQ-9": "phq9_escore", "Concentração": "concentracao_frequente"},
        "exposição": {"6h+ vs <1h": ("tela_lazer_ord", "x6"), "3h+ vs 1–3h (usuários)": ("usuario", "tela_3h"),
                      "3h+ vs <3h (todos)": (None, "tela_3h")},
        "covariáveis": {"mínimo": CTRL_MIN, "principal": CTRL, "estendido": CTRL_EXT},
        "amostra": {"15+": 15, "18+": 18},
        "pesos": {"com peso": True, "sem peso": False},
    }
    df["x6"] = (df["tela_lazer_ord"] == 5).astype(int)
    specs = []
    for (dn, y), (en, (dom_col, x)), (cn, ctrl), (an, idade_min), (pn, pond) in product(*[d.items() for d in dims.values()]):
        dom = df["idade"] >= idade_min
        if dom_col == "tela_lazer_ord":
            dom &= df["tela_lazer_ord"].isin([1, 5])
        elif dom_col == "usuario":
            dom &= df["usuario"]
        a = svyglm(df, f"{y} ~ {x} + {ctrl}", dominio=dom, ponderar=pond)
        c = a.coef(x)
        specs.append({"desfecho": dn, "exposição": en, "covariáveis": cn, "amostra": an, "pesos": pn,
                      "RP": c["RP"], "ic_inf": c["ic95"][0], "ic_sup": c["ic95"][1], "p": c["p"], "n": a.n})
    specs = pd.DataFrame(specs)

    def resumo(d: pd.DataFrame) -> dict:
        return {"n": int(len(d)), "mediana_RP": float(d["RP"].median()), "min_RP": float(d["RP"].min()),
                "max_RP": float(d["RP"].max()), "pct_RP_acima_1": float(100 * (d["RP"] > 1).mean()),
                "pct_IC_acima_1": float(100 * (d["ic_inf"] > 1).mean())}
    res["specification_curve"] = {
        "resumo": resumo(specs),
        "por_desfecho": {k: resumo(g) for k, g in specs.groupby("desfecho")},
        "por_exposicao": {k: resumo(g) for k, g in specs.groupby("exposição")},
        "especificacoes": specs.to_dict("records")}
    grafico_spec_curve(specs, {k: list(v_) for k, v_ in dims.items()})

    # --- 6. Descritivos: correlações, perfil, prevalências ----------------------
    desc = {"phq9": "phq9_escore", "concentracao": "phq_concentracao", "sono": "phq_sono", "agitacao": "phq_agitacao",
            "humor_deprimido": "phq_humor_deprimido", "diag_ansiedade_outros": "diag_outro_transtorno_mental"}
    cor = {f"tela_x_{n}": spearman_ic(df["tela_lazer_ord"], df[c]) for n, c in desc.items()}
    res["correlacoes_spearman"] = cor
    controles = ["idade", "sexo_feminino", "escolaridade", "renda_faixa"]
    res["correlacoes_parciais"] = {f"tela_x_{n}": spearman_parcial(df, "tela_lazer_ord", desc[n], controles)
                                   for n in ["phq9", "concentracao"]}
    u = df[usuarios]
    res["spearman_usuarios_por_idade"] = {f: spearman_ic(u.loc[u.faixa_etaria == f, "tela_lazer_ord"],
                                                         u.loc[u.faixa_etaria == f, "phq9_escore"]) for f in FAIXAS}
    perfil = []
    for k in range(6):
        dom = df["tela_lazer_ord"] == k
        g = df[dom]
        perfil.append({"tela": TELA_ROTULO[k], "n": int(dom.sum()),
                       "idade_media": round(media_amostral(df, "idade", dom)[0], 1),
                       "pct_60_mais": round(100 * media_amostral(df.assign(v=(df["idade"] >= 60).astype(int)), "v", dom)[0], 1),
                       "pct_ate_1SM": round(100 * media_amostral(df.assign(v=(df["renda_faixa"] <= 3).astype(float).where(df["renda_faixa"].notna())), "v", dom)[0], 1),
                       "pct_mulheres": round(100 * media_amostral(df, "sexo_feminino", dom)[0], 1)})
        del g
    res["perfil_por_faixa_de_tela"] = perfil

    prev_dep = tabela_prevalencia(df, "phq9_depressao", ["sexo", "tela_lazer_ord"])
    prev_conc = tabela_prevalencia(df, "concentracao_frequente", ["sexo", "tela_lazer_ord"])
    prev_uso = tabela_prevalencia(df, "tela_lazer_3h_mais", ["faixa_etaria"])
    prev_dep_idade = tabela_prevalencia(df, "phq9_depressao", ["faixa_etaria", "tela_lazer_3h_mais"])
    res["prevalencias"] = {
        "PHQ-9>=10 por faixa de tela": tabela_prevalencia(df, "phq9_depressao", ["tela_lazer_ord"]).to_dict("records"),
        "PHQ-9>=10 por sexo e tela": prev_dep.to_dict("records"),
        "Concentracao frequente por sexo e tela": prev_conc.to_dict("records"),
        "Uso 3h+ por faixa etaria": prev_uso.to_dict("records"),
        "Uso 3h+ por sexo": tabela_prevalencia(df, "tela_lazer_3h_mais", ["sexo"]).to_dict("records"),
        "PHQ-9>=10 por faixa etaria e uso 3h+": prev_dep_idade.to_dict("records"),
        "PHQ-9>=10 por sexo": tabela_prevalencia(df, "phq9_depressao", ["sexo"]).to_dict("records"),
        "Uso 6h+ por faixa etaria": tabela_prevalencia(df.assign(u6=(df["tela_lazer_ord"] == 5).astype(int)), "u6", ["faixa_etaria"]).to_dict("records"),
    }
    res["populacao_estimada_milhoes"] = {
        "15+": df["peso"].sum() / 1e6, "3h+": df.loc[df["tela_3h"] == 1, "peso"].sum() / 1e6,
        "6h+": df.loc[df["tela_lazer_ord"] == 5, "peso"].sum() / 1e6,
        "6h+ e PHQ-9>=10": df.loc[(df["tela_lazer_ord"] == 5) & casos, "peso"].sum() / 1e6}

    # --- 6b. Indicadores e perfil do segmento-alvo para o Grupo 2 ----------------
    df["tela_6h"] = (df["tela_lazer_ord"] == 5).astype(int)
    df["faixa_jovem"] = np.where(df["jovem"] == 1, "15–24", "25+")
    ind = []
    for indicador, y in [("Uso de tela de lazer 3h+/dia", "tela_3h"), ("Uso de tela de lazer 6h+/dia", "tela_6h")]:
        for grupos in (["faixa_etaria"], ["sexo"], ["faixa_etaria", "sexo"]):
            for linha in tabela_prevalencia(df, y, grupos).to_dict("records"):
                ind.append({"indicador": indicador, "recorte": " · ".join(str(linha[g]) for g in grupos), **{k: linha[k] for k in ("pct", "ic_inf", "ic_sup", "n")}})
    for y, rot in DESFECHOS.items():
        for grupos in (["tela_cat", "sexo"], ["tela_cat", "faixa_jovem"]):
            for linha in tabela_prevalencia(df, y, grupos).to_dict("records"):
                ind.append({"indicador": rot, "recorte": " · ".join(str(linha[g]) for g in grupos), **{k: linha[k] for k in ("pct", "ic_inf", "ic_sup", "n")}})
    pd.DataFrame(ind).round(2).to_csv(OUT / "indicadores_grupo2.csv", index=False)

    segmentos = {"15–24 anos, 6h+/dia": (df["jovem"] == 1) & (df["tela_lazer_ord"] == 5),
                 "15–24 anos, 3h+/dia": (df["jovem"] == 1) & (df["tela_3h"] == 1),
                 "15–24 anos, usuários com <3h/dia": (df["jovem"] == 1) & df["usuario"] & (df["tela_3h"] == 0),
                 "Mulheres 15–24 anos, 6h+/dia": (df["jovem"] == 1) & (df["tela_lazer_ord"] == 5) & (df["sexo_feminino"] == 1)}
    aux = df.assign(renda_ate_1sm=(df["renda_faixa"] <= 3).astype(float).where(df["renda_faixa"].notna()),
                    urbano=1 - df["zona_rural"], ocupado=(df["ocupacao"] == "Ocupado").astype(int),
                    fora_forca=(df["ocupacao"] == "Fora da força de trabalho").astype(int),
                    idade_15_17=(df["faixa_etaria"] == "15–17").astype(int))
    metricas = {"idade_media": "idade", "pct_15_17": "idade_15_17", "pct_mulheres": "sexo_feminino",
                "pct_frequenta_escola": "frequenta_escola", "pct_ocupado": "ocupado", "pct_fora_forca_trabalho": "fora_forca",
                "pct_renda_ate_1SM": "renda_ate_1sm", "pct_urbano": "urbano", "pct_internet_domicilio": "internet_domicilio",
                "pct_phq9_10": "phq9_depressao", "pct_concentracao_frequente": "concentracao_frequente",
                "pct_sono_frequente": "sono_frequente", "pct_diag_ansiedade_outros": "diag_outro_transtorno_mental"}
    perfil_seg = {}
    for nome, dom in segmentos.items():
        linha = {"n": int(dom.sum()), "populacao_milhoes": float(df.loc[dom, "peso"].sum() / 1e6)}
        for chave, col in metricas.items():
            est, se, _ = media_amostral(aux, col, dom)
            fator = 1 if chave == "idade_media" else 100
            linha[chave] = {"valor": fator * est, "ic95": [fator * (est - 1.96 * se), fator * (est + 1.96 * se)]}
        perfil_seg[nome] = linha
    res["perfil_segmento_alvo"] = perfil_seg

    # --- 7. Gráficos e saída ----------------------------------------------------
    grafico_scatter(df, cor)
    res["matriz_spearman"] = grafico_heatmap(df).round(4).to_dict()
    grafico_barras_sexo(prev_dep, prev_conc)
    grafico_barras_idade(prev_uso, prev_dep_idade)
    grafico_dose_resposta(modelos_rp)
    (OUT / "graficos" / "05_dose_resposta_OR.png").unlink(missing_ok=True)
    (OUT / "resultados_estatisticos.json").write_text(json.dumps(res, ensure_ascii=False, indent=2, default=float))
    escrever_markdown(res)

    print("\n=== HIPÓTESE PRIMÁRIA (PHQ-9 ≥ 10) ===")
    for k, c in res["primario"]["ajustado"].items():
        print(f"  {k:<8} RP aj = {fmt_rp(c)}  p={c['p']:.2g}")
    t = res["primario"]["tendencia_usuarios"]
    print(f"  Tendência (usuários): RP/faixa = {fmt_rp(t, dec=3)} p={t['p']:.2g}")
    print(f"  Não linearidade: p={res['primario']['nao_linearidade']['p']:.2g}")
    print(f"[OK] Spec curve: {res['specification_curve']['resumo']}")
    print(f"[OK] Saídas em {OUT}")


if __name__ == "__main__":
    main()
