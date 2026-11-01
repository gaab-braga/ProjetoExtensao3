# Guia Operacional - Grupo 1 (Problem Space)

## Projeto de Extensão: Saúde Mental e Tecnologia

Este documento define o plano de ação, a divisão de tarefas e os entregáveis exatos do Grupo 1. Nossa missão não é criar a solução, mas **investigar, provar matematicamente e documentar o problema escolhido**, fornecendo ao Grupo 2 um dossiê robusto para que eles construam a solução em cima de evidências.

> **Atualização (01/11/2026):** a trilha quantitativa está **concluída**. O [Dossiê de Evidências Quantitativas](../Dossie_Evidencias_Quantitativas.md) foi gerado com microdados oficiais do IBGE (PNS 2019). Os resultados estão resumidos na **seção 5** e devem orientar o trabalho do RH e do Marketing.

---

### 🚨 ESCLARECIMENTO DEFINITIVO SOBRE OS ODS (Alinhamento da Equipe)

Houve uma confusão inicial de que precisaríamos escolher três ODS diferentes e fazer pesquisas separadas para cada um. **Isso está incorreto, geraria retrabalho e foge do escopo da disciplina.**

Abaixo está o direcionamento baseado **literalmente nas instruções da aula e no infográfico oficial do IESB**:

1. **Regra do Tema Norteador (A Única Obrigatoriedade Absoluta):**
   * *Texto oficial:* "Projetos que apresentarem fuga ao tema norteador receberão nota 0 (...) Todos os projetos deverão investigar diretamente aspectos relacionados à **Saúde Mental**."
   * *Conclusão:* Ao focarmos nosso único problema em Saúde Mental, nós já atingimos automaticamente o **ODS 3 (Saúde e Bem-Estar)**. Ele é o coração do projeto.
2. **Regra dos ODS Adicionais (A Palavra-Chave é "E/OU"):**
   * *Texto oficial (Passo 4 do infográfico):* "Articulado aos ODS 3, 5 **E/OU** 16, **conforme a pertinência do projeto**."
   * *Conclusão:* O termo "E/OU" significa que não somos obrigados a incluir todos. Faremos **UMA ÚNICA pesquisa** em uma **ÚNICA base de dados**. Se a nossa base mostrar que o problema tecnológico afeta mais as mulheres, nós justificamos a inclusão do **ODS 5 (Igualdade de Gênero)**. Não precisamos de uma pesquisa separada para isso, apenas de uma base de dados que tenha a coluna "Gênero/Sexo" para cruzarmos os dados.

**Resumo da Ópera:** Vamos focar em **UMA** pesquisa sólida, ancorada principalmente no ODS 3, utilizando uma única base de dados.

> ✅ **Decisão tomada com base nos dados:** o **ODS 5 entra**. Na PNS 2019, as mulheres têm **2,5 vezes mais sintomas depressivos** que os homens (15,1% vs 6,0%), e chegam a **19,9%** entre as que passam 6h+/dia em telas de lazer. A justificativa é a **desigualdade de carga**: na escala relativa o efeito da tela é semelhante nos dois sexos, mas as mulheres partem de um patamar muito maior de sofrimento. Na escala absoluta, há indício (sugestivo, p = 0,052) de que o uso de 3h+ soma mais casos entre elas: +4,4 pontos percentuais, contra +2,5 nos homens. O **ODS 16 não se aplica**: os dados não tratam de instituições, violência ou justiça.

---

### 1. Definição do Escopo ✅

A equipe já definiu o nosso direcionamento exato, cumprindo as regras do edital:

* **Tema Norteador Obrigatório:** Saúde Mental
* **ODS Principal:** ODS 3 (Saúde e Bem-Estar)
* **ODS Adicional:** ODS 5 (Igualdade de Gênero), confirmado pelos dados
* **Área do Conhecimento:** Ciências Exatas e da Terra / Tecnológicas
* **Subtema Oficial Escolhido:** Saúde mental, dependência digital e comportamento on-line.
* **Tema Criado pela Equipe:** Ansiedade e dependência tecnológica na sociedade contemporânea: impactos do uso excessivo de tecnologias digitais na saúde mental.
* **Pergunta de Pesquisa Master:** *"Como o uso intenso de telas para lazer — que inclui redes sociais e vídeos curtos — influencia a saúde mental, em especial a ansiedade e os sintomas depressivos, e o déficit de atenção nas atividades do dia a dia, e que padrões de dados podem indicar caminhos para uma relação mais saudável com a tecnologia?"*

