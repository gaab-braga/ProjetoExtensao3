"""
mapa_do_projeto.py — Gera o Mapa do Projeto (etapa 8 do roteiro DreamShaper).

Como pede o roteiro, a questão de pesquisa fica no centro e se liga aos demais
elementos: cursos de graduação, tópicos da pesquisa, tema norteador e tendências
das áreas. O rodapé resume a evidência principal, cujos números vêm de
resultados/tabelas/resultados_estatisticos.json.

Uso:  python codigo/mapa_do_projeto.py            (salva em resultados/figuras/Mapa_do_Projeto.png)
      python codigo/mapa_do_projeto.py saida.png  (salva no caminho indicado)
"""
import sys
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parent.parent
OUT = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "resultados" / "figuras" / "Mapa_do_Projeto.png")

AZUL, AZUL_CLARO, INK, INK2, CINZA = "#2a78d6", "#e8f1fc", "#0b0b0b", "#52514e", "#d9d8d2"
LARANJA, VERDE, ROXO, FUNDO = "#eb6834", "#1baf7a", "#7a5bd6", "#fcfcfb"

QUESTAO = ("Como o uso intenso de telas para lazer — que inclui redes sociais e vídeos curtos — "
           "influencia a saúde mental, em especial a ansiedade e os sintomas depressivos, "
           "e o déficit de atenção na sociedade contemporânea?")

# (título, itens, cor, caixa: x0, y0, largura, altura, ponto de ligação na caixa)
BLOCOS = [
    ("CURSOS DE GRADUAÇÃO",
     ["Análise e Desenvolvimento de Sistemas", "Engenharia de Software", "Design de Interiores"],
     AZUL, (2, 65.5, 30, 22.5)),
    ("TÓPICOS DA PESQUISA",
     ["Tempo de tela e dependência digital", "Sintomas depressivos e ansiedade em jovens",
      "Atenção e concentração", "Desigualdade de gênero em saúde"],
     AZUL, (68, 65.5, 30, 22.5)),
    ("TEMA NORTEADOR",
     ["Saúde Mental", "ODS 3 — Saúde e bem-estar (meta 3.4)", "ODS 5 — Igualdade de gênero"],
     ROXO, (2, 10, 30, 27)),
    ("TENDÊNCIAS DAS ÁREAS",
     ["ADS: ferramentas de bem-estar digital e análise de dados de uso",
      "Eng. de Software: design persuasivo (notificações, rolagem infinita) e design ético",
      "Design de Interiores: ambientes de descanso e foco, com espaços sem telas"],
     VERDE, (68, 10, 30, 27)),
]

fig = plt.figure(figsize=(14, 10.5), dpi=160)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
fig.patch.set_facecolor(FUNDO)

ax.text(2, 96, "Mapa do Projeto", fontsize=24, fontweight="bold", color=INK, va="center")
ax.text(2, 92.4, "Projeto de Extensão IESB · Trilha de Pesquisa · Tema norteador: Saúde Mental",
        fontsize=12, color=INK2, va="center")

# Questão de pesquisa, no centro
cx0, cy0, cw, ch = 33, 41.5, 34, 20
centro = (cx0 + cw / 2, cy0 + ch / 2)

# Ligações (desenhadas antes das caixas, para ficarem por baixo)
for titulo, itens, cor, (x0, y0, w, h) in BLOCOS:
    bx = x0 + w - 6 if x0 < 50 else x0 + 6       # ponto na borda da caixa voltada para o centro
    by = y0 if y0 > 50 else y0 + h
    ex = cx0 + 6 if x0 < 50 else cx0 + cw - 6    # ponto na caixa central
    ey = cy0 + ch if y0 > 50 else cy0
    ax.plot([bx, ex], [by, ey], color=cor, lw=2.6, solid_capstyle="round", zorder=1)
    ax.plot([bx, ex], [by, ey], "o", color=cor, ms=8, zorder=3)

ax.add_patch(FancyBboxPatch((cx0, cy0), cw, ch, boxstyle="round,pad=0,rounding_size=1.6",
                            fc=LARANJA, ec="none", zorder=2))
ax.text(centro[0], cy0 + ch - 2.8, "QUESTÃO DE PESQUISA", ha="center", va="center",
        fontsize=12.5, fontweight="bold", color="white", zorder=4)
ax.text(centro[0], cy0 + ch / 2 - 1.6, "\n".join(textwrap.wrap(QUESTAO, 46)), ha="center", va="center",
        fontsize=11.6, color="white", linespacing=1.35, zorder=4)

for titulo, itens, cor, (x0, y0, w, h) in BLOCOS:
    ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0,rounding_size=1.2",
                                fc="white", ec=CINZA, lw=1.2, zorder=2))
    ax.add_patch(FancyBboxPatch((x0, y0 + h - 4.6), w, 4.6, boxstyle="round,pad=0,rounding_size=1.2",
                                fc=cor, ec="none", zorder=3))
    ax.text(x0 + w / 2, y0 + h - 2.3, titulo, ha="center", va="center", fontsize=12,
            fontweight="bold", color="white", zorder=4)
    y = y0 + h - 7.3
    for it in itens:
        linhas = textwrap.wrap(it, 40)
        ax.text(x0 + 1.8, y, "•", fontsize=11.5, color=cor, va="top", fontweight="bold", zorder=4)
        ax.text(x0 + 3.6, y, "\n".join(linhas), fontsize=10.6, color=INK, va="top", linespacing=1.25, zorder=4)
        y -= 2.4 * len(linhas) + 1.0

ax.add_patch(FancyBboxPatch((2, 1.2), 96, 6.6, boxstyle="round,pad=0,rounding_size=1.0", fc=AZUL_CLARO, ec="none"))
ax.text(4, 4.5, "Evidência: IBGE, Pesquisa Nacional de Saúde 2019 (n = 90.846). Acima de ~3h/dia de tela de lazer, "
        "sintomas depressivos e dificuldade de\nconcentração ficam mais frequentes (6h+: 1,59× e 1,55×). "
        "Comunidade estudada: Brasil, 15+ anos; público prioritário: jovens de 15 a 24 anos.",
        va="center", fontsize=10.8, color=INK, linespacing=1.4)

fig.savefig(OUT, dpi=160, facecolor=fig.get_facecolor())
print("ok", OUT)
