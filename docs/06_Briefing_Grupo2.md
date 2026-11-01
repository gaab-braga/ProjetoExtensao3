# Briefing de Passagem — Grupo 1 → Grupo 2

**Projeto de Extensão IESB · Saúde Mental (ODS 3 e ODS 5)**
**Para:** Grupo 2 (Solution Space) · **De:** Grupo 1 (Problem Space)
**Base de evidência:** IBGE — Pesquisa Nacional de Saúde 2019 (n = 90.846; representa 168 milhões de brasileiros com 15+ anos). Detalhes em [`Dossie_Evidencias_Quantitativas.md`](../Dossie_Evidencias_Quantitativas.md).

> Este documento é a versão "de produto" do Dossiê: o que vocês precisam saber para **desenhar** a solução, sem a estatística.

---

## 1. O problema em um parágrafo

Entre brasileiros que usam celular, tablet ou computador no tempo livre, **até cerca de 3 horas por dia não há sinal de prejuízo** à saúde mental. **Acima disso, a prevalência de sintomas depressivos e de dificuldade de concentração sobe**: com 6h ou mais, ela é cerca de **1,6 vez maior**. Esse uso intenso é sobretudo **jovem**: **1 em cada 3 adolescentes de 15 a 17 anos usa 6h ou mais por dia**. As **mulheres** carregam o dobro da carga de sofrimento. São **16,6 milhões** de brasileiros acima de 6h/dia.

## 2. Pergunta "Como poderíamos" (HMW)

> **Como poderíamos ajudar jovens que passam mais de 3 horas por dia em telas de lazer a reduzir esse tempo, de modo a proteger sua concentração e seu bem-estar emocional?**

## 3. As 5 evidências que sustentam o desenho

| # | Evidência | Número | Confiança |
|---|---|---|---|
| 1 | O risco aparece **acima de ~3h/dia**, não antes | Sem diferença entre 1h e 3h; 6h+ = prevalência 1,59× maior (depressão) e 1,55× (concentração) | 🟢 alta no formato · 🟡 o "3h" exato é aproximado |
| 2 | O resultado **não depende** de como os dados foram analisados | 144 de 144 análises alternativas apontam na mesma direção | 🟢 alta |
| 3 | **Jovens são os mais expostos** (o efeito por pessoa é igual em todas as idades) | 58,8% (15–17) e 52,2% (18–24) usam 3h+/dia; 31,9% e 25,3% usam 6h+ | 🟢 alta |
| 4 | **Mulheres jovens com uso intenso** formam o grupo mais afetado | 20,7% com rastreio positivo para depressão (mulheres 15–24, 6h+) | 🟢 alta (descritivo) |
| 5 | **Quem não usa nada também tem mais sintomas** (perfil mais velho e mais pobre) | Não usar não é "o ideal" | 🟢 alta |

⚠️ **O que a evidência NÃO diz:** que telas *causam* ansiedade ou depressão. O estudo é transversal: pessoas em sofrimento também podem buscar mais telas.

## 4. Quem é o público (segmento-alvo)

**Jovens de 15 a 24 anos que usam 6h+/dia de tela de lazer:** cerca de **8,5 milhões** de pessoas.

| Característica | Valor | O que significa para o desenho |
|---|---|---|
| Idade média | 19 anos; **34,7% têm 15–17** | Muitos são **menores de idade** (ver §7) |
| Mulheres | 50,6% | Público misto, mas a carga de sofrimento é maior nelas |
| Frequentam escola | 48,9% | Metade **não** está estudando |
| Trabalham | 40,0% (42,9% fora da força de trabalho) | Rotinas muito diferentes; não pensar só em "estudante" |
| Renda domiciliar até 1 salário mínimo por pessoa | 64,5% | **Solução gratuita e leve**, que rode em celular simples. Essa renda é típica dos jovens em geral, não só dos que usam muito |
| Zona urbana / internet em casa | 92,8% / 96,9% | Canal digital é viável |
| Rastreio positivo de depressão | 14,3% (vs 8,8% dos jovens que usam <3h) | Parte relevante do público **já está em sofrimento** |
| Dificuldade frequente de concentração | 11,6% (vs 7,0%) | Desfecho tangível para o usuário ("consigo focar") |
| Problemas de sono frequentes | 14,8% (vs 8,9%) | Sono é uma porta de entrada provável (hipótese) |

Comparações entre parênteses são descritivas, sem ajuste. Ficha completa: [`08_Persona_Ficha_de_Dados.md`](08_Persona_Ficha_de_Dados.md).

## 5. Princípios de design derivados dos dados

