# Dossiê de Evidências Quantitativas
### Uso excessivo de telas e saúde mental no Brasil — PNS 2019 (IBGE)

**Projeto de Extensão IESB · Grupo 1 (Problem Space) → entrega para o Grupo 2 (Solution Space)**
**Tema norteador:** Saúde Mental · **ODS 3** (Saúde e Bem-Estar) · **ODS 5** (Igualdade de Gênero), com a justificativa da seção 4.5
**Pergunta de pesquisa:** *Como o uso excessivo de tecnologias digitais influencia os níveis de ansiedade e o déficit de atenção na sociedade contemporânea?*

---

## 1. Sumário executivo

> **O que os dados provam:** não existe uma relação linear do tipo "cada hora a mais = mais sofrimento". O que existe é um **efeito de limiar (curva em J)**. Até ~3h/dia de tela de lazer, o risco é estável. **Acima de 3h/dia ele sobe, e com 6h ou mais por dia as chances de rastreio positivo para depressão são 72% maiores e as de dificuldade frequente de concentração são 62% maiores**, já descontados idade, sexo, renda, escolaridade, TV e zona rural.

| # | Evidência | Número-chave |
|---|---|---|
| 1 | **Limiar de risco em 3h/dia** | OR ajustado 6h+ vs <1h: **1,72** (depressão), **1,62** (concentração), **1,42** (diagnóstico de ansiedade/outros) |
| 2 | **O problema é jovem** | **58,8%** dos jovens de 15–17 anos e **52,2%** dos de 18–24 usam 3h+/dia (vs 5,7% dos 60+). Entre usuários jovens, **cada faixa a mais de tela aumenta em 20%** as chances de rastreio positivo |
| 3 | **Mulheres carregam o dobro da carga (ODS 5)** | PHQ-9 ≥ 10: **15,1%** das mulheres vs **6,0%** dos homens. Entre mulheres com 6h+/dia: **19,9%** |
| 4 | **Escala nacional** | **40,8 milhões** de brasileiros com 15+ anos usam 3h+/dia de tela de lazer, e **16,6 milhões** usam 6h+. Entre estes, **2,4 milhões** têm rastreio positivo para depressão |
| ⚠️ | **Correlação linear é desprezível** | Spearman tela × PHQ-9: ρ = 0,020; parcial ρ = 0,052. **Não usar** este número como "prova". A evidência está no limiar (item 1) |

---

## 2. Fonte dos dados e justificativa

**Fonte:** IBGE, *Pesquisa Nacional de Saúde 2019*, microdados do questionário individual (arquivo `PNS_2019_20220525.zip`, layout `input_PNS_2019.txt`, dicionário `dicionario_PNS_microdados_2019.xls`). Baixados diretamente de `ftp.ibge.gov.br/PNS/2019/Microdados/`.

**Por que a PNS 2019:** foram avaliadas 6 bases oficiais (detalhes em [`docs/01_Data_Discovery.md`](docs/01_Data_Discovery.md)). A PNS é a **única** base pública e oficial brasileira, com representatividade nacional, que mede no **mesmo indivíduo**:

| Dimensão | Variável | Descrição |
|---|---|---|
| Tecnologia | **P04502** | Horas/dia do tempo livre em **celular, tablet ou computador para lazer** ("redes sociais, notícias, vídeos, jogar") |
| Atenção | **N013** | Problemas para se concentrar nas atividades habituais (2 últimas semanas) |
| Saúde mental | **PHQ-9** (N010–N018) | Questionário validado internacionalmente; ≥ 10 pontos = rastreio positivo para depressão |
| Ansiedade | **Q11006** | Diagnóstico de transtorno de ansiedade, pânico, TOC ou outro transtorno mental |
| Demografia | C006, C008 | Sexo e idade |
| Inferência | V00291, V0024, UPA_PNS | Peso amostral, estrato e conglomerado |

**Validação externa:** o pipeline reproduz a prevalência oficial publicada. Obtivemos **PHQ-9 ≥ 10 = 10,78%** (IC95% 10,38–11,18), idêntico aos **10,8%** de Ciência & Saúde Coletiva (2023).

---

## 3. Metodologia de limpeza (ETL — `etl_processor.py`)

| Etapa | Registros | Regra |
|---|---:|---|
| Arquivo bruto do IBGE | 293.726 | Todos os moradores de todos os domicílios |
| Morador selecionado (V0025A = 1) | 94.114 | Só ele responde os módulos N (PHQ-9), P (telas) e Q (diagnósticos) |
| Entrevista realizada (M001 = 1) | **90.846** | Exclui recusas e moradores não encontrados (3.268) |
| Peso válido e 15+ anos | 90.846 | Nenhuma exclusão adicional |
| Casos completos (tela + PHQ-9) | **90.846** | **0 nulos** nessas variáveis para quem fez a entrevista |

