# Agenda de Pesquisa — reflexões, perguntas abertas e próximos passos

**Projeto de Extensão IESB · Grupo 1**

Este documento é intencionalmente **aberto**. Ele registra o que os dados da PNS 2019 *sugerem mas não respondem*, para orientar uma revisão de literatura e um eventual aprofundamento (iniciação científica, TCC ou artigo). Nada aqui é conclusão: são **perguntas bem formuladas**.

---

## 1. Onde o trabalho se encaixa na literatura (verificado)

| Estudo | O que fez | O que deixou em aberto, e onde podemos contribuir |
|---|---|---|
| **Werneck et al., 2018** — *J Affect Disord* 236:23–30 | PNS **2013**, tempo de **TV** × sintomas depressivos (PHQ-9), n = 60.202. Associação em U: muito pouca e muita TV (> 5h/dia) ligadas a mais depressão, exceto em idosos | Em 2013 o foco era TV. A PNS 2019 introduziu celular, tablet e computador no lazer, a tela que interessa ao nosso tema |
| **Silva et al., 2021** — *BMC Public Health* | PNS **2019**, **correlatos** dos comportamentos de tela em 88.509 adultos. Sintomas depressivos aparecem entre os fatores associados a mais TV e a mais uso de outras telas | A tela era o **desfecho**. Nós invertemos: tela como **exposição**, com dose-resposta, desfecho de **concentração**, interação aditiva por sexo e specification curve |
| **Melo et al., 2023** — *Ciênc Saúde Colet* 28(4):1163–74 | Prevalência de rastreio de depressão na PNS 2019 (10,8% no corte ≥ 10; 5,7% pelo algoritmo) | Usamos como **validação externa** do nosso pipeline |
| **Przybylski & Weinstein, 2017** — *Psychol Sci* 28:204–15 | "Hipótese Goldilocks digital": em 120 mil adolescentes ingleses, uso moderado não prejudica, e a relação com bem-estar é curvilínea | **Nosso padrão em J em adultos brasileiros é compatível com essa hipótese.** Vale testá-la formalmente |
| **Orben & Przybylski, 2019** — *Nat Hum Behav* 3:173–82 | Specification curve em 3 bases (>300 mil jovens): associação negativa pequena, ~0,4% da variância do bem-estar | Mostra por que a robustez importa; adotamos o mesmo método |
| **Haidt, 2024** (*The Anxious Generation*) × **Odgers, 2024** (resenha na *Nature*) | Haidt atribui o aumento de ansiedade em jovens ao smartphone e às redes sociais; Odgers responde que a evidência causal não sustenta a tese | Nossos dados **não arbitram** esse debate (são transversais), mas trazem um dado brasileiro, populacional e com desenho amostral |

> **Pendência de revisão:** busca estruturada no SciELO, LILACS e PubMed por "PNS 2019" + "screen time"/"tempo de tela" + "depress*"/"ansiedade"/"concentração". Precisamos confirmar se **já existe** estudo com P04502 como exposição e PHQ-9 como desfecho com razão de prevalência. Encontramos um preprint de 2026 (medRxiv) com análise ampla de exposições na PNS 2013/2019, mas não conseguimos verificar se ele inclui tempo de tela.

---

## 2. Perguntas abertas que os dados levantaram

### 2.1 Sobre o efeito
1. **Por que o risco só aparece acima de ~3h/dia?** Hipótese do *deslocamento*: o tempo de tela substitui sono, atividade física e convívio. Ela é testável com variáveis da própria PNS (atividade física no módulo P), **sem ajustar mediadores no modelo principal**. Seria uma análise de mediação.
2. **O limiar é o mesmo para todos?** Nossos dados não mostram diferença de efeito por idade, mas o grupo 15–17 tem só 2.315 pessoas. Faltaria poder estatístico para detectar diferenças moderadas?
3. **Por que quem não usa tela também tem mais sintomas?** O grupo é mais velho e mais pobre (exclusão digital). Seria um grupo em isolamento social? A literatura sobre exclusão digital e saúde mental de idosos pode ajudar.

### 2.2 Sobre gênero (ODS 5)
4. **Por que a carga absoluta parece maior nas mulheres** se o efeito relativo é igual? Hipóteses da literatura a investigar: comparação social, cyberbullying, sobrecarga de trabalho doméstico e de cuidado (tempo de tela como pausa?).
5. A interação aditiva ficou no limite (p = 0,052). **Ela se replicaria** numa amostra independente?

### 2.3 Sobre medida (o elo mais fraco)
6. **Tempo ≠ dependência.** O tema da equipe fala em "dependência tecnológica", mas a PNS mede horas. Escalas de uso problemático, como a Bergen Social Media Addiction Scale, teriam outro resultado? Bases candidatas: TIC Kids Online (Cetic.br) para 9–17 anos.
7. **Ansiedade mal medida.** Q11006 é um diagnóstico amplo e depende de acesso a serviços. Há base brasileira com tempo de tela e uma escala de ansiedade (ex.: GAD-7)?
8. **Conteúdo, não só tempo.** Vídeos curtos têm efeito diferente de leitura de notícias ou mensagens? Nenhuma base oficial separa isso. Seria possível com dados de uso real do celular (screen time do sistema) em amostra própria?

