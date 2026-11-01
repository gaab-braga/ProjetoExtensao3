# Uso intenso de telas e saúde mental no Brasil

**Centro Universitário IESB · Projeto de Extensão · Grupo 1 (Problem Space)**
Evidências quantitativas a partir dos microdados oficiais da Pesquisa Nacional de Saúde 2019 (IBGE), entregues ao Grupo 2 para o desenho de uma solução.

---

## Eixo do projeto

| | |
|---|---|
| **Tema norteador** | Saúde Mental |
| **ODS** | **ODS 3** — Saúde e Bem-Estar (principal) · **ODS 5** — Igualdade de Gênero (justificado pelos dados, [Dossiê §4.5](Dossie_Evidencias_Quantitativas.md#45-gênero-ods-5)) |
| **Área do conhecimento** | Ciências Exatas e da Terra / Tecnológicas |
| **Subtema oficial** | Saúde mental, dependência digital e comportamento on-line |
| **Tema da equipe** | Ansiedade e dependência tecnológica na sociedade contemporânea: impactos do uso excessivo de tecnologias digitais na saúde mental |
| **Pergunta de pesquisa** | *Como o uso intenso de telas para lazer — que inclui redes sociais e vídeos curtos — influencia a saúde mental, em especial a ansiedade e os sintomas depressivos, e o déficit de atenção nas atividades do dia a dia, e que padrões de dados podem indicar caminhos para uma relação mais saudável com a tecnologia?* |
| **Fase (Double Diamond)** | Problem Space: **Descobrir** e **Definir** |
| **Base de dados** | IBGE — Pesquisa Nacional de Saúde 2019, microdados oficiais (n = 90.846; representa 168 milhões de brasileiros com 15+ anos) |

## Principal achado

Até cerca de **3 horas por dia** de tela de lazer (celular, tablet ou computador), a prevalência de sintomas é estável. **Acima disso ela sobe**: com **6h ou mais**, a prevalência de rastreio positivo para depressão é **1,59 vez maior** e a de dificuldade frequente de concentração, **1,55 vez maior** (razão de prevalência ajustada, com o desenho amostral da PNS). O resultado se repete em **144 de 144** análises alternativas. A exposição se concentra nos jovens: **59%** dos adolescentes de 15–17 anos usam 3h+ por dia. As **mulheres** carregam 2,5 vezes mais sintomas depressivos. O estudo é transversal e mostra **associação, não causa**.

---

## Para avaliadores: comece por aqui

| Ordem | Documento | O que encontrar | Tempo |
|---|---|---|---|
| 1 | [**Dossiê de Evidências Quantitativas**](Dossie_Evidencias_Quantitativas.md) | Entregável principal: fonte, método, resultados, veredito graduado, limitações | 15 min |
| 2 | [**Briefing para o Grupo 2**](docs/06_Briefing_Grupo2.md) | Passagem ao Solution Space: pergunta "Como poderíamos", público, princípios de design, métricas, restrições éticas e legais | 5 min |
| 3 | [**Rigor Metodológico**](docs/04_Rigor_Metodologico.md) | Método científico etapa por etapa, checklist STROBE, ética, histórico de decisões, conclusões corrigidas, reavaliação da pergunta | 10 min |
| 4 | [Árvore de Problemas](docs/07_Arvore_de_Problemas.md) · [Ficha de Dados da Persona](docs/08_Persona_Ficha_de_Dados.md) | Insumos para a trilha qualitativa, com o que é dado e o que é hipótese | 5 min |
| 5 | [Agenda de Pesquisa](docs/05_Agenda_de_Pesquisa.md) | Posicionamento na literatura, perguntas abertas, referências verificadas | 5 min |
| 6 | [Data Discovery](docs/01_Data_Discovery.md) · [Aquisição](docs/02_Aquisicao_Dados.md) | Por que esta base e de onde vieram os dados | 5 min |

## Entregáveis × exigências do projeto

| Exigência | Como foi atendida | Onde |
|---|---|---|
| Investigar diretamente **Saúde Mental** (tema norteador) | Todos os desfechos são de saúde mental: PHQ-9, concentração, diagnóstico de ansiedade/outros | [Dossiê §2](Dossie_Evidencias_Quantitativas.md#2-fonte-dos-dados-e-justificativa) |
| Articulação com **ODS 3, 5 e/ou 16** | ODS 3 central; ODS 5 justificado por dados de desigualdade de carga; ODS 16 não se aplica | [Dossiê §4.5](Dossie_Evidencias_Quantitativas.md#45-gênero-ods-5) · [Guia Operacional](docs/Guia_Operacional_G1.md) |
| **Base de dados pública e oficial** | Microdados da PNS 2019 baixados do FTP do IBGE, com integridade registrada (SHA-256) | [`docs/01`](docs/01_Data_Discovery.md) · [`docs/02`](docs/02_Aquisicao_Dados.md) · [`etl_relatorio.json`](data/processed/etl_relatorio.json) |
| **Problem Space** (Double Diamond) | Descobrir: mapeamento de 6 bases oficiais. Definir: evidência + pergunta "Como poderíamos" | [`docs/01`](docs/01_Data_Discovery.md) · [Dossiê](Dossie_Evidencias_Quantitativas.md) |
| **Dossiê para o Grupo 2** | Painel de evidências, pergunta "Como poderíamos", briefing, árvore de problemas e ficha da persona | [`docs/06`](docs/06_Briefing_Grupo2.md) · [`docs/07`](docs/07_Arvore_de_Problemas.md) · [`docs/08`](docs/08_Persona_Ficha_de_Dados.md) |
| Rigor e honestidade científica | Validação externa (2 prevalências oficiais reproduzidas), razão de prevalência, desenho amostral, FDR, specification curve, STROBE | [`docs/04`](docs/04_Rigor_Metodologico.md) |

---

## Estrutura do repositório

```
Dossie_Evidencias_Quantitativas.md   entregável principal
docs/
  01_Data_Discovery.md               bases avaliadas e colunas escolhidas
  02_Aquisicao_Dados.md              procedência dos dados
  03_Guia_Standup.md                 roteiro de apresentação e perguntas da banca
  04_Rigor_Metodologico.md           método científico, STROBE, ética, correções
  05_Agenda_de_Pesquisa.md           literatura, perguntas abertas, referências
  06_Briefing_Grupo2.md              passagem para o Grupo 2
  07_Arvore_de_Problemas.md          causas e efeitos (dado × hipótese)
  08_Persona_Ficha_de_Dados.md       retrato estatístico do público-alvo
  Guia_Operacional_G1.md             organização interna da equipe
etl_processor.py                     leitura e limpeza dos microdados do IBGE
analise_exploratoria.py              hipóteses, modelos, gráficos, indicadores
metodos_amostrais.py                 estatística com desenho amostral complexo
tests/                               testes automáticos dos métodos
outputs/
  graficos/01–06_*.png               gráficos do Dossiê
  resultados_estatisticos.(md|json)  todas as tabelas
  indicadores_grupo2.csv             indicadores prontos para o Grupo 2
data/processed/etl_relatorio.json    auditoria do ETL
```

## Como reproduzir

Requisitos: Python 3.11+ e os microdados da PNS 2019 (≈ 30 MB zipados). Instruções de download em [`docs/02`](docs/02_Aquisicao_Dados.md).

```bash
pip install -r requirements.txt
python -m pytest tests            # valida os métodos amostrais
python etl_processor.py           # lê o zip do IBGE em data/raw/ e gera a base analítica
python analise_exploratoria.py    # gera tabelas, gráficos e indicadores (~1,5 min)
```

Os microdados brutos e a base processada não são versionados: são públicos no IBGE e reprodutíveis pelos scripts.

## Ética

Pesquisa com dados públicos e anonimizados do IBGE, enquadrada nas exceções do art. 1º, parágrafo único, da Resolução CNS nº 510/2016. Não requer apreciação pelo sistema CEP/Conep. Detalhes em [`docs/04`](docs/04_Rigor_Metodologico.md).

## Licença e citação

- **Código** (`*.py`, `tests/`): [MIT](LICENSE)
- **Documentos, gráficos e indicadores** (`*.md`, `outputs/`): [CC BY 4.0](LICENSE-docs.md)
- **Como citar:** ver [`CITATION.cff`](CITATION.cff). No GitHub, use o botão "Cite this repository".