**Transformações:**
1. **Layout conferido** automaticamente contra o `input_PNS_2019.txt` oficial (28/28 posições corretas).
2. **Códigos conferidos** contra o dicionário oficial. O código **9 = "Ignorado"** vira nulo (nenhuma ocorrência nas variáveis-chave). O ETL **para** se surgir código desconhecido.
3. **Escalas ordinais:**
   - Tela P04502: 6 "não usa" → **0**; 1 "<1h" → 1; … 5 "6h+" → **5**. Também há uma versão em horas (ponto médio: 0; 0,5; 1,5; 2,5; 4,5; 7).
   - PHQ-9: "nenhum dia" → 0; "menos da metade" → 1; "mais da metade" → 2; "quase todos os dias" → 3. Escore de 0 a 27.
   - Binários: PHQ-9 ≥ 10; concentração/sono/agitação "frequente" (≥ mais da metade dos dias); uso 3h+; diagnósticos Sim → 1 e Não → 0.
4. **Pesos amostrais** (V00291) em todas as prevalências. Erro-padrão por **linearização de Taylor**, com estrato e conglomerado.

---

## 4. Resultados estatísticos (`analise_exploratoria.py`)

### 4.1 Correlação linear: **desprezível**, e isso precisa ser dito

| Tela de lazer × | Spearman ρ | IC 95% | p |
|---|---:|---|---:|
| PHQ-9 (escore) | 0,020 | [0,013; 0,026] | < 0,001 |
| Concentração (N013) | 0,041 | [0,035; 0,048] | < 0,001 |
| Sono (N010) | −0,034 | [−0,040; −0,027] | < 0,001 |
| Agitação (N015) | −0,007 | [−0,013; −0,000] | 0,035 |
| Diag. ansiedade/outros (Q11006) | 0,062 | [0,055; 0,068] | < 0,001 |

Pearson (horas × PHQ-9): r ≈ 0,01. **Todas as correlações são estatisticamente significativas (n = 90 mil), mas a magnitude é desprezível** (|ρ| < 0,10). Com essa amostra, p < 0,001 não significa efeito relevante.

📊 `outputs/graficos/01_scatter_correlacao.png` · `outputs/graficos/02_heatmap_correlacoes.png`

### 4.2 Por que a correlação linear esconde o efeito

O heatmap mostra o motivo: **tempo de tela tem correlação forte com idade (ρ = −0,50) e escolaridade (ρ = +0,50)**. Isso gera dois vieses que se anulam:

| Faixa de tela | n | Idade média | % 60+ | % renda ≤ 1 SM |
|---|---:|---:|---:|---:|
| Não usa | 30.540 | 56,7 | 47,0% | 66,7% |
| < 1h | 15.597 | 47,5 | 21,0% | 49,2% |
| 1–2h | 15.590 | 41,3 | 11,3% | 43,4% |
| 2–3h | 11.032 | 36,9 | 8,3% | 44,9% |
| 3–6h | 10.920 | 32,8 | 5,8% | 46,6% |
| 6h+ | 7.167 | **28,5** | 3,5% | 55,0% |

1. **O grupo "não usa" é outro perfil populacional:** mais velho, mais pobre e com mais doença. A taxa alta de sintomas nesse grupo (11,8%) não vem da tecnologia; reflete exclusão digital e envelhecimento.
2. **A relação inverte com a idade:** entre jovens a correlação é positiva; entre idosos é ligeiramente negativa (para eles, tela pode ser conexão social).

**Com o confundimento controlado, o sinal aparece de forma consistente:**

| Análise | ρ |
|---|---:|
| Spearman parcial tela × PHQ-9 (controle: idade, sexo, escolaridade, renda) | **0,052** |
| Somente usuários (exclui "não usa"), todas as idades | 0,054 |
| Somente usuários, **15–17 anos** | **0,132** [0,088; 0,175] |
| Somente usuários, **18–24 anos** | **0,124** [0,102; 0,147] |
| Somente usuários, 25–34 | 0,083 |
| Somente usuários, 35–44 | 0,047 |
| Somente usuários, 45–59 | 0,020 |
| Somente usuários, 60+ | 0,025 |

Nos jovens a correlação passa de "desprezível" para **"fraca"** (> 0,10), e diminui conforme a idade aumenta.

### 4.3 Dose-resposta: a evidência principal (curva em J)

Regressão logística ponderada (OR ajustado; referência = < 1h/dia; EP robusto por conglomerado). Controles: sexo, faixa etária, escolaridade, renda, TV e zona rural. n = 90.824.

