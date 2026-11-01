# Passo 1 — Data Discovery (mapeamento de metadados e dicionários)

**Projeto de Extensão IESB · Grupo 1 (Problem Space) · ODS 3 (+ ODS 5 condicional)**
**Pergunta:** *Como o uso intenso de telas para lazer — que inclui redes sociais e vídeos curtos — influencia os níveis de ansiedade e o déficit de atenção na sociedade contemporânea?*

---

## 1. Veredito

| | |
|---|---|
| **Base escolhida** | **IBGE — Pesquisa Nacional de Saúde (PNS) 2019**, microdados do questionário individual |
| **Por quê** | É a única base **oficial brasileira, de representatividade nacional**, que traz no **mesmo respondente**: (a) tempo de tela de lazer em **celular/tablet/computador, explicitamente incluindo redes sociais e vídeos**, (b) um **instrumento clínico validado** de saúde mental (PHQ-9), com um item específico de **dificuldade de concentração**, (c) diagnósticos autorreferidos de **depressão e transtorno de ansiedade/outros**, (d) **sexo e idade** e (e) **pesos amostrais** para inferência populacional. |
| **Tamanho** | ~94 mil moradores selecionados (15+ anos) com entrevista individual; ~88 mil de 18+ anos analisáveis segundo a literatura (Scielo, 2023). |
| **Público** | Pessoas de 15 anos ou mais, em todas as UFs, área urbana e rural. |

## 2. Fontes avaliadas

| Fonte | Tem tela/redes? | Tem saúde mental? | Mesmo indivíduo? | Decisão |
|---|---|---|---|---|
| **PNS 2019 (IBGE)** | ✅ P04502 (celular/tablet/PC para lazer: "redes sociais, notícias, vídeos, jogar") + P04501 (TV) | ✅ PHQ-9 completo (N010–N018), diagnósticos Q092 e Q11006 | ✅ | **ESCOLHIDA** |
| **PeNSE 2019 (IBGE)** | ✅ tempo diário em redes sociais, tempo de tela | ✅ módulo novo de saúde mental (tristeza, irritação, preocupação, "a vida não vale a pena", sono) | ✅ | **Plano B (pivot)**: só escolares de 13–17 anos e itens não validados como escala clínica. Códigos das colunas não puderam ser verificados nesta sessão (FTP do IBGE bloqueado). |
| **TIC Kids Online Brasil (Cetic.br)** | ✅ uso intenso de internet; em 2024, 24% de 9–17 anos "gostariam de passar menos tempo conectados, mas não conseguem" | ⚠️ só indicadores de uso excessivo e experiências online (ofensas, discriminação); **sem escala de ansiedade ou atenção** | ✅ | Usar como **contexto** no Dossiê (prevalência de uso compulsivo), não como base de correlação. |
| **TIC Domicílios (Cetic.br)** | ✅ | ❌ | — | Descartada: não mede saúde mental. |
| **TIC Saúde (Cetic.br)** | ❌ (mede digitalização de estabelecimentos de saúde) | ❌ | — | Descartada: a unidade de análise são estabelecimentos e profissionais, não pessoas. |
| **DATASUS (SIA/RAAS-Psicossocial)** | ❌ | ✅ atendimentos por CID F40/F41 (ansiedade) e F90 (TDAH) | ❌ | Descartada para correlação (sem exposição a telas); útil como **série temporal de contexto**, como fez a Folha de S.Paulo ("Geração Ansiosa" no Brasil). |

## 3. Colunas exatas selecionadas (layout oficial PNS 2019, versão 20220525)

Posições conferidas com o layout publicado pelo IBGE (reproduzido em `datazoompuc/datazoom_social_Stata/PNS/dct/pns2019.dct` e no `schema.yml` da Base dos Dados). O `etl_processor.py` volta a conferir tudo contra o `input_PNS_2019.txt` oficial quando ele estiver em `data/raw/`.

### 3.1 Feature — tecnologia (Módulo P, estilo de vida)

| Código | Pos. | Pergunta (texto oficial) | Codificação → escala do ETL |
|---|---|---|---|
| **P04502** | 706 | "Em um dia, quantas horas do seu tempo livre (excluindo o trabalho), o(a) Sr(a) costuma usar computador, tablet ou celular para lazer, tais como: **utilizar redes sociais, para ver notícias, vídeos, jogar** etc?" | 1 <1h · 2 1–2h · 3 2–3h · 4 3–6h · 5 6h+ · 6 não usa → **ordinal 0–5** (0 = não usa) e horas aproximadas (ponto médio) |
| P04501 | 705 | "Em média, quantas horas por dia o(a) Sr(a) costuma ficar assistindo televisão?" | mesma escala; usada como **controle** (tela passiva × tela interativa) |

### 3.2 Targets — saúde mental (Módulo N = PHQ-9, últimas 2 semanas)

Respostas: 1 nenhum dia · 2 menos da metade dos dias · 3 mais da metade dos dias · 4 quase todos os dias → **0–3**.

