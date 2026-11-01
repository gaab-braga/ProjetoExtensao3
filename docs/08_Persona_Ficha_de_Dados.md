# Persona — Ficha de Dados (rascunho para o Marketing)

**Projeto de Extensão IESB · Grupo 1 · Insumo para a trilha qualitativa (Marketing)**

> Uma persona boa é **ficção ancorada em dados**. Esta ficha traz a **âncora**: o retrato estatístico do público-alvo nos microdados da PNS 2019, ponderado para representar a população, com IC 95%. A parte narrativa (seção 3) é **ilustrativa** e deve ser refinada com entrevistas.

---

## 1. Retrato estatístico do segmento-alvo

**Segmento:** jovens de **15 a 24 anos** com **6h ou mais por dia** de tela de lazer (celular, tablet ou computador). Representam **≈ 8,5 milhões** de brasileiros (n amostral = 2.584).

| Característica | Jovens 15–24 com **6h+** | Mulheres 15–24 com **6h+** | Jovens 15–24 que usam **<3h** (comparação) |
|---|---:|---:|---:|
| População representada | 8,5 milhões | 4,3 milhões | 11,8 milhões |
| Idade média | 19,1 | 19,1 | 20,0 |
| Têm 15–17 anos (menores) | **34,7%** [31,3; 38,0] | 33,4% | 25,1% |
| Mulheres | 50,6% [47,3; 53,9] | 100% | 51,1% |
| Frequentam escola | 48,9% [45,5; 52,3] | 47,0% | 42,2% |
| Ocupados (trabalham) | 40,0% [36,6; 43,4] | 38,0% | 51,3% |
| Fora da força de trabalho | 42,9% [39,5; 46,2] | 45,4% | 37,0% |
| Renda domiciliar ≤ 1 salário mínimo por pessoa | 64,5% [61,2; 67,7] | 68,4% | 66,9% |
| Zona urbana | 92,8% [91,4; 94,2] | 92,6% | 83,2% |
| Internet no domicílio | 96,9% [96,2; 97,7] | 96,6% | 90,6% |
| **Rastreio positivo para depressão (PHQ-9 ≥ 10)** | **14,3%** [12,1; 16,6] | **20,7%** [17,1; 24,2] | 8,8% [7,2; 10,5] |
| **Dificuldade frequente de concentração** | **11,6%** [9,6; 13,6] | **15,0%** [11,9; 18,0] | 7,0% [5,5; 8,4] |
| Problemas de sono frequentes | 14,8% [12,6; 17,1] | 19,1% [15,8; 22,4] | 8,9% [7,1; 10,6] |
| Diagnóstico de ansiedade/outros (autorreferido) | 8,1% [6,3; 9,8] | 10,9% [8,0; 13,8] | 4,8% [3,8; 5,9] |

*Comparações entre colunas são descritivas, sem ajuste por confundidores. Os efeitos ajustados estão no Dossiê, §4.3. Fonte: `outputs/resultados_estatisticos.json` → `perfil_segmento_alvo`.*

## 2. O que os dados dizem sobre a persona (e o que derrubam)

| Insight | Base | Implicação |
|---|---|---|
| **Não é só universitário de classe média.** Metade não estuda, 4 em 10 trabalham, 2/3 vivem com até 1 salário mínimo por pessoa | Tabela acima | A persona do exemplo inicial do Guia ("Lucas, universitário") representa só uma parte do público |
| A baixa renda é **típica dos jovens em geral** (66,9% entre os que usam <3h), não um traço dos que usam muito | Coluna de comparação | Renda não diferencia o segmento, mas define a **restrição de acesso** (solução gratuita e leve) |
| **1 em cada 3 é menor de idade** | 34,7% com 15–17 | A persona precisa de uma variante adolescente, com o contexto familiar e legal (LGPD art. 14; ECA Digital) |
| **Metade são mulheres**, e elas concentram mais sintomas (20,7% de rastreio positivo) | Coluna de mulheres | Uma persona feminina é a escolha mais representativa do **sofrimento** |
| Urbanos e conectados | 92,8% e 96,9% | Canal digital viável. Conectividade não é barreira |
| Sono e concentração são queixas **frequentes** (~12–15%) | Tabela acima | Ganchos de comunicação concretos ("dormir melhor", "conseguir focar") |

## 3. Esboço narrativo (FICÇÃO ILUSTRATIVA, não é dado)

> **Ana, 19 anos**, mora em área urbana, não está estudando no momento e não tem trabalho fixo. O celular é seu principal lazer e fica nas mãos **mais de 6 horas por dia** no tempo livre. Tem dificuldade para se concentrar quando tenta se dedicar a algo e dorme mal com frequência. A renda da família é apertada, então qualquer solução precisa ser gratuita e funcionar no celular que já tem.

Cada traço da Ana corresponde a um dado da tabela: idade média 19; urbana (93%); não frequenta escola (53% das mulheres do segmento); sem ocupação (62% das mulheres do segmento não estão ocupadas); 6h+; concentração e sono frequentes; renda ≤ 1 salário mínimo por pessoa (68%). **O conteúdo do uso (redes sociais, vídeos) não é medido** e deve vir das entrevistas (seção 4). **Variante sugerida: "Bia, 16 anos"**, que frequenta escola, para representar o terço de menores.

## 4. O que o Marketing precisa pesquisar (os dados da PNS não cobrem)

A PNS não mede estes pontos; eles vêm de **entrevistas ou questionários próprios**:

| Tema | Pergunta-guia para entrevista |
|---|---|
| Conteúdo | "O que você mais faz no celular no tempo livre? Quanto disso são vídeos curtos?" |
| Contexto | "Em que momentos do dia você mais usa? O que estaria fazendo se não estivesse no celular?" |
| Percepção | "Você sente que o uso afeta seu sono ou sua concentração?" |
| Tentativas | "Já tentou usar menos? Usou algum app ou modo foco? Por que parou?" *(alimenta o benchmarking)* |
| Motivação | "O que faria você querer usar menos? O que você ganharia?" |

Ao entrevistar menores de 18 anos, seguir as orientações de consentimento do projeto e do IESB.
