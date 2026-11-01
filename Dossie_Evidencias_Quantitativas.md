# Dossiê de Evidências Quantitativas
### Uso intenso de telas e saúde mental no Brasil — PNS 2019 (IBGE)

**Projeto de Extensão IESB · Grupo 1 (Problem Space) → entrega para o Grupo 2 (Solution Space)**
**Tema norteador:** Saúde Mental · **ODS 3** (Saúde e Bem-Estar) · **ODS 5** (Igualdade de Gênero), justificado na seção 4.5
**Pergunta de pesquisa:** *Como o uso intenso de telas para lazer — que inclui redes sociais e vídeos curtos — influencia a saúde mental, em especial a ansiedade e os sintomas depressivos, e o déficit de atenção na sociedade contemporânea?*
**Versão 2 (01/11/2026):** revisão metodológica completa. Mudanças e justificativas em [`docs/04_Rigor_Metodologico.md`](docs/04_Rigor_Metodologico.md).

---

## 1. Sumário executivo

> **O que os dados mostram:** não existe uma relação do tipo "cada hora a mais = mais sofrimento". Até ~3h/dia de tela de lazer, a prevalência de sintomas é estável. **Acima disso ela sobe**: com **6h ou mais por dia**, a prevalência de rastreio positivo para depressão é **59% maior** e a de dificuldade frequente de concentração é **55% maior** que entre quem usa menos de 1h. As estimativas já descontam idade, sexo, renda, escolaridade, TV e zona rural. A direção desse resultado se manteve em **todos os 144 modelos alternativos** testados.

| # | Evidência | Número-chave | Força |
|---|---|---|---|
| 1 | **Dose-resposta entre usuários (hipótese primária)** | +12% de prevalência por faixa de tela: RP 1,12 [1,08; 1,16] | 🟢 Forte |
| 2 | **Padrão em J (limiar ~3h)** | Sem diferença abaixo de 3h (p = 0,46); 3–6h: RP 1,19; **6h+: RP 1,59** [1,39; 1,83] | 🟢 Forte no formato · 🟡 o ponto exato de 3h é exploratório |
| 3 | **Concentração (déficit de atenção)** | 6h+: RP 1,55 [1,31; 1,83] | 🟡 Moderada (medida por um único item) |
| 4 | **Ansiedade (diagnóstico)** | 6h+: RP 1,38 [1,14; 1,66]; 3–6h não sobrevive à correção de multiplicidade | 🟠 Fraca a moderada (medida ampla) |
| 5 | **Exposição concentrada nos jovens** | **58,8%** dos jovens de 15–17 anos usam 3h+/dia e **31,9%** usam 6h+ (60+: 5,7% e 1,7%) | 🟢 Forte (descritivo) |
| 6 | **Mulheres: carga 2,5× maior (ODS 5)** | PHQ-9 ≥ 10: **15,1%** vs **6,0%**. O uso de 3h+ soma +4,4 p.p. nas mulheres e +2,5 p.p. nos homens | 🟢 carga · 🟡 excesso absoluto maior é **sugestivo** (p = 0,052) |
| 7 | **Escala nacional** | **40,8 milhões** usam 3h+/dia; **16,6 milhões** usam 6h+, dos quais **2,4 milhões** têm rastreio positivo | 🟢 Descritivo |
| ⚠️ | **Correlação linear** | Spearman ρ = 0,02. **Não usar como prova**: a relação não é linear | — |

---

## 2. Fonte dos dados e justificativa

**Fonte:** IBGE, *Pesquisa Nacional de Saúde 2019*, microdados (`PNS_2019_20220525.zip`, SHA-256 `a789f6b0…be6057`), baixados do FTP oficial. A metodologia da pesquisa está em Stopa et al. (2020).

**Por que a PNS 2019:** foram avaliadas 6 bases oficiais ([`docs/01_Data_Discovery.md`](docs/01_Data_Discovery.md)). A PNS é a única base pública e oficial, com representatividade nacional, que mede no mesmo indivíduo:

| Dimensão | Variável | Descrição |
|---|---|---|
| Tecnologia | **P04502** | Horas/dia do tempo livre em celular, tablet ou computador para lazer ("redes sociais, notícias, vídeos, jogar") |
| Atenção | **N013** | Dificuldade de concentração nas atividades habituais (2 últimas semanas) |
| Saúde mental | **PHQ-9** (N010–N018) | Escala validada no Brasil (Santos et al., 2013); ≥ 10 = rastreio positivo |
| Ansiedade | **Q11006** | Diagnóstico autorreferido de transtorno de ansiedade, pânico, TOC ou outro |
| Demografia | C006, C008 | Sexo e idade |
| Desenho amostral | V00291, V0024, UPA_PNS | Peso, estrato e conglomerado |

**Validação externa:** o pipeline reproduz as **duas** prevalências publicadas por Melo et al. (2023): PHQ-9 ≥ 10 = **10,78%** (publicado: 10,8%) e PHQ-9 por algoritmo = **5,63%** (publicado: 5,7%).

**Ética:** dados públicos e anonimizados. A pesquisa enquadra-se nas exceções do art. 1º, parágrafo único, da Resolução CNS nº 510/2016 (informações de acesso e domínio público), e não requer apreciação pelo sistema CEP/Conep. Confirmar com o CEP do IESB em caso de submissão formal.

---

## 3. Metodologia

### 3.1 Limpeza (ETL — `etl_processor.py`)

| Etapa | Registros | Regra |
|---|---:|---|
| Arquivo bruto do IBGE | 293.726 | Todos os moradores |
| Morador selecionado (V0025A = 1) | 94.114 | Só ele responde os módulos N, P e Q |
| Entrevista realizada (M001 = 1) | **90.846** | Exclui 3.268 recusas ou não encontrados |
| Casos completos (tela + PHQ-9) | **90.846** | 0 nulos nessas variáveis. Covariáveis: 22 sem renda e 10 sem cor/raça (casos completos) |

Layout conferido automaticamente contra o input oficial do IBGE. Códigos validados contra o dicionário, com 9 = "ignorado" convertido em nulo. Escalas ordinais: tela 0–5 (0 = não usa) e PHQ-9 0–3 por item.

### 3.2 Análise (`analise_exploratoria.py` + `metodos_amostrais.py`)

| Elemento | Escolha | Por quê |
|---|---|---|
| Medida de efeito | **Razão de prevalência (RP)**, Poisson com variância robusta | O OR superestima o efeito com desfecho comum, como aqui (~11%) (Barros & Hirakata, 2003) |
| Inferência | **Desenho completo** (estrato + 8.027 UPAs + peso), linearização de Taylor, subgrupos como domínio | Ignorar o desenho subestima os erros-padrão (Lumley, 2004) |
| Confundidores | Escolhidos por DAG: sexo, idade, escolaridade, renda, TV, zona; estendido: + estado civil, ocupação, região. **Sono não** (mediador) | `docs/04` §7 |
| Hipóteses | 1 primária; secundárias com **FDR** (Benjamini-Hochberg); limiar declarado como **exploratório** | Evita falsos positivos e "forking paths" |
| Interação | Escalas **multiplicativa e aditiva** (RERI) | Knol & VanderWeele (2012) |
| Robustez | E-value; **specification curve** com 144 modelos | VanderWeele & Ding (2017); Simonsohn et al. (2020) |
| Correlações | Spearman/Pearson como **descritivas** | Exposição categórica e relação não linear |

---

## 4. Resultados

### 4.1 Correlação linear: desprezível (descritivo)

| Tela de lazer × | Spearman ρ | IC 95% |
|---|---:|---|
| PHQ-9 (escore) | 0,020 | [0,013; 0,026] |
| Concentração (N013) | 0,041 | [0,035; 0,048] |
| Diag. ansiedade/outros | 0,062 | [0,055; 0,068] |
| PHQ-9, parcial (controle: idade, sexo, escolaridade, renda) | 0,052 | [0,045; 0,058] |