| Tela de lazer/dia | PHQ-9 ≥ 10 (depressão) | Concentração frequente | Diag. ansiedade/outros |
|---|---|---|---|
| Não usa | 1,22 [1,07; 1,38] | 1,37 [1,18; 1,59] | 1,00 [0,85; 1,19] |
| < 1h (ref.) | 1 | 1 | 1 |
| 1–2h | 0,92 [0,80; 1,06] | 0,88 [0,74; 1,05] | 0,91 [0,77; 1,07] |
| 2–3h | 1,00 [0,86; 1,16] | 0,95 [0,79; 1,14] | 0,97 [0,80; 1,18] |
| **3–6h** | **1,22 [1,04; 1,44]** | **1,32 [1,09; 1,59]** | **1,21 [1,01; 1,46]** |
| **6h+** | **1,72 [1,47; 2,03]** | **1,62 [1,35; 1,95]** | **1,42 [1,16; 1,75]** |

**Leitura:** até 3h/dia não há aumento de risco (os intervalos cruzam 1). **A partir de 3h o risco sobe nos três desfechos, e em 6h+ todos os intervalos ficam bem acima de 1.** É um padrão de **limiar**, consistente com a hipótese de "uso excessivo", e não com "qualquer uso faz mal".

Prevalências ponderadas (ambos os sexos), PHQ-9 ≥ 10: 1–2h = **8,9%** → 3–6h = 10,9% → 6h+ = **14,7%**.

📊 `outputs/graficos/05_dose_resposta_OR.png`

### 4.4 Gradiente etário: o problema se concentra nos jovens

| Indicador | 15–17 | 18–24 | 25–34 | 35–44 | 45–59 | 60+ |
|---|---:|---:|---:|---:|---:|---:|
| % que usa 3h+/dia | **58,8%** | **52,2%** | 36,0% | 21,0% | 11,3% | 5,7% |
| PHQ-9 ≥ 10, < 3h/dia | 8,1% | 9,3% | 8,0% | 10,1% | 11,6% | 10,6% |
| PHQ-9 ≥ 10, 3h+/dia | 11,2% | 12,8% | **12,4%** | 12,2% | 13,6% | 12,0% |

Tendência ordinal entre usuários (OR por faixa a mais de tela, ajustado):

| Grupo | OR por faixa | IC 95% | p |
|---|---:|---|---:|
| **15–24 anos** | **1,20** | [1,07; 1,35] | 0,002 |
| 25–44 anos | 1,15 | [1,09; 1,22] | < 0,001 |
| 45+ anos | 1,09 | [1,02; 1,16] | 0,012 |

**27,2%** dos jovens de 15–24 anos usam **6h ou mais por dia** (média nacional: 9,9%).

> Nota de rigor: o teste formal de interação "3h+ × jovem" não foi significativo (OR 1,08; p = 0,55). O gradiente etário é **consistente em direção** (correlações e tendências), mas não há prova estatística de que o efeito *por pessoa* seja maior nos jovens. O que é inequívoco é que **a exposição é muito maior nos jovens**, e portanto a carga populacional também.

📊 `outputs/graficos/04_barras_idade.png`

### 4.5 Gênero (ODS 5)

| Indicador | Homens | Mulheres |
|---|---:|---:|
| Uso 3h+/dia | 24,1% | 24,3% |
| PHQ-9 ≥ 10 (geral) | **6,0%** | **15,1%** |
| PHQ-9 ≥ 10 com 6h+/dia | 8,9% | **19,9%** |
| Concentração frequente com 6h+/dia | 8,0% | **13,9%** |
| OR ajustado "ser mulher" para PHQ-9 ≥ 10 | — | **2,78** [2,54; 3,04] |
| Interação tela 3h+ × sexo | — | OR 1,05 [0,85; 1,29], p = 0,67 (n.s.) |

**Conclusão para o ODS 5:**
- Homens e mulheres usam telas na mesma proporção, e o aumento de risco com o uso excessivo é **igual nos dois sexos** (interação não significativa).
- Mesmo assim, **as mulheres partem de uma carga de sofrimento 2,5 vezes maior** e chegam a ~20% de rastreio positivo no grupo de 6h+.
- **O ODS 5 se justifica pela desigualdade de carga, não por um efeito diferente da tecnologia.** Uma solução que ignore gênero deixa de alcançar o grupo mais afetado em números absolutos.

📊 `outputs/graficos/03_barras_sexo.png`

---

## 5. Veredito científico