> ✅ **Pergunta ajustada em 01/11/2026 para refletir o que os dados oficiais medem.** A versão anterior dizia *"especificamente o consumo frequente de conteúdos de curta duração"* e *"em atividades prolongadas"*. Nenhuma base oficial brasileira isola vídeos curtos: a PNS mede o tempo de lazer em celular, tablet ou computador ("redes sociais, notícias, vídeos, jogos"). E o item de atenção (N013) mede a concentração nas *atividades habituais*. A nova redação mantém os vídeos curtos no escopo, como parte do uso de telas, sem prometer um recorte que os dados não permitem. **Use esta versão em todos os materiais** (DreamShaper, slides, Dossiê).
>
> ✅ **Segundo ajuste (01/11/2026, opção B da revisão metodológica):** a pergunta passou a nomear a **saúde mental** como desfecho, mantendo **ansiedade** e **déficit de atenção** e incluindo **sintomas depressivos**. Motivo: a evidência mais forte da PNS 2019 está nos sintomas depressivos (PHQ-9, escala validada), que antes não apareciam na pergunta. A ansiedade, foco do tema da equipe, é medida apenas por um diagnóstico amplo (ver [`docs/04`](04_Rigor_Metodologico.md) §9). Tema norteador, subtema oficial e tema da equipe **não mudam**.
>
> **Versão curta** (para títulos e capas): *"Como o uso intenso de telas para lazer — que inclui redes sociais e vídeos curtos — influencia a saúde mental, em especial a ansiedade e os sintomas depressivos, e o déficit de atenção na sociedade contemporânea?"*

---

### 2. O Fluxo de Trabalho (Como não travar a equipe)

Para o projeto fluir, **ninguém espera ninguém no início**. O trabalho é dividido em duas trilhas paralelas (Qualitativa e Quantitativa) que correm ao mesmo tempo nas Semanas 1 e 2, e se juntam na Semana 3 para montar o Dossiê.

* **Trilha Quantitativa (Devs):** Focam em achar os dados, limpar e gerar gráficos. Eles provam que a ansiedade digital é real através de números. → ✅ **Concluída.**
* **Trilha Qualitativa (RH/Marketing):** Focam em pesquisar as causas psicológicas (literatura), definir quem sofre com isso (persona) e por que as soluções de hoje não funcionam. Eles dão a "alma" e o contexto aos números. → Deve agora **ancorar-se nos números da seção 5**.

---

### 3. Divisão de Tarefas por Perfil

#### 🧠 A RH (Foco no Comportamento e Literatura)

O RH tem o olhar clínico para bem-estar emocional e atenção focada.

* **A Missão:** Descobrir o *Porquê*.
* **O que fazer imediatamente (Não precisa esperar os Devs):**
  * Pesquisar artigos (Google Acadêmico, Scielo) sobre o impacto da "dopamina barata" (vídeos curtos) na ansiedade e no déficit de atenção.
  * Ler os PDFs base do IESB e extrair os conceitos oficiais sobre Saúde Mental.
  * Mapear a "Árvore de Problemas": Qual é a causa raiz (algoritmos viciantes)? Qual o problema central (dependência)? Quais as consequências (ansiedade, burnout, insônia)?
* **🔄 Com os dados em mãos, priorizar na literatura:**
  * Por que o efeito aparece **só acima de ~3h/dia** (hipótese de deslocamento: o tempo de tela substitui sono, atividade física e convívio).
  * **Causalidade reversa:** pessoas ansiosas ou deprimidas usam telas como fuga? A banca vai perguntar isso, e a literatura ajuda a responder.
  * Por que as mulheres apresentam mais sintomas depressivos (comparação social, cyberbullying, sobrecarga).