A correlação é desprezível porque a relação **não é linear** (4.3) e porque o tempo de tela tem forte correlação com idade (ρ = −0,50). Os dois grupos com mais sintomas, os que **não usam** (mais velhos e mais pobres) e os que usam **6h+** (mais jovens), ficam em extremos opostos e "anulam" a reta.

📊 `outputs/graficos/01_scatter_correlacao.png` · `02_heatmap_correlacoes.png`

### 4.2 Perfil de cada faixa de tela

| Faixa | n | Idade média | % 60+ | % renda ≤ 1 SM | PHQ-9 ≥ 10 |
|---|---:|---:|---:|---:|---:|
| Não usa | 30.540 | 56,7 | 47,0% | 66,7% | 11,8% |
| < 1h | 15.597 | 47,5 | 21,0% | 49,2% | 10,2% |
| 1–2h | 15.590 | 41,3 | 11,3% | 43,4% | 8,9% |
| 2–3h | 11.032 | 36,9 | 8,3% | 44,9% | 9,3% |
| 3–6h | 10.920 | 32,8 | 5,8% | 46,6% | 10,9% |
| 6h+ | 7.167 | 28,5 | 3,5% | 55,0% | **14,7%** |

### 4.3 Dose-resposta: evidência principal

RP ajustada (referência: < 1h/dia), Poisson com desenho amostral completo, n = 90.824:

| Tela de lazer/dia | PHQ-9 ≥ 10 (primário) | Concentração frequente | Diag. ansiedade/outros |
|---|---|---|---|
| Não usa | 1,18 [1,06; 1,32] | 1,33 [1,16; 1,53] | 1,00 [0,85; 1,18] |
| < 1h (ref.) | 1 | 1 | 1 |
| 1–2h | 0,93 [0,82; 1,05] | 0,89 [0,75; 1,05] | 0,92 [0,78; 1,07] |
| 2–3h | 1,00 [0,87; 1,14] | 0,95 [0,81; 1,13] | 0,97 [0,81; 1,17] |
| **3–6h** | **1,19 [1,03; 1,37]** | **1,29 [1,08; 1,53]** | 1,19 [1,01; 1,41] (q = 0,07) |
| **6h+** | **1,59 [1,39; 1,83]** | **1,55 [1,31; 1,83]** | **1,38 [1,14; 1,66]** |

| Teste formal (PHQ-9 ≥ 10) | Resultado |
|---|---|
| **H1: tendência entre usuários** | **RP 1,12 por faixa [1,08; 1,16], p < 0,001** |
| Não linearidade | χ² = 22,7 (3 gl), p < 0,001 |
| Abaixo de 3h (1–2h e 2–3h = <1h?) | p = 0,46: sem diferença |
| Acima de 3h (3–6h e 6h+ = <1h?) | p < 0,001: diferença |
| Modelo bruto → ajustado → estendido (6h+) | 1,45 → 1,59 → 1,54 |

**Leitura:** até 3h/dia não há aumento. Acima de 3h a prevalência sobe nos três desfechos, e em 6h+ todos os intervalos ficam acima de 1. Isso é compatível com a "hipótese Goldilocks" (Przybylski & Weinstein, 2017): o uso moderado não está associado a prejuízo, e o uso intenso está.

O grupo "não usa" também tem RP elevada para depressão e concentração. Isso é atribuível ao seu perfil (seção 4.2), **não é argumento a favor de abstinência digital**, e na literatura aparece como associação em U (Werneck et al., 2018).

📊 `outputs/graficos/05_dose_resposta_RP.png`

### 4.4 Idade: a exposição é jovem, o efeito é igual

| Indicador | 15–17 | 18–24 | 25–34 | 35–44 | 45–59 | 60+ |
|---|---:|---:|---:|---:|---:|---:|
| % que usa 3h+/dia | **58,8%** | **52,2%** | 36,0% | 21,0% | 11,3% | 5,7% |
| % que usa 6h+/dia | **31,9%** | **25,3%** | 13,5% | 6,9% | 3,4% | 1,7% |

Teste de interação (usuários, 3h+ vs <3h): RP de 1,40 nos jovens de 15–24 e de 1,34 nos de 25+. Interação multiplicativa p = 0,75; aditiva p = 0,85.