| Afirmação | Status | Base |
|---|---|---|
| "Quanto mais tela, mais sofrimento" (linear) | ❌ **Não sustentada** | ρ < 0,06 em todas as análises |
| "Uso excessivo (≥ 3h, sobretudo 6h+) está associado a pior saúde mental e atenção" | ✅ **Sustentada** | OR 1,22–1,72, IC fora de 1, ajustado, 3 desfechos |
| "A exposição excessiva é um fenômeno jovem" | ✅ **Sustentada** | 59% dos 15–17 usam 3h+; 27% dos 15–24 usam 6h+ |
| "O efeito por pessoa é maior em jovens" | ⚠️ **Sugestiva, não provada** | Correlações maiores, mas interação n.s. |
| "Mulheres são mais afetadas" | ✅ em carga · ❌ em efeito diferencial | PHQ 15,1% vs 6,0%; interação n.s. |
| "Telas **causam** ansiedade/déficit de atenção" | ❌ **Não demonstrável com esta base** | Estudo transversal; causalidade reversa plausível |

### Pivot recomendado para a narrativa

A narrativa **"tecnologia faz mal"** não se sustenta nos dados. A narrativa que se sustenta é:

> **"O uso excessivo (acima de 3h/dia de tela de lazer) é um marcador de risco para sofrimento mental e problemas de atenção. Ele atinge principalmente os jovens, e a carga mais pesada fica com as mulheres."**

---

## 6. Implicações para o Grupo 2 (Solution Space)

1. **Limiar, não abstinência.** Os dados não apoiam soluções de "detox total": quem não usa telas também tem risco alto, por outros motivos. A meta defensável é **manter o uso abaixo de ~3h/dia de lazer**.
2. **Público prioritário: 15–24 anos.** É onde a exposição é massiva e a associação é mais clara.
3. **Desenho sensível a gênero.** Mulheres jovens com uso intenso são o grupo com maior prevalência de sintomas. A persona do Marketing deve refletir isso.
4. **Dois desfechos-alvo mensuráveis:** concentração (N013) e humor/sono (PHQ-9). Ambos podem ser autoavaliados num app com o próprio PHQ-9, que é de domínio público.
5. **Pergunta "Como poderíamos" (HMW) sugerida:** *Como poderíamos ajudar jovens que passam mais de 3 horas por dia em telas de lazer a reduzir esse tempo, de modo a proteger sua concentração e seu bem-estar emocional?*

---

## 7. Limitações (obrigatório citar)

1. **Transversal:** associação ≠ causalidade. Pessoas em sofrimento podem usar mais telas como fuga (causalidade reversa).
2. **P04502 não isola vídeos curtos.** A pergunta mistura redes sociais, notícias, vídeos e jogos. Nenhuma base oficial brasileira mede especificamente Reels/TikTok/Shorts.
3. **Dados de 2019:** antes da pandemia e da massificação do TikTok e dos Reels no Brasil. A exposição atual tende a ser maior.
4. **A PNS não tem escala de ansiedade (GAD-7).** A ansiedade foi aproximada pelo diagnóstico autorreferido Q11006, que agrupa ansiedade com outros transtornos, e por itens do PHQ-9 (agitação, sono).
5. **N013 mede dificuldade de concentração**, não diagnóstico de TDAH.
6. **Autorrelato** do tempo de tela, sujeito a viés de memória.
7. **Erro-padrão das regressões:** sanduíche por conglomerado (UPA), sem estratos. É levemente conservador; para publicação formal, confirmar com `survey::svyglm` (R).
8. **Efeito pequeno em escala individual:** o escore PHQ-9 sobe ~0,14 ponto por faixa de tela, de 0 a 27. A relevância está na **escala populacional** (16,6 milhões com 6h+).

---

## 8. Reprodutibilidade

```bash
pip install -r requirements.txt
python etl_processor.py          # ~10 s
python analise_exploratoria.py   # ~20 s
```

| Artefato | Conteúdo |
|---|---|
| `data/processed/etl_relatorio.json` | Contagem de cada filtro e distribuição bruta dos códigos |
| `outputs/resultados_estatisticos.md` / `.json` | Todas as tabelas (inclusive as não citadas aqui) |
| `outputs/graficos/01–05_*.png` | Gráficos do dossiê |

## 9. Referências

- IBGE. *Pesquisa Nacional de Saúde 2019: microdados*. Rio de Janeiro: IBGE, 2022. https://ftp.ibge.gov.br/PNS/2019/Microdados/
- Kroenke K, Spitzer RL, Williams JB. The PHQ-9: validity of a brief depression severity measure. *J Gen Intern Med*, 2001.
- *Depression screening in a population-based study: Brazilian National Health Survey 2019*. Ciência & Saúde Coletiva, 2023. https://www.scielo.br/j/csc/a/wWKFtv8ZVZZTwVDM94Q3gFt/
- Bonett DG, Wright TA. Sample size requirements for estimating Pearson, Kendall and Spearman correlations. *Psychometrika*, 2000.
- Cetic.br. *TIC Kids Online Brasil 2024* (contexto: 24% dos jovens de 9–17 anos querem reduzir o tempo online e não conseguem).
