# Projeto de Extensão IESB — Grupo 1 · Saúde Mental e Dependência Digital

**Fase:** Problem Space (Double Diamond) · **ODS 3** (Saúde e Bem-Estar), com **ODS 5** se os dados mostrarem desigualdade de gênero.
**Pergunta:** *Como o uso intenso de telas para lazer — que inclui redes sociais e vídeos curtos — influencia os níveis de ansiedade e o déficit de atenção na sociedade contemporânea?*

## Base oficial escolhida
**IBGE — Pesquisa Nacional de Saúde 2019 (microdados).** A justificativa e as colunas exatas estão em [`docs/01_Data_Discovery.md`](docs/01_Data_Discovery.md).

## Pipeline

| Passo | Arquivo | Status |
|---|---|---|
| 1. Data Discovery | `docs/01_Data_Discovery.md` | ✅ concluído |
| 2. Aquisição | `docs/02_Aquisicao_Dados.md` | ✅ baixado do FTP oficial do IBGE |
| 3. ETL | `etl_processor.py` | ✅ 90.846 respondentes; layout e códigos conferidos com o dicionário oficial |
| 4. Análise estatística | `analise_exploratoria.py` | ✅ correlações, confundidores, regressões, gráficos |
| 5. Dossiê | [`Dossie_Evidencias_Quantitativas.md`](Dossie_Evidencias_Quantitativas.md) + `outputs/graficos/*.png` | ✅ entregue |
| Standup | [`docs/03_Guia_Standup.md`](docs/03_Guia_Standup.md) | ✅ roteiro e papel de cada arquivo |
| Equipe | [`docs/Guia_Operacional_G1.md`](docs/Guia_Operacional_G1.md) | ✅ guia operacional atualizado com os resultados |

## Principal achado
A correlação linear é desprezível (ρ = 0,02), mas existe um **limiar**: acima de 3h/dia de tela de lazer o risco sobe, e com **6h+/dia** as chances são **72% maiores para depressão (PHQ-9 ≥ 10)** e **62% maiores para dificuldade de concentração** (ajustado). **59%** dos adolescentes de 15–17 anos usam 3h+/dia, e as mulheres têm 2,5× mais sintomas (ODS 5).

## Como rodar
```bash
pip install -r requirements.txt
# coloque PNS_2019_*.zip e input_PNS_2019.txt em data/raw/ (ver docs/02)
python etl_processor.py          # -> data/processed/pns2019_telas_saude_mental.csv + etl_relatorio.json
python analise_exploratoria.py   # -> outputs/graficos/*.png + outputs/resultados_estatisticos.(md|json)
```

## Estrutura
```
etl_processor.py            leitura do arquivo de posição fixa, filtros, recodificação ordinal, PHQ-9
analise_exploratoria.py     Spearman/Pearson, correlação parcial, prevalências com desenho amostral, regressões, gráficos
docs/                       Data Discovery e instruções de aquisição
data/raw/                   microdados do IBGE (não versionados)
data/processed/             base analítica + relatório do ETL
outputs/graficos/           01_scatter, 02_heatmap, 03_barras_sexo, 04_barras_idade
```