> ⚠️ **Correção em relação à v1:** a v1 afirmava que o efeito era "+20% maior nos jovens". O teste formal **não sustenta** isso. A afirmação correta é: **o efeito por pessoa é semelhante em todas as idades, mas a exposição é muito maior nos jovens**, e por isso a carga populacional se concentra neles.

📊 `outputs/graficos/04_barras_idade.png`

### 4.5 Gênero (ODS 5)

| Indicador | Homens | Mulheres |
|---|---:|---:|
| Uso 3h+/dia | 24,1% | 24,3% |
| PHQ-9 ≥ 10 (geral) | **6,0%** | **15,1%** |
| PHQ-9 ≥ 10 com 6h+/dia | 8,9% | **19,9%** |
| Concentração frequente com 6h+/dia | 8,0% | **13,9%** |
| RP ajustada mulher vs homem (PHQ-9 ≥ 10) | — | **2,49** [2,29; 2,71] |
| RP de 3h+ (usuários) | 1,49 [1,22; 1,81] | 1,35 [1,22; 1,49] |
| **Excesso absoluto de 3h+** | **+2,5 p.p.** [1,2; 3,8] | **+4,4 p.p.** [2,8; 6,0] |

- **Escala relativa:** efeito semelhante (interação 0,91, p = 0,37).
- **Escala absoluta:** o uso intenso soma **quase o dobro de casos por 100 pessoas nas mulheres**. A diferença tem RERI = 0,48 [0,07; 0,88], mas o teste direto fica no limite (p = 0,052; q = 0,07). É **sugestivo, não comprovado**.

**Conclusão para o ODS 5:** homens e mulheres usam telas na mesma proporção, mas as mulheres carregam uma carga de sofrimento 2,5 vezes maior. Há indício de que o uso intenso **acrescenta mais casos** entre elas. O ODS 5 se justifica pela **desigualdade de carga**, e a hipótese de maior excesso absoluto merece replicação.

📊 `outputs/graficos/03_barras_sexo.png`

### 4.6 Robustez

| Análise | Resultado |
|---|---|
| **Specification curve** (144 modelos: 4 desfechos × 3 exposições × 3 conjuntos de covariáveis × 2 amostras × com/sem peso) | **144/144 com RP > 1 e IC acima de 1**; mediana 1,38 (1,18 a 1,89) |
| E-value (6h+, PHQ-9 ≥ 10) | 2,56 (IC: 2,12). Um confundidor oculto precisaria ter RP ≥ 2,1 com a tela **e** com o desfecho para anular o resultado |
| Fração atribuível populacional (3h+) | 7,3%, **hipotética** (só vale se a relação for causal) |

📊 `outputs/graficos/06_specification_curve.png`

---

## 5. Veredito científico

| Afirmação | Status | Base |
|---|---|---|
| "Quanto mais tela, pior" (linear) | ❌ Não sustentada | ρ = 0,02; não linearidade p < 0,001 |
| "Entre usuários, mais tela associa-se a mais sintomas depressivos" | ✅ **Sustentada (hipótese primária)** | RP 1,12/faixa; 144/144 especificações |
| "O risco aparece acima de ~3h/dia" | ✅ no formato · ⚠️ ponto exato exploratório | Wald abaixo de 3h p = 0,46; acima p < 0,001 |
| "Uso intenso associa-se a dificuldade de concentração" | ✅ Sustentada (medida limitada) | RP 1,55 em 6h+, q < 0,001 |
| "Uso intenso associa-se a ansiedade" | 🟡 Parcial | 6h+ sim (q = 0,002); 3–6h não após FDR; medida ampla |
| "A exposição intensa é um fenômeno jovem" | ✅ Sustentada | 59% dos 15–17 usam 3h+ |
| "O efeito por pessoa é maior nos jovens" | ❌ **Não sustentada** (corrigido) | Interação p = 0,75 |
| "Mulheres carregam mais sofrimento" | ✅ Sustentada | RP 2,49 |
| "O uso intenso soma mais casos entre mulheres" | 🟡 Sugestiva | RERI p = 0,02; diferença direta p = 0,052 |
| "Telas **causam** ansiedade ou depressão" | ❌ Não demonstrável | Transversal; causalidade reversa plausível |

