# Guia para o Standup Final — o que cada arquivo é e o que dizer

> Use a ordem abaixo como roteiro. Ela segue o **Double Diamond**: descobrir a fonte → limpar → analisar → concluir → entregar ao Grupo 2.

## 1. Roteiro de 2 minutos (fala sugerida)

1. **Fonte:** "Avaliamos 6 bases oficiais. A única que cruza tempo de tela com uma escala clínica de saúde mental no mesmo indivíduo é a **PNS 2019 do IBGE**: 90 mil pessoas que representam 168 milhões de brasileiros com 15 anos ou mais."
2. **Rigor:** "Nosso pipeline reproduziu as duas prevalências oficiais publicadas (10,8% e 5,7%). Usamos o desenho amostral completo da pesquisa e o checklist internacional STROBE."
3. **Achado honesto:** "A correlação linear é desprezível (ρ = 0,02). Não dá para dizer que 'mais tela é sempre pior'."
4. **Achado principal:** "O que existe é um **limiar**. Até cerca de 3h por dia nada muda; acima disso a prevalência sobe, e com 6h ou mais o rastreio de depressão é 59% maior e a dificuldade de concentração, 55% maior. Testamos 144 formas diferentes de analisar, e o resultado apareceu em todas."
5. **Quem:** "59% dos adolescentes usam 3h ou mais por dia, e 1 em cada 3 usa 6h ou mais. O efeito por pessoa é igual em todas as idades: o problema dos jovens é a **exposição**. As mulheres têm 2,5 vezes mais sintomas depressivos, o que justifica o **ODS 5**."
6. **Entrega ao Grupo 2:** "A pergunta 'Como poderíamos': ajudar jovens acima de 3h/dia a reduzir esse uso, protegendo concentração e bem-estar."

## 2. Cada arquivo, o que representa e o que dizer

### Documentação (Problem Space — "Descobrir")

| Arquivo | O que é | Papel no projeto | Frase para o standup |
|---|---|---|---|
| `README.md` | Porta de entrada do repositório | Mapa do projeto e de como rodar | "Qualquer pessoa reproduz tudo com 3 comandos." |
| `docs/01_Data_Discovery.md` | Mapeamento das bases e das colunas | Justifica a escolha da base perante o edital (base pública e oficial) | "Avaliamos IBGE, Cetic.br e DATASUS e escolhemos a PNS com critério, não por conveniência." |
| `docs/02_Aquisicao_Dados.md` | Procedência dos dados | Cadeia de custódia: o dado veio do FTP oficial do IBGE | "Nada de Kaggle ou espelho: fonte primária do governo." |
| `docs/03_Guia_Standup.md` | Este roteiro | Alinhamento da equipe | — |
| `docs/04_Rigor_Metodologico.md` | Diagnóstico do método científico, STROBE, ética, histórico das decisões | Mostra que o trabalho se autocorrigiu | "Revisamos o próprio trabalho e corrigimos duas conclusões que estavam exageradas." |
| `docs/05_Agenda_de_Pesquisa.md` | Posicionamento na literatura e perguntas abertas | Ponte para um aprofundamento futuro | "Deixamos mapeado o que os dados sugerem mas não respondem." |

### Código (o "laboratório")

| Arquivo | O que faz | Analogia | Frase para o standup |
|---|---|---|---|
| `etl_processor.py` | Lê os 455 MB do IBGE, filtra quem respondeu a entrevista, transforma respostas em números e calcula o PHQ-9 | A **cozinha**: lava e corta os ingredientes | "Trava sozinho se algum código fugir do dicionário oficial. Isso é controle de qualidade." |
| `analise_exploratoria.py` | Hipóteses, razão de prevalência, interações, specification curve, gráficos | O **laboratório**: faz os experimentos | "Não paramos na correlação simples. Controlamos idade, renda e escolaridade, que mascaravam o efeito." |
| `metodos_amostrais.py` | Estatística que respeita o desenho amostral da PNS (estrato + conglomerado + peso) | A **balança calibrada** | "Sem isso, os intervalos de confiança ficariam artificialmente estreitos." |
| `tests/` | Testes automáticos dos métodos | O **controle de qualidade** | "Provamos que o método reproduz o cálculo de referência." |
| `requirements.txt` | Lista de bibliotecas Python | A **receita** do ambiente | "Garante que o resultado é igual em qualquer computador." |

### Dados (intermediários)

| Arquivo | O que é | Frase para o standup |
|---|---|---|
| `data/raw/` (fora do Git) | Microdados brutos do IBGE | "Matéria-prima oficial, não alterada." |
| `data/processed/pns2019_telas_saude_mental.csv` (fora do Git, regenerável) | Base limpa: 90.846 pessoas × 36 variáveis | "A base analítica." |
| `data/processed/etl_relatorio.json` | Registro de cada filtro aplicado | "Auditoria: sabemos quantas pessoas saíram em cada etapa e por quê (3.268 recusas)." |

### Resultados (as provas)