#### 🎯 O Marketing (Foco na Persona e Cenário)

O Marketing entende de público, concorrência e como contar uma história.

* **A Missão:** Descobrir o *Quem* e o *Cenário Atual*.
* **O que fazer imediatamente (Não precisa esperar os Devs):**
  * **Criar a Persona:** Quem é a pessoa que vamos ajudar? (Ex: "Lucas, 22 anos, estudante universitário, passa 4h/dia no TikTok e não consegue focar 30 min em um livro sem sentir ansiedade").
  * **Análise de Mercado (Benchmarking):** Quais soluções já existem para combater isso? (Apps como Forest, Modo Foco do celular, bloqueadores de sites). Por que essas soluções *falham*? Onde elas deixam a desejar? (Isso é o que o Grupo 2 vai usar para inovar).
  * **Storytelling do DreamShaper:** Ao final, transformar os achados de todos em um texto coeso e persuasivo para jogar na plataforma do IESB.
* **🔄 Ajuste da persona com base nos dados:** o perfil de maior risco é **jovem (15–24 anos), mulher, com 3h+ de tela de lazer por dia**. A ficha estatística completa, com um esboço narrativo e o roteiro de entrevistas, está em [`08_Persona_Ficha_de_Dados.md`](08_Persona_Ficha_de_Dados.md). Atenção: os dados mostram que o público **não é só universitário**. Metade não estuda, 4 em 10 trabalham, 2/3 vivem com até 1 salário mínimo por pessoa e 1 em cada 3 é menor de idade.

#### 💻 Os Desenvolvedores / Analistas de Dados (2 pessoas) — ✅ CONCLUÍDO

* **A Missão:** Descobrir as *Evidências (O Quê)*.
* **O que foi feito:**
  * ~~Caçar 1 base no Kaggle~~ → por exigência do edital (**base pública e oficial**), usamos os **microdados da Pesquisa Nacional de Saúde 2019 do IBGE**: 90.846 respondentes, que representam 168 milhões de brasileiros com 15+ anos. Avaliamos 6 bases oficiais (IBGE, Cetic.br, DATASUS) antes de escolher.
  * A base tem: **PHQ-9** (escala clínica validada, com item de concentração), **diagnóstico de ansiedade/outros transtornos**, **tempo de tela de lazer** (redes sociais, vídeos, jogos), **sexo e idade**.
  * ETL em Python (`etl_processor.py`), com o layout e os códigos conferidos contra o dicionário oficial do IBGE.
  * Análise (`analise_exploratoria.py`): Pearson/Spearman, controle de confundidores, regressão logística ajustada e recortes por sexo e idade.
  * 5 gráficos em `outputs/graficos/` e o [Dossiê](../Dossie_Evidencias_Quantitativas.md).

---

### 4. A Síntese Final (O que entregaremos ao Grupo 2)

Quando as trilhas se encontrarem, o Marketing e o RH pegam os gráficos dos Devs e juntam com suas pesquisas teóricas e de persona. O Dossiê final entregue ao Grupo 2 (focado em criar a solução) deverá conter:

1. **A Questão de Pesquisa Fechada** (O nosso "HMW - How Might We / Como Poderíamos"). → **Proposta pelos dados:** *"Como poderíamos ajudar jovens que passam mais de 3 horas por dia em telas de lazer a reduzir esse tempo, de modo a proteger sua concentração e seu bem-estar emocional?"*
2. **O Painel de Evidências (Gerado pelos Devs):** Gráficos provando estatisticamente a relação entre tecnologia e saúde mental. → ✅ `outputs/graficos/01` a `06` + [Dossiê](../Dossie_Evidencias_Quantitativas.md) (v2, com revisão metodológica)
3. **A Árvore de Problemas e a Literatura (Gerado pelo RH):** A fundamentação teórica de por que isso afeta a saúde mental. → 🟡 Rascunho baseado em evidências em [`07_Arvore_de_Problemas.md`](07_Arvore_de_Problemas.md) (para o RH revisar) + literatura verificada em [`05_Agenda_de_Pesquisa.md`](05_Agenda_de_Pesquisa.md)
4. **A Persona e o Cenário (Gerado pelo Marketing):** Quem sofre com isso e por que os apps atuais de "bem-estar digital" não estão funcionando. → 🟡 Base estatística em [`08_Persona_Ficha_de_Dados.md`](08_Persona_Ficha_de_Dados.md); o benchmarking de apps é da trilha do Marketing
5. **Briefing de passagem:** → ✅ [`06_Briefing_Grupo2.md`](06_Briefing_Grupo2.md): o documento que o Grupo 2 lê primeiro