### Narrativa defensável

> **"Entre brasileiros que usam telas no lazer, o uso acima de ~3 horas por dia, e sobretudo acima de 6 horas, está associado a mais sintomas depressivos e a mais dificuldade de concentração. Esse padrão resiste a 144 formas diferentes de analisar os dados. O uso intenso é um fenômeno jovem, e as mulheres carregam o dobro da carga de sofrimento."**

---

## 6. Para o Grupo 2 (Solution Space)

1. **Meta de limiar, não abstinência.** Os dados não mostram prejuízo até ~3h/dia, e quem não usa nada também tem mais sintomas. A meta defensável é **manter o lazer em telas abaixo de ~3h/dia**, com atenção especial a quem passa de 6h.
2. **Público prioritário: 15 a 24 anos.** O efeito por pessoa é o mesmo, mas é ali que está a exposição: 1 em cada 3 adolescentes usa 6h+.
3. **Desenho sensível a gênero.** Mulheres jovens com uso intenso formam o grupo de maior prevalência (~20%).
4. **Desfechos mensuráveis:** concentração e humor. O PHQ-9 é de domínio público e serve para autoavaliação no app.
5. **Pergunta "Como poderíamos":** *Como poderíamos ajudar jovens que passam mais de 3 horas por dia em telas de lazer a reduzir esse tempo, de modo a proteger sua concentração e seu bem-estar emocional?*
6. **O que a solução não pode prometer:** "curar ansiedade" ou "evitar depressão". Os dados mostram associação, não causa.

---

## 7. Limitações

1. **Transversal:** associação ≠ causalidade; causalidade reversa plausível (sofrimento → fuga para a tela).
2. **P04502 não isola vídeos curtos**: mistura redes sociais, notícias, vídeos e jogos.
3. **Tempo ≠ dependência:** a PNS mede horas, não uso compulsivo.
4. **Ansiedade mal medida:** Q11006 agrupa transtornos e depende de acesso a diagnóstico. Não há GAD-7.
5. **N013 é um único item** e é um sintoma depressivo, não um diagnóstico de TDAH.
6. **Dados de 2019**, pré-pandemia e pré-massificação de vídeos curtos.
7. **Limiar de 3h exploratório**: surgiu da inspeção dos dados.
8. **Efeito individual pequeno, relevância populacional:** o excesso é de alguns pontos percentuais por pessoa, mas atinge 16,6 milhões de pessoas com 6h+.

Detalhamento: [`docs/04_Rigor_Metodologico.md`](docs/04_Rigor_Metodologico.md) §8 · Perguntas abertas: [`docs/05_Agenda_de_Pesquisa.md`](docs/05_Agenda_de_Pesquisa.md)

---

## 8. Reprodutibilidade

```bash
pip install -r requirements.txt
python -m pytest tests          # valida métodos amostrais e recodificações
python etl_processor.py         # ~10 s
python analise_exploratoria.py  # ~1,5 min (inclui 144 modelos)
```

| Artefato | Conteúdo |
|---|---|
| `data/processed/etl_relatorio.json` | Contagens de cada filtro, distribuição dos códigos, SHA-256 do dado bruto |
| `outputs/resultados_estatisticos.md` / `.json` | Todas as tabelas, incluindo as 144 especificações |
| `outputs/graficos/01–06_*.png` | Gráficos do Dossiê |

## 9. Referências

Lista completa e verificada em [`docs/05_Agenda_de_Pesquisa.md`](docs/05_Agenda_de_Pesquisa.md#referências-todas-verificadas). Principais: Barros & Hirakata (2003); Knol & VanderWeele (2012); Lumley (2004); Melo et al. (2023); Orben & Przybylski (2019); Przybylski & Weinstein (2017); Santos et al. (2013); Simonsohn, Simmons & Nelson (2020); Stopa et al. (2020); VanderWeele & Ding (2017); von Elm et al. (2007); Werneck et al. (2018).