| Arquivo | O que mostra | Como ler | Frase para o standup |
|---|---|---|---|
| `outputs/graficos/01_scatter_correlacao.png` | Cada ponto cinza é uma pessoa; a linha azul é a média por faixa de tela | Linha quase plana = correlação linear fraca | "Mostramos com transparência que a correlação simples é fraca." |
| `outputs/graficos/02_heatmap_correlacoes.png` | Correlação entre todas as variáveis | Vermelho = andam juntas; azul = opostas | "O quadrado azul-escuro (tela × idade = −0,50) explica por que o efeito ficava escondido: quem usa mais tela é mais jovem." |
| `outputs/graficos/03_barras_sexo.png` | % com sintomas por faixa de tela, homens vs mulheres | Barras laranja sempre ~2× maiores | "**ODS 5:** as mulheres carregam o dobro da carga em todas as faixas, chegando a 20% no grupo de 6h+." |
| `outputs/graficos/04_barras_idade.png` | Uso intenso por idade; depressão por idade × tela | Barras despencam com a idade | "59% dos adolescentes passam de 3h/dia. Em todas as idades, quem passa de 3h tem mais sintomas." |
| `outputs/graficos/05_dose_resposta_RP.png` ⭐ | **Gráfico principal**: razão de prevalência ajustada por faixa de tela, para 3 desfechos | Acima da linha 1 = mais prevalência; o formato é uma curva em J | "Até ~3h a prevalência é estável; depois sobe. É um **limiar**, não uma reta. Esse é o número que o Grupo 2 deve usar." |
| `outputs/graficos/06_specification_curve.png` | 144 análises alternativas, cada ponto um modelo | Todos os pontos acima da linha 1 = resultado robusto | "O resultado não depende de escolhas convenientes: apareceu em 144 de 144 análises." |
| `outputs/resultados_estatisticos.md` / `.json` | Todas as tabelas numéricas | Fonte de cada número citado | "Cada número do dossiê tem rastreabilidade." |

### Entregável final

| Arquivo | O que é | Frase para o standup |
|---|---|---|
| `Dossie_Evidencias_Quantitativas.md` | Documento de passagem para o Grupo 2: fonte, metodologia, resultados, veredito, limitações e recomendações | "O que está provado, o que **não** está provado, e qual problema o Grupo 2 deve resolver." |

## 3. Perguntas difíceis que a banca pode fazer

| Pergunta | Resposta |
|---|---|
| "Então tela causa depressão?" | "Não podemos afirmar. O estudo é transversal: mostra associação. Pode ser que pessoas em sofrimento usem mais telas como fuga." |
| "Por que a correlação é tão baixa se vocês dizem que há efeito?" | "Porque a relação não é linear. Até 3h não muda nada, e o efeito se concentra no topo. A correlação de Pearson/Spearman mede reta, e a reta 'dilui' o efeito do limiar." |
| "Por que quem não usa tela também tem mais sintomas?" | "Porque é outro perfil: 47% têm 60+ anos e 67% ganham até 1 salário mínimo. É exclusão digital e envelhecimento, não efeito da tecnologia." |
| "Isso fala de vídeos curtos?" | "Não diretamente. A pergunta do IBGE junta redes sociais, vídeos, notícias e jogos. Nenhuma base oficial isola o TikTok. Por isso ajustamos a nossa pergunta de pesquisa para 'uso intenso de telas para lazer, que **inclui** redes sociais e vídeos curtos'. Ela promete exatamente o que os dados entregam." |
| "Dados de 2019 não estão velhos?" | "São os mais recentes da PNS com esse módulo. E são pré-TikTok/pandemia, então o cenário atual tende a ser **pior**, não melhor." |
| "E a ansiedade?" | "É nosso ponto mais fraco, e dizemos isso. A PNS não tem escala de ansiedade. O diagnóstico autorreferido mostra associação em 6h+ (RP 1,38), mas é uma medida ampla." |
| "Por que a pergunta fala em sintomas depressivos se o tema é ansiedade?" | "Porque deixamos os dados corrigirem a pergunta. A ansiedade continua no centro, mas a PNS só a mede por um diagnóstico amplo. A medida mais forte de saúde mental da base é o PHQ-9, de sintomas depressivos. Incluímos os dois sob 'saúde mental', sem abandonar o tema." |
| "Os jovens são mais afetados?" | "Eles são mais **expostos**: 1 em cada 3 adolescentes usa 6h+. Mas o teste estatístico mostra que o efeito por pessoa é semelhante em todas as idades." |
| "Por que razão de prevalência e não odds ratio?" | "Porque o desfecho é comum (11%). Nesse caso o odds ratio exagera o efeito. É o padrão recomendado em epidemiologia para estudos transversais (Barros & Hirakata, 2003)." |
| "Vocês não escolheram a análise que dava resultado?" | "Por isso fizemos a specification curve: 144 combinações de escolhas, e a associação apareceu em todas. Também declaramos que o ponto de 3h é exploratório." |
