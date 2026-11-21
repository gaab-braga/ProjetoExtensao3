# Uso Intenso de Telas e Saúde Mental no Brasil

**Centro Universitário IESB · Projeto de Extensão na Educação Superior · Trilha de Pesquisa**
**Tema norteador:** Saúde Mental · **ODS 3** (meta 3.4) e **ODS 5** · **Professor orientador:** Prof. Guilherme Bueno

Pesquisa com os microdados oficiais da Pesquisa Nacional de Saúde 2019 (IBGE), com 90.846 pessoas que representam 168 milhões de brasileiros com 15 anos ou mais.

---

## 📄 Comece por aqui

### ➜ [**RELATORIO_FINAL_DA_PESQUISA.pdf**](RELATORIO_FINAL_DA_PESQUISA.pdf) — o documento oficial da pesquisa, de ponta a ponta
Versão para leitura no navegador: [`RELATORIO_FINAL_DA_PESQUISA.md`](RELATORIO_FINAL_DA_PESQUISA.md)

O relatório contém resumo, introdução (com o Mapa do Projeto), objetivos e hipóteses, métodos, resultados (Figuras 1 a 6), discussão, limitações, conclusão e referências. Cada seção indica o arquivo que a sustenta.

**Pergunta de pesquisa:** *Como o uso intenso de telas para lazer — que inclui redes sociais e vídeos curtos — influencia a saúde mental, em especial a ansiedade e os sintomas depressivos, e o déficit de atenção na sociedade contemporânea?*

**Principal resultado:** até cerca de 3 horas por dia de tela de lazer, a prevalência de sintomas não muda; acima disso, ela sobe. Com 6 horas ou mais, o rastreio positivo para depressão é 1,59 vez mais frequente e a dificuldade de concentração, 1,55 vez. O uso intenso concentra-se nos jovens, e as mulheres têm 2,5 vezes mais sintomas depressivos. O resultado se manteve em 144 análises alternativas. O estudo é transversal: mostra associação, não causa.

---

## 🗂️ Organização do repositório

| Pasta / arquivo | Conteúdo |
|---|---|
| **`RELATORIO_FINAL_DA_PESQUISA.pdf`** | Documento oficial (com figuras) |
| **`anexos/`** | Anexos A a G, citados no relatório |
| &nbsp;&nbsp;`Anexo_A_Selecao_da_Base_de_Dados.md` | Bases avaliadas e variáveis escolhidas |
| &nbsp;&nbsp;`Anexo_B_Obtencao_e_Preparacao_dos_Dados.md` | Origem dos dados e procedimento replicável |
| &nbsp;&nbsp;`Anexo_C_Rigor_Metodologico.md` | Método científico, STROBE, ética, histórico das decisões |
| &nbsp;&nbsp;`Anexo_D_Arvore_de_Problemas.md` | Causas e efeitos do problema |
| &nbsp;&nbsp;`Anexo_E_Perfil_do_Publico_Alvo.md` | Retrato estatístico do público mais exposto |
| &nbsp;&nbsp;`Anexo_F_Referencias_e_Questoes_Futuras.md` | Referências completas e perguntas para estudos futuros |
| &nbsp;&nbsp;`Anexo_G_Literatura_Periodicos_e_Fichamentos.md` | Periódicos consultados, artigos correlacionados, fichamentos e fichamento dos achados |
| **`resultados/figuras/`** | `Mapa_do_Projeto.png` e `Figura_1_…` a `Figura_6_…`, na ordem do relatório |
| **`resultados/tabelas/`** | Todas as tabelas (`resultados_estatisticos.md`), indicadores em planilha (`indicadores_por_grupo.csv`) e registro da preparação dos dados |
| **`codigo/`** | `preparacao_dos_dados.py` → `analise_estatistica.py` (+ `metodos_amostrais.py` e `testes/`); `mapa_do_projeto.py` gera o Mapa do Projeto |
| **`dados/`** | Pasta local para os microdados do IBGE (não versionados; ver Anexo B) |

## 🔁 Reprodutibilidade

```bash
pip install -r codigo/requirements.txt
python -m pytest codigo/testes
python codigo/preparacao_dos_dados.py
python codigo/analise_estatistica.py
python codigo/mapa_do_projeto.py
```

Instruções para baixar os microdados do IBGE: [Anexo B](anexos/Anexo_B_Obtencao_e_Preparacao_dos_Dados.md).

## Ética, licença e citação

- **Ética:** dados públicos e anonimizados; exceções do art. 1º, parágrafo único, da Resolução CNS nº 510/2016.
- **Licenças:** código sob [MIT](LICENSE); documentos, figuras e tabelas sob [CC BY 4.0](LICENSE-docs.md).
- **Como citar:** [`CITATION.cff`](CITATION.cff).