1. **Meta de limiar, não de abstinência.** Mirar em trazer o lazer em telas para **abaixo de ~3h/dia**, com prioridade para quem passa de 6h. Não promover "detox total".
2. **Não estigmatizar.** O uso moderado não está associado a prejuízo. A mensagem é equilíbrio, não culpa.
3. **Sensível a gênero.** Testar a solução com mulheres jovens, o grupo de maior prevalência de sintomas.
4. **Inclusiva.** Funcionar sem custo, em aparelhos simples e com pouco consumo de dados.
5. **Foco no que o usuário sente.** Concentração e sono são desfechos que o jovem percebe no dia a dia, mais motivadores que "saúde mental" em abstrato.

## 6. Métricas de sucesso (comparáveis com a base nacional)

| Métrica | Como medir | Por quê |
|---|---|---|
| Tempo de tela de lazer | **Mesmas 6 faixas da PNS**: não usa, <1h, 1–2h, 2–3h, 3–6h, 6h+ | Permite comparar o usuário com a média nacional |
| % de usuários abaixo de 3h/dia | Proporção na faixa ≤ 2–3h | Traduz a meta de limiar |
| Sintomas depressivos | **PHQ-9**: uso livre, sem necessidade de permissão, citando os autores (Kroenke, Spitzer & Williams, 2001) | Mesma escala do Dossiê. **É rastreio, não diagnóstico** |
| Concentração | Item do PHQ-9: "problemas para se concentrar nas atividades habituais" | Mesmo item usado no Dossiê (N013) |

## 7. Restrições éticas e legais (obrigatórias)

| Tema | O que observar |
|---|---|
| **Dados de saúde** | Respostas a questionários como o PHQ-9 são **dado pessoal sensível** pela LGPD (Lei 13.709/2018, art. 5º, II), com bases legais restritas (art. 11). Coletar o mínimo necessário |
| **Menores de idade** | 1/3 do público tem 15–17 anos. A LGPD exige consentimento específico de pelo menos um responsável (art. 14, §1º). O **ECA Digital** (Lei 15.211/2025), em vigor desde 17/03/2026, impõe obrigações a aplicativos de provável acesso por crianças e adolescentes, como verificação de idade sem mera autodeclaração. **Validar com orientação jurídica** antes de lançar |
| **Item 9 do PHQ-9 (ideação suicida)** | Se a solução usar o PHQ-9, qualquer resposta positiva no item 9 deve disparar um **protocolo de acolhimento**: mensagem de cuidado e encaminhamento ao **CVV, telefone 188** (gratuito, 24 horas). Os próprios materiais do PHQ-9 alertam que o item pode mobilizar sentimentos difíceis |
| **Sem diagnóstico** | A solução **não pode** dizer que o usuário "tem depressão" ou "tem ansiedade". O PHQ-9 indica necessidade de avaliação profissional |

## 8. O que a solução não pode prometer

- "Curar" ou "prevenir" ansiedade ou depressão: os dados mostram associação, não causa.
- Resultados específicos para **vídeos curtos**: a PNS não separa o tipo de conteúdo.
- Tratar "dependência": a PNS mede **tempo**, não uso compulsivo.

## 9. Perguntas que o Grupo 2 deve validar com usuários

1. Em que **momentos e contextos** o uso passa de 3h? Noite? Ociosidade?
2. O jovem **percebe** a relação entre uso intenso, sono e concentração?
3. Por que as soluções existentes (modo foco, bloqueadores, apps de bem-estar digital) são abandonadas? *(benchmarking do Marketing)*
4. O que funciona melhor para menores: autonomia ou participação dos responsáveis?
5. Mulheres jovens vivem o uso intenso de forma diferente (conteúdo, comparação social, pausas na sobrecarga)?

## 10. Kit de arquivos

| Arquivo | Uso |
|---|---|
| [`outputs/indicadores_grupo2.csv`](../outputs/indicadores_grupo2.csv) | 112 indicadores ponderados com IC 95% (uso de tela por idade e sexo; desfechos por faixa de tela × sexo e × idade) para gráficos e protótipos |
| `outputs/graficos/05_dose_resposta_RP.png` | **Gráfico-chave** do limiar |
| `outputs/graficos/03_barras_sexo.png` · `04_barras_idade.png` | Quem é afetado |
| [`07_Arvore_de_Problemas.md`](07_Arvore_de_Problemas.md) | Causas e efeitos, com o que é dado e o que é hipótese |
| [`08_Persona_Ficha_de_Dados.md`](08_Persona_Ficha_de_Dados.md) | Base estatística para a persona |
| [`Dossie_Evidencias_Quantitativas.md`](../Dossie_Evidencias_Quantitativas.md) | Evidência completa |

---

**Referências desta seção:** Kroenke, Spitzer & Williams (2001); Lei 13.709/2018 (LGPD); Lei 15.211/2025 (ECA Digital); CVV (cvv.org.br). Lista completa em [`05_Agenda_de_Pesquisa.md`](05_Agenda_de_Pesquisa.md#referências-todas-verificadas).