---

### 5. Resultados do Dossiê (o que todos precisam saber) 📊

**Fonte:** IBGE, Pesquisa Nacional de Saúde 2019 (microdados oficiais). n = 90.846 pessoas de 15+ anos. Validação: o pipeline reproduz as duas prevalências oficiais publicadas (10,8% pelo corte; 5,7% pelo algoritmo).

> 🔄 **Revisão metodológica (Dossiê v2):** os números abaixo usam **razão de prevalência** com o desenho amostral completo, mais conservadora que o odds ratio da v1. Duas conclusões foram corrigidas: (1) o efeito por pessoa **não** é maior nos jovens, só a exposição; (2) no ODS 5, a escala absoluta sugere mais casos entre mulheres. Detalhes em [`docs/04_Rigor_Metodologico.md`](04_Rigor_Metodologico.md).

#### 5.1 O achado honesto: não é uma reta, é um limiar

* **A correlação linear é desprezível** (Spearman ρ = 0,02). **Não podemos dizer que "quanto mais tela, pior".**
* O que os dados mostram é um **efeito de limiar (curva em J)**: até ~3h/dia de tela de lazer o risco é estável; **acima de 3h ele sobe**.

| Tela de lazer/dia | Prevalência de rastreio positivo para depressão* | Prevalência de dificuldade de concentração frequente* | Prevalência de diagnóstico de ansiedade/outros* |
|---|---|---|---|
| 1–3h | igual a <1h | igual a <1h | igual a <1h |
| 3–6h | **+19%** | **+29%** | +19% (não significativo após correção de multiplicidade) |
| **6h ou mais** | **+59%** | **+55%** | **+38%** |

\* Razão de prevalência ajustada por sexo, idade, renda, escolaridade, TV e zona rural, com o desenho amostral da PNS; comparação com quem usa menos de 1h/dia.

* **Robustez:** a associação apareceu em **144 de 144** formas diferentes de analisar os dados (specification curve).
* **Cuidado:** o ponto exato de 3h surgiu da exploração dos dados. Digam "a partir de cerca de 3h", não "exatamente 3h".

📊 Gráficos principais: `outputs/graficos/05_dose_resposta_RP.png` · `06_specification_curve.png`

#### 5.2 Quem é afetado

| Grupo | Dado-chave |
|---|---|
| **Adolescentes (15–17)** | **58,8%** usam 3h+/dia de tela de lazer |
| **Jovens (18–24)** | **52,2%** usam 3h+/dia; **1 em cada 3** adolescentes de 15–17 (31,9%) e 1 em cada 4 jovens de 18–24 (25,3%) usam **6h+** |
| Efeito por idade | O efeito **por pessoa** é semelhante em todas as idades. O que muda é a **exposição**, muito maior nos jovens |
| Idosos (60+) | Só 5,7% usam 3h+/dia |
| **Mulheres** | 15,1% com sintomas depressivos (vs 6,0% dos homens); **19,9%** entre as que usam 6h+ |
| Brasil | **40,8 milhões** usam 3h+/dia; **16,6 milhões** usam 6h+; **2,4 milhões** destes têm rastreio positivo para depressão |

📊 `outputs/graficos/03_barras_sexo.png` · `outputs/graficos/04_barras_idade.png`

#### 5.3 O que podemos e o que NÃO podemos afirmar

