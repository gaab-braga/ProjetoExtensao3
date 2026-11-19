# Anexo B — Obtenção e Preparação dos Dados

**Projeto de Extensão IESB · Trilha de Pesquisa · Saúde Mental** · [← Relatório Final](../RELATORIO_FINAL_DA_PESQUISA.md)

Este anexo descreve, passo a passo, como os dados foram obtidos, preparados e analisados, de forma que **qualquer pessoa consiga replicar o estudo**.

---

## 1. Fonte oficial

| Item | Detalhe |
|---|---|
| Pesquisa | IBGE — Pesquisa Nacional de Saúde 2019 (PNS), em parceria com o Ministério da Saúde |
| Endereço | https://ftp.ibge.gov.br/PNS/2019/Microdados/ |
| Microdados | `Dados/PNS_2019_20220525.zip` (29,5 MB; 455 MB descompactado; 293.726 registros de posição fixa) |
| Documentação | `Documentacao/Dicionario_e_input_20220530.zip` → `dicionario_PNS_microdados_2019.xls` e `input_PNS_2019.txt` (layout das colunas) |
| Integridade | SHA-256 do zip registrado em [`resultados/tabelas/relatorio_preparacao_dos_dados.json`](../resultados/tabelas/relatorio_preparacao_dos_dados.json) |

Os microdados **não são redistribuídos** neste repositório: eles são públicos no IBGE e o pipeline os lê diretamente da pasta `dados/brutos/`.

## 2. Procedimento replicável

### Etapa 1 — Baixar os dados
1. Baixar os dois arquivos acima no site oficial do IBGE.
2. Extrair `input_PNS_2019.txt` do zip de documentação.
3. Colocar `PNS_2019_20220525.zip` (pode ficar zipado) e `input_PNS_2019.txt` em `dados/brutos/`.

### Etapa 2 — Preparar os dados (`codigo/preparacao_dos_dados.py`)
1. Ler o arquivo de posição fixa e **conferir automaticamente** a posição das 32 variáveis usadas contra o `input_PNS_2019.txt` oficial. Qualquer divergência interrompe a execução.
2. Conferir cada código de resposta contra o dicionário oficial. Respostas "ignorado" (código 9) viram dado ausente; um código desconhecido interrompe a execução.
3. Aplicar os critérios de inclusão: morador selecionado para a entrevista individual (V0025A = 1), entrevista realizada (M001 = 1), peso válido e 15 anos ou mais.
4. Transformar as respostas em escalas: tempo de tela de 0 (não usa) a 5 (6h ou mais); itens do PHQ-9 de 0 a 3, com escore total de 0 a 27.
5. Criar os indicadores: rastreio positivo (PHQ-9 ≥ 10), PHQ-9 pelo algoritmo diagnóstico, dificuldade de concentração frequente, uso de 3h+ e 6h+.

| Etapa da preparação | Registros |
|---|---:|
| Registros no arquivo do IBGE | 293.726 |
| Moradores selecionados para a entrevista individual | 94.114 |
| Entrevistas realizadas (amostra final) | **90.846** |
| Excluídos (recusa ou morador não encontrado) | 3.268 |
| Casos sem tempo de tela ou PHQ-9 | 0 |

### Etapa 3 — Validar
Comparar a prevalência calculada com a publicada para a mesma base (MELO et al., 2023): **10,78%** de rastreio positivo para depressão (publicado: 10,8%) e **5,63%** pelo algoritmo do PHQ-9 (publicado: 5,7%).

### Etapa 4 — Analisar (`codigo/analise_estatistica.py`)
1. Prevalências ponderadas pelos pesos do IBGE, com intervalos de confiança que respeitam o desenho amostral (estrato e conglomerado; funções em `codigo/metodos_amostrais.py`).
2. Correlações descritivas (Spearman e Pearson).
3. Razões de prevalência por faixa de tempo de tela (regressão de Poisson), ajustadas por sexo, idade, escolaridade, renda, TV e zona rural.
4. Testes da hipótese principal (tendência), do limiar e das diferenças por sexo e idade, com correção para múltiplas comparações.
5. Robustez: a análise é repetida de 144 formas diferentes (*specification curve*).
6. Saídas: figuras em `resultados/figuras/` e tabelas em `resultados/tabelas/`.

## 3. Como rodar

Requisitos: Python 3.11 ou superior.

```bash
pip install -r codigo/requirements.txt
python -m pytest codigo/testes          # valida os métodos estatísticos
python codigo/preparacao_dos_dados.py   # ~10 s
python codigo/analise_estatistica.py    # ~1,5 min
```

Os resultados gerados são idênticos aos publicados em `resultados/`.

## 4. Ética
Dados públicos e anonimizados, sem contato com participantes. A pesquisa enquadra-se nas exceções do art. 1º, parágrafo único, da Resolução CNS nº 510/2016 e não requer apreciação pelo sistema CEP/Conep.

**Referência:** MELO, A. P. S. et al. Depression screening in a population-based study: Brazilian National Health Survey 2019. *Ciência & Saúde Coletiva*, v. 28, n. 4, p. 1163-1174, 2023.