| Código | Pos. | Item | Papel na pergunta de pesquisa |
|---|---|---|---|
| N010 | 564 | Problemas no sono | Sono |
| N011 | 565 | Cansaço / pouca energia | — |
| N012 | 566 | Pouco interesse ou prazer | — |
| **N013** | 567 | **Problemas para se concentrar nas atividades habituais** | **Proxy direto de déficit de atenção** |
| N014 | 568 | Problemas de alimentação | — |
| **N015** | 569 | **Lentidão ou muita agitação/inquietação** | Componente ansioso/psicomotor |
| N016 | 570 | Sentiu-se deprimido, "pra baixo", sem perspectiva | Humor |
| N017 | 571 | Sentiu-se mal consigo mesmo / fracasso | — |
| N018 | 572 | Pensou em se ferir / melhor estar morto | — |
| **PHQ-9 escore** | derivado | Soma 0–27; **≥ 10 = rastreio positivo para depressão** (ponto de corte validado) | Desfecho principal |
| Q092 | 986 | Diagnóstico de depressão por médico ou profissional de saúde mental | Desfecho clínico |
| **Q11006** | 1007 | Diagnóstico de **outra doença mental, como transtorno de ansiedade**, pânico, TOC, bipolar etc. | Desfecho clínico, proxy de **ansiedade** |

### 3.3 Demografia (ODS 5) e controles

| Código | Pos. | Conteúdo |
|---|---|---|
| **C006** | 108 | Sexo (1 homem, 2 mulher) |
| **C008** | 117 | Idade (anos) |
| C009 | 120 | Cor ou raça |
| VDD004A | 1514 | Escolaridade (1–7) |
| VDF004 | 1535 | Faixa de renda domiciliar per capita |
| A01901 | 81 | Acesso à internet no domicílio |
| V0026 | 31 | Urbano/rural |

### 3.4 Desenho amostral e filtros

| Código | Pos. | Uso |
|---|---|---|
| V0025A | 33 | = 1 → morador selecionado para o questionário individual |
| M001 | 527 | = 1 → entrevista individual realizada |
| V00291 | 1426 | **Peso do morador selecionado com calibração** (todas as estimativas populacionais) |
| V0024 / UPA_PNS | 3 / 10 | Estrato e conglomerado, para erros-padrão corretos |

## 4. Limitações conhecidas (precisam constar no Dossiê)

1. **Não existe escala de ansiedade validada (GAD-7) na PNS 2019.** A ansiedade é medida por (a) diagnóstico autorreferido Q11006, que agrupa ansiedade com outros transtornos, e (b) itens do PHQ-9 de agitação (N015), sono (N010) e concentração (N013). O PHQ-9 é, a rigor, um instrumento de **depressão**.
2. **P04502 não isola "conteúdo curto".** A pergunta soma redes sociais, notícias, vídeos e jogos. Nenhuma base oficial brasileira mede especificamente consumo de vídeos curtos (Reels/TikTok/Shorts). Isso precisa ser dito ao Grupo 2.
3. **Coleta em 2019**, antes da explosão do TikTok e dos Reels no Brasil (2020–2021) e da pandemia. É provável que os números atuais de exposição sejam maiores.
4. **Estudo transversal:** o desenho prova **associação**, não **causalidade**. A causalidade reversa é plausível: pessoas ansiosas ou deprimidas podem usar mais telas como fuga.
5. **N013 mede dificuldade de concentração** nas últimas duas semanas, não diagnóstico de TDAH.

## 5. Fontes consultadas

- IBGE — PNS 2019, layout de microdados (via [datazoompuc/datazoom_social_Stata](https://github.com/datazoompuc/datazoom_social_Stata/blob/master/PNS/dct/pns2019.dct)) e dicionário (via [basedosdados/pipelines · br_ms_pns/schema.yml](https://github.com/basedosdados/pipelines/blob/main/models/br_ms_pns/schema.yml)).
- [Questionário oficial PNS 2019 (Fiocruz/IBGE)](https://www.pns.icict.fiocruz.br/wp-content/uploads/2021/02/Questionario-PNS-2019.pdf): categorias de P45a/P45b.
- [Depression screening in a population-based study: PNS 2019 (Ciência & Saúde Coletiva, 2023)](https://www.scielo.br/j/csc/a/wWKFtv8ZVZZTwVDM94Q3gFt/): PHQ-9, ponto de corte ≥ 10, prevalência de 10,8%.
- [Tempo de tela durante o lazer e consumo de alimentos (ALAN, 2023)](https://www.alanrevista.org/ediciones/2023/suplemento-1/art-2): uso de P04501/P04502.
- [Tempo de televisão, obesidade e DCV em idosos — PNS 2013/2019 (C&SC)](http://www.scielo.br/j/csc/a/Y6VdtJnCtPNwNtBFwJ8Y3dv/?lang=pt).
- [deltafolha/deltafolha-geracao-ansiosa-br](https://github.com/deltafolha/deltafolha-geracao-ansiosa-br): metodologia da Folha (PNS + SIA/SUS + PISA) para "A Geração Ansiosa" no Brasil.
- TIC Kids Online Brasil 2024 (Cetic.br), via [Acessa.com, out/2024](https://www.acessa.com/noticias/2024/10/226457-tres-em-cada-dez-criancas-e-adolescentes-foram-ofendidos-na-internet.html) e [Campo Grande News](https://www.campograndenews.com.br/educacao-e-tecnologia/pesquisa-mostra-que-ate-adolescentes-admitem-uso-excessivo-das-redes).
- PeNSE 2019: [IBGE, Biblioteca (liv101956)](https://biblioteca.ibge.gov.br/visualizacao/livros/liv101956.pdf) e [RBEpid 2024](https://scielosp.org/pdf/rbepid/2024.v27/e240053/pt).