### 2.4 Sobre causalidade
9. **Causalidade reversa**: pessoas em sofrimento procuram a tela como fuga? Só um desenho longitudinal responde. Coortes brasileiras como ELSA-Brasil e as coortes de Pelotas têm medidas de saúde mental; seria preciso verificar se medem tempo de tela.
10. **Replicação temporal**: a PNS 2013 permite repetir a análise? É preciso verificar se ela tem item equivalente ao P04502 (Werneck et al. 2018 usaram apenas TV).

---

## 3. Próximos passos, se houver aprofundamento

| Nível | Passo | Esforço |
|---|---|---|
| Congresso (atual) | Resumo expandido com os resultados deste repositório + STROBE resumido | Baixo, material pronto |
| Iniciação científica | Revisão estruturada da literatura (item 2 da pendência) + análise de mediação (pergunta 1) | Médio |
| Iniciação científica | Replicação na PNS 2013, se houver item equivalente | Médio |
| Artigo | Pré-registro (OSF) das hipóteses confirmatórias antes da replicação; manuscrito IMRaD; validação cruzada com o pacote `survey` do R | Alto |
| Artigo / TCC | Amostra própria com escala de uso problemático + GAD-7 + tempo de tela objetivo | Alto |

---

## Referências (todas verificadas)

- BARROS, A. J. D.; HIRAKATA, V. N. Alternatives for logistic regression in cross-sectional studies: an empirical comparison of models that directly estimate the prevalence ratio. *BMC Medical Research Methodology*, v. 3, art. 21, 2003.
- BONETT, D. G.; WRIGHT, T. A. Sample size requirements for estimating Pearson, Kendall and Spearman correlations. *Psychometrika*, v. 65, n. 1, p. 23–28, 2000.
- BRASIL. Conselho Nacional de Saúde. Resolução nº 510, de 7 de abril de 2016.
- HAIDT, J. *The Anxious Generation: how the great rewiring of childhood is causing an epidemic of mental illness*. 2024.
- IBGE. *Pesquisa Nacional de Saúde 2019: microdados*. Rio de Janeiro: IBGE, 2022.
- KNOL, M. J.; VANDERWEELE, T. J. Recommendations for presenting analyses of effect modification and interaction. *International Journal of Epidemiology*, v. 41, n. 2, p. 514–520, 2012.
- KROENKE, K.; SPITZER, R. L.; WILLIAMS, J. B. The PHQ-9: validity of a brief depression severity measure. *Journal of General Internal Medicine*, v. 16, n. 9, p. 606–613, 2001.
- LUMLEY, T. Analysis of complex survey samples. *Journal of Statistical Software*, v. 9, n. 1, p. 1–19, 2004.
- MELO, A. P. S. et al. Depression screening in a population-based study: Brazilian National Health Survey 2019. *Ciência & Saúde Coletiva*, v. 28, n. 4, p. 1163–1174, 2023.
- ODGERS, C. L. [Resenha de *The Anxious Generation*, de J. Haidt]. *Nature*, 2024. Disponível em: https://www.nature.com/articles/d41586-024-00902-2.
- ORBEN, A.; PRZYBYLSKI, A. K. The association between adolescent well-being and digital technology use. *Nature Human Behaviour*, v. 3, p. 173–182, 2019.
- PRZYBYLSKI, A. K.; WEINSTEIN, N. A large-scale test of the Goldilocks hypothesis. *Psychological Science*, v. 28, n. 2, p. 204–215, 2017.
- SANTOS, I. S. et al. Sensibilidade e especificidade do Patient Health Questionnaire-9 (PHQ-9) entre adultos da população geral. *Cadernos de Saúde Pública*, v. 29, n. 8, p. 1533–1543, 2013.
- SILVA et al. Correlates of screen-based behaviors among adults from the 2019 Brazilian National Health Survey. *BMC Public Health*, 2021.
- SIMONSOHN, U.; SIMMONS, J. P.; NELSON, L. D. Specification curve analysis. *Nature Human Behaviour*, v. 4, p. 1208–1214, 2020.
- STOPA, S. R. et al. Pesquisa Nacional de Saúde 2019: histórico, métodos e perspectivas. *Epidemiologia e Serviços de Saúde*, v. 29, n. 5, e2020315, 2020.
- VANDERWEELE, T. J.; DING, P. Sensitivity analysis in observational research: introducing the E-value. *Annals of Internal Medicine*, v. 167, n. 4, p. 268–274, 2017.
- VON ELM, E. et al. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement. *PLoS Medicine*, v. 4, n. 10, e296, 2007.
- WERNECK, A. O. et al. Associations between TV viewing and depressive symptoms among 60,202 Brazilian adults: the Brazilian National Health Survey. *Journal of Affective Disorders*, v. 236, p. 23–30, 2018.