| ✅ Podemos dizer | ❌ Não podemos dizer |
|---|---|
| "Uso acima de 3h/dia está associado a mais sintomas depressivos e problemas de concentração" | "Telas **causam** ansiedade ou depressão" (o estudo é transversal) |
| "O uso intenso é um fenômeno jovem" | "Mais tela é sempre pior" (até 3h não há efeito) |
| "Mulheres carregam o dobro da carga de sofrimento" | "A tela afeta mais as mulheres" (o efeito relativo é semelhante; há só um **indício** de mais casos absolutos) |
| "O uso intenso se concentra nos jovens" | "A tela faz mais mal aos jovens" (o teste de interação não sustenta) |
| "A associação resiste a 144 análises diferentes" | "O limite é exatamente 3h" (o ponto exato é exploratório) |
| "Os dados vêm do IBGE, base oficial nacional" | "Vídeos curtos especificamente…" (a pergunta do IBGE não separa) |

#### 5.4 Limitações (citar na apresentação)

1. Estudo **transversal**: associação, não causa. Pessoas em sofrimento podem usar mais telas como fuga.
2. A pergunta do IBGE **não separa vídeos curtos** de redes sociais, notícias e jogos.
3. Dados de **2019**: pré-pandemia e pré-TikTok massivo. O cenário atual tende a ser pior.
4. A PNS **não tem escala de ansiedade** (GAD-7). Usamos o diagnóstico autorreferido.
5. "Quem não usa tela" também tem mais sintomas, mas é outro perfil (mais velho e mais pobre). **Não é argumento a favor de abstinência digital.**
6. A PNS mede **tempo**, não **dependência**. O tema "dependência tecnológica" não pode ser medido diretamente nesta base.
7. A **ansiedade** é o construto pior medido: diagnóstico amplo, sem escala. Ver a reavaliação da linha de pesquisa em [`docs/04`](04_Rigor_Metodologico.md) §9.

#### 5.5 Recomendações para o Grupo 2

1. **Meta de limiar, não abstinência:** foco em manter o lazer em telas **abaixo de ~3h/dia**.
2. **Público prioritário:** jovens de 15 a 24 anos.
3. **Desenho sensível a gênero:** mulheres jovens com uso intenso são o grupo de maior prevalência.
4. **Desfechos mensuráveis:** concentração e humor (o PHQ-9 é de domínio público e pode ser usado no app para autoavaliação).

---

### 6. Onde está cada coisa (repositório)

| Arquivo | Para quem | Para quê |
|---|---|---|
| [`Dossie_Evidencias_Quantitativas.md`](../Dossie_Evidencias_Quantitativas.md) | **Todos / Grupo 2** | Entregável final completo |
| [`docs/03_Guia_Standup.md`](03_Guia_Standup.md) | **Todos** | Roteiro do standup e respostas para perguntas difíceis da banca |
| `outputs/graficos/*.png` | Marketing (DreamShaper, slides) | Gráficos prontos para apresentação |
| [`docs/01_Data_Discovery.md`](01_Data_Discovery.md) | RH | Justificativa da escolha da base e das variáveis |
| `outputs/resultados_estatisticos.md` | Quem quiser os detalhes | Todas as tabelas numéricas |
| [`docs/04_Rigor_Metodologico.md`](04_Rigor_Metodologico.md) | **Todos** (antes do standup) | Método científico aplicado, STROBE, ética, o que foi corrigido e reavaliação da pergunta |
| [`docs/05_Agenda_de_Pesquisa.md`](05_Agenda_de_Pesquisa.md) | RH e quem quiser aprofundar | Posicionamento na literatura, perguntas abertas e referências verificadas |
| [`docs/06_Briefing_Grupo2.md`](06_Briefing_Grupo2.md) | **Grupo 2** | Passagem: público, princípios de design, métricas, restrições éticas e legais |
| [`docs/07_Arvore_de_Problemas.md`](07_Arvore_de_Problemas.md) | RH | Rascunho da árvore com dado × literatura × hipótese |
| [`docs/08_Persona_Ficha_de_Dados.md`](08_Persona_Ficha_de_Dados.md) | Marketing | Retrato estatístico do público-alvo + roteiro de entrevistas |
| `outputs/indicadores_grupo2.csv` | Marketing e Grupo 2 | 112 indicadores prontos para gráficos e protótipos |
