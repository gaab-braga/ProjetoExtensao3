"""
mapa_do_projeto.py — Gera o Mapa do Projeto (etapa 8 do roteiro DreamShaper).

O mapa liga os cursos do grupo aos tópicos da pesquisa, ao tema norteador,
à questão de pesquisa e às tendências de cada área. O rodapé resume a evidência
principal, cujos números vêm de resultados/tabelas/resultados_estatisticos.json.

Uso:  python codigo/mapa_do_projeto.py            (salva em resultados/figuras/Mapa_do_Projeto.png)
      python codigo/mapa_do_projeto.py saida.png  (salva no caminho indicado)
"""
import sys, textwrap
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parent.parent
OUT = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "resultados" / "figuras" / "Mapa_do_Projeto.png")
AZUL, AZUL_CLARO, INK, INK2, CINZA = "#2a78d6", "#e8f1fc", "#0b0b0b", "#52514e", "#f3f3f1"
LARANJA, VERDE = "#eb6834", "#1baf7a"

linhas = [
    ("CURSOS DE GRADUAÇÃO", ["Análise e Desenvolvimento de Sistemas", "Engenharia de Software", "Design de Interiores"], AZUL),
    ("TÓPICOS DA PESQUISA", ["Tempo de tela e dependência digital", "Sintomas depressivos e ansiedade em jovens", "Atenção e concentração", "Desigualdade de gênero em saúde"], AZUL),
    ("TEMA", ["Saúde Mental  ·  ODS 3 (meta 3.4) e ODS 5"], LARANJA),
    ("QUESTÃO DE PESQUISA", ["Como o uso intenso de telas para lazer — que inclui redes sociais e vídeos curtos — influencia a saúde mental, em especial a ansiedade e os sintomas depressivos, e o déficit de atenção na sociedade contemporânea?"], LARANJA),
    ("TENDÊNCIAS DAS ÁREAS", ["ADS: ferramentas de bem-estar digital e análise de dados de uso", "Eng. de Software: design persuasivo (notificações, rolagem infinita, recomendação) e design ético", "Design de Interiores: ambientes que favorecem descanso e foco, com espaços livres de telas"], VERDE),
]

fig = plt.figure(figsize=(13, 10.5), dpi=160)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
fig.patch.set_facecolor("#fcfcfb")
ax.text(4, 96, "Mapa do Projeto", fontsize=24, fontweight="bold", color=INK, va="center")
ax.text(4, 92.3, "Projeto de Extensão IESB · Trilha de Pesquisa · Tema norteador: Saúde Mental", fontsize=12, color=INK2, va="center")

topo, alt, gap = 87.5, 12.4, 3.0
for i, (rot, itens, cor) in enumerate(linhas):
    y = topo - i * (alt + gap) - alt
    ax.add_patch(FancyBboxPatch((4, y), 92, alt, boxstyle="round,pad=0,rounding_size=1.2", fc=CINZA, ec="none"))
    ax.add_patch(FancyBboxPatch((4, y), 22, alt, boxstyle="round,pad=0,rounding_size=1.2", fc=cor, ec="none"))
    ax.text(15, y + alt / 2, "\n".join(textwrap.wrap(rot, 14)), ha="center", va="center", color="white", fontsize=11.5, fontweight="bold")
    n = len(itens)
    if n == 1:
        ax.text(28.5, y + alt / 2, "\n".join(textwrap.wrap(itens[0], 95)), va="center", fontsize=12.5 if len(itens[0]) < 60 else 11.5,
                color=INK, fontweight="bold" if len(itens[0]) < 60 else "normal")
    else:
        larg = (96 - 28.5 - 1.5) / n
        for j, it in enumerate(itens):
            x = 28.5 + j * larg
            ax.add_patch(FancyBboxPatch((x, y + 1.6), larg - 1.2, alt - 3.2, boxstyle="round,pad=0,rounding_size=0.8", fc="white", ec="#d9d8d2", lw=1))
            ax.text(x + (larg - 1.2) / 2, y + alt / 2, "\n".join(textwrap.wrap(it, int(larg * 1.35))), ha="center", va="center", fontsize=10.2, color=INK)
    if i < len(linhas) - 1:
        ax.annotate("", xy=(15, y - gap + 0.4), xytext=(15, y - 0.4), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.6))

ax.add_patch(FancyBboxPatch((4, 2.2), 92, 6.2, boxstyle="round,pad=0,rounding_size=1.0", fc=AZUL_CLARO, ec="none"))
ax.text(6, 5.3, "Evidência: IBGE, Pesquisa Nacional de Saúde 2019 (n = 90.846). Acima de ~3h/dia de tela de lazer, sintomas depressivos\n"
        "e dificuldade de concentração ficam mais frequentes (6h+: 1,59× e 1,55×). Comunidade estudada: Brasil, 15+ anos.",
        va="center", fontsize=10.8, color=INK)
fig.savefig(OUT, dpi=160, facecolor=fig.get_facecolor())
print("ok", OUT)
