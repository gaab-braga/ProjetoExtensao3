# Projeto de Extensão IESB — Grupo 1 · Saúde Mental e Dependência Digital

**Fase:** Problem Space (Double Diamond) · **ODS 3** (Saúde e Bem-Estar), com **ODS 5** se os dados mostrarem desigualdade de gênero.
**Pergunta:** *Como o uso excessivo de tecnologias digitais influencia os níveis de ansiedade e o déficit de atenção na sociedade contemporânea?*

## Base oficial escolhida
**IBGE — Pesquisa Nacional de Saúde 2019 (microdados).** A justificativa e as colunas exatas estão em [`docs/01_Data_Discovery.md`](docs/01_Data_Discovery.md).

## Pipeline

| Passo | Arquivo | Status |
|---|---|---|
| 1. Data Discovery | `docs/01_Data_Discovery.md` | ✅ concluído |
| 2. Aquisição | `docs/02_Aquisicao_Dados.md` | ⛔ aguardando download manual dos microdados do IBGE |
| 3. ETL | `etl_processor.py` | ✅ pronto e testado (layout de posição fixa do IBGE) |
| 4. Análise estatística | `analise_exploratoria.py` | ✅ pronto e testado |
| 5. Dossiê | `Dossie_Evidencias_Quantitativas.md` + `outputs/graficos/*.png` | ⏳ será gerado com os dados reais |

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
