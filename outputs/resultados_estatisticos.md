# Resultados estatísticos (gerado automaticamente por `analise_exploratoria.py`)

Base: PNS 2019 — 90.846 pessoas de 15+ anos com tempo de tela e PHQ-9 completos. Toda inferência usa o desenho amostral (estrato + UPA + peso V00291).

## 0. Validação externa

| Indicador | Este pipeline | Literatura |
|---|---|---|
| PHQ-9 ≥ 10 | 10.78% [10.38; 11.18] | 10,8% [10,4; 11,0] |
| PHQ-9 algoritmo | 5.63% [5.34; 5.93] | 5,7% [5,4; 6,0] |

## 1. Hipótese primária — RP ajustada de PHQ-9 ≥ 10 por faixa de tela (ref. < 1h)

| Faixa | Bruta | Ajustada (principal) | Ajustada (estendida) |
|---|---|---|---|
| Não usa | 1.16 [1.05; 1.29] | 1.18 [1.06; 1.32] | 1.18 [1.06; 1.32] |
| 1–2h | 0.88 [0.77; 0.99] | 0.93 [0.82; 1.05] | 0.92 [0.82; 1.05] |
| 2–3h | 0.91 [0.80; 1.04] | 1.00 [0.87; 1.14] | 0.98 [0.86; 1.13] |
| 3–6h | 1.07 [0.93; 1.24] | 1.19 [1.03; 1.37] | 1.17 [1.02; 1.35] |
| 6h+ | 1.45 [1.28; 1.64] | 1.59 [1.39; 1.83] | 1.54 [1.34; 1.77] |

**H1 — tendência entre usuários (RP por faixa):** 1.12 [1.08; 1.16]. p < 0.001 (n = 60.285).
Não linearidade (Wald, 3 gl): χ² = 22.7, p < 0,001.
Exploratório — faixas abaixo de 3h (1–2h e 2–3h = 1): p 0,460; faixas acima de 3h (3–6h e 6h+ = 1): p < 0,001.

## 2. Desfechos secundários e interações (q = FDR de Benjamini-Hochberg)

| Teste | Estimativa | p | q (FDR) |
|---|---|---:|---:|
| Dificuldade de concentração frequente (N013): RP 3–6h vs <1h | 1.29 [1.08; 1.53] | 0,004 | 0,008 |
| Dificuldade de concentração frequente (N013): RP 6h+ vs <1h | 1.55 [1.31; 1.83] | < 0,001 | < 0,001 |
| Dificuldade de concentração frequente (N013): tendência entre usuários | 1.13 [1.08; 1.18] | < 0,001 | < 0,001 |
| Dificuldade de concentração frequente (N013): não linearidade | χ² = 19.3 | < 0,001 | < 0,001 |
| Diagnóstico de ansiedade/outros transtornos (Q11006): RP 3–6h vs <1h | 1.19 [1.01; 1.41] | 0,041 | 0,070 |
| Diagnóstico de ansiedade/outros transtornos (Q11006): RP 6h+ vs <1h | 1.38 [1.14; 1.66] | < 0,001 | 0,002 |
| Diagnóstico de ansiedade/outros transtornos (Q11006): tendência entre usuários | 1.11 [1.06; 1.16] | < 0,001 | < 0,001 |
| Diagnóstico de ansiedade/outros transtornos (Q11006): não linearidade | χ² = 7.6 | 0,054 | 0,072 |
| Interação multiplicativa — Sexo (ref. homens; comparado: mulheres) | 0.91 [0.73; 1.12] | 0,366 | 0,440 |
| Interação aditiva (p.p.) — Sexo (ref. homens; comparado: mulheres) | 1.91 [-0.01; 3.84] | 0,052 | 0,072 |
| Interação multiplicativa — Idade (ref. 25+; comparado: 15–24 anos) | 1.04 [0.82; 1.32] | 0,745 | 0,813 |
| Interação aditiva (p.p.) — Idade (ref. 25+; comparado: 15–24 anos) | 0.25 [-2.23; 2.72] | 0,845 | 0,845 |

## 3. Interações (domínio: usuários; exposição 3h+ vs <3h)

**Sexo (ref. homens; comparado: mulheres)**

- RP no grupo de referência: 1.49 [1.22; 1.81]; no grupo comparado: 1.35 [1.22; 1.49]
- Interação multiplicativa (razão de RPs): 0.91 [0.73; 1.12], p 0,366
- Excesso absoluto da exposição (p.p.): referência 2.48 [1.21; 3.75]; comparado 4.39 [2.81; 5.97]
- Interação aditiva (diferença das diferenças, p.p.): 1.91 [-0.01; 3.84], p 0,052
- RERI: 0.48 [0.07; 0.88], p 0,021

**Idade (ref. 25+; comparado: 15–24 anos)**

- RP no grupo de referência: 1.34 [1.22; 1.48]; no grupo comparado: 1.40 [1.11; 1.75]
- Interação multiplicativa (razão de RPs): 1.04 [0.82; 1.32], p 0,745
- Excesso absoluto da exposição (p.p.): referência 3.24 [2.11; 4.38]; comparado 3.49 [1.20; 5.78]
- Interação aditiva (diferença das diferenças, p.p.): 0.25 [-2.23; 2.72], p 0,845
- RERI: 0.03 [-0.23; 0.29], p 0,818

## 4. Robustez

| Medida | Valor |
|---|---|
| E-value PHQ-9 ≥ 10, 3–6h vs <1h | 1.67 (limite do IC: 1.21) |
| E-value PHQ-9 ≥ 10, 6h+ vs <1h | 2.56 (limite do IC: 2.12) |
| E-value Dificuldade de concentração frequente (N013), 6h+ vs <1h | 2.47 (limite do IC: 1.94) |
| E-value Diagnóstico de ansiedade/outros transtornos (Q11006), 6h+ vs <1h | 2.10 (limite do IC: 1.55) |
| FAP hipotética PHQ-9 ≥ 10 atribuível a 3h+ (supõe causalidade) | 7.3% |
| Specification curve | 144 modelos; mediana RP 1.38; 100% com RP > 1; 100% com IC acima de 1 |

| Desfecho (spec curve) | n | Mediana RP | % IC > 1 |
|---|---:|---:|---:|
| Concentração | 36 | 1.43 | 100% |
| Escore PHQ-9 | 36 | 1.23 | 100% |
| PHQ-9 algoritmo | 36 | 1.47 | 100% |
| PHQ-9 ≥ 10 | 36 | 1.35 | 100% |

| Exposição (spec curve) | n | Mediana RP | % IC > 1 |
|---|---:|---:|---:|
| 3h+ vs 1–3h (usuários) | 48 | 1.39 | 100% |
| 3h+ vs <3h (todos) | 48 | 1.33 | 100% |
| 6h+ vs <1h | 48 | 1.57 | 100% |

## 5. Correlações (descritivas)

| Par | ρ | IC 95% | p | Força |
|---|---:|---|---:|---|
| tela_x_phq9 | 0.020 | [0.013; 0.026] | < 0,001 | desprezível |
| tela_x_concentracao | 0.041 | [0.035; 0.048] | < 0,001 | desprezível |
| tela_x_sono | -0.034 | [-0.040; -0.027] | < 0,001 | desprezível |
| tela_x_agitacao | -0.007 | [-0.013; -0.000] | 0,035 | desprezível |
| tela_x_humor_deprimido | 0.007 | [0.001; 0.014] | 0,025 | desprezível |
| tela_x_diag_ansiedade_outros | 0.062 | [0.055; 0.068] | < 0,001 | desprezível |
| tela_x_phq9 (parcial) | 0.052 | [0.045; 0.058] | < 0,001 | desprezível |
| tela_x_concentracao (parcial) | 0.031 | [0.025; 0.038] | < 0,001 | desprezível |

| Usuários, por idade (tela × PHQ-9) | ρ | IC 95% | n |
|---|---:|---|---:|
| 15–17 | 0.132 | [0.088; 0.175] | 2,012 |
| 18–24 | 0.124 | [0.102; 0.147] | 7,165 |
| 25–34 | 0.083 | [0.066; 0.100] | 13,586 |
| 35–44 | 0.047 | [0.031; 0.064] | 14,177 |
| 45–59 | 0.020 | [0.004; 0.036] | 15,167 |
| 60+ | 0.025 | [0.004; 0.047] | 8,199 |

## 6. Perfil por faixa de tela

| tela    |     n |   idade_media |   pct_60_mais |   pct_ate_1SM |   pct_mulheres |
|:--------|------:|--------------:|--------------:|--------------:|---------------:|
| Não usa | 30540 |          56.7 |          47   |          66.7 |           50.7 |
| <1h     | 15597 |          47.5 |          21   |          49.2 |           53.9 |
| 1–2h    | 15590 |          41.3 |          11.3 |          43.4 |           54.1 |
| 2–3h    | 11032 |          36.9 |           8.3 |          44.9 |           54.1 |
| 3–6h    | 10920 |          32.8 |           5.8 |          46.6 |           53.6 |
| 6h+     |  7167 |          28.5 |           3.5 |          55   |           52.6 |

## 7. Prevalências ponderadas

**PHQ-9>=10 por faixa de tela**

|   tela_lazer_ord |   pct |   ic_inf |   ic_sup |     n |
|-----------------:|------:|---------:|---------:|------:|
|                0 | 11.79 |    11.13 |    12.46 | 30540 |
|                1 | 10.15 |     9.26 |    11.03 | 15597 |
|                2 |  8.88 |     8.06 |     9.7  | 15590 |
|                3 |  9.27 |     8.29 |    10.25 | 11032 |
|                4 | 10.87 |     9.69 |    12.05 | 10920 |
|                5 | 14.68 |    13.33 |    16.02 |  7167 |

**PHQ-9>=10 por sexo e tela**

| sexo   |   tela_lazer_ord |   pct |   ic_inf |   ic_sup |     n |
|:-------|-----------------:|------:|---------:|---------:|------:|
| Homem  |                0 |  7.37 |     6.58 |     8.15 | 15586 |
| Homem  |                1 |  4.99 |     3.91 |     6.07 |  7067 |
| Homem  |                2 |  4.38 |     3.51 |     5.24 |  7060 |
| Homem  |                3 |  4.99 |     3.98 |     6.01 |  4976 |
| Homem  |                4 |  5.31 |     4.05 |     6.56 |  4887 |
| Homem  |                5 |  8.88 |     7.24 |    10.53 |  3223 |
| Mulher |                0 | 16.09 |    15.04 |    17.15 | 14954 |
| Mulher |                1 | 14.55 |    13.27 |    15.84 |  8530 |
| Mulher |                2 | 12.71 |    11.36 |    14.05 |  8530 |
| Mulher |                3 | 12.9  |    11.32 |    14.48 |  6056 |
| Mulher |                4 | 15.69 |    13.83 |    17.56 |  6033 |
| Mulher |                5 | 19.91 |    17.87 |    21.95 |  3944 |

**Concentracao frequente por sexo e tela**

| sexo   |   tela_lazer_ord |   pct |   ic_inf |   ic_sup |     n |
|:-------|-----------------:|------:|---------:|---------:|------:|
| Homem  |                0 |  6.32 |     5.59 |     7.06 | 15586 |
| Homem  |                1 |  4.17 |     3.11 |     5.22 |  7067 |
| Homem  |                2 |  3.27 |     2.56 |     3.98 |  7060 |
| Homem  |                3 |  4.51 |     3.53 |     5.49 |  4976 |
| Homem  |                4 |  5.74 |     4.5  |     6.98 |  4887 |
| Homem  |                5 |  8.02 |     6.47 |     9.57 |  3223 |
| Mulher |                0 | 10.96 |    10.08 |    11.85 | 14954 |
| Mulher |                1 |  9.1  |     8.04 |    10.15 |  8530 |
| Mulher |                2 |  8.28 |     7.16 |     9.41 |  8530 |
| Mulher |                3 |  8.12 |     6.86 |     9.37 |  6056 |
| Mulher |                4 | 11.49 |     9.78 |    13.2  |  6033 |
| Mulher |                5 | 13.85 |    12.05 |    15.66 |  3944 |

**Uso 3h+ por faixa etaria**

| faixa_etaria   |   pct |   ic_inf |   ic_sup |     n |
|:---------------|------:|---------:|---------:|------:|
| 15–17          | 58.83 |    55.11 |    62.54 |  2315 |
| 18–24          | 52.18 |    50.1  |    54.27 |  8145 |
| 25–34          | 35.96 |    34.51 |    37.41 | 15970 |
| 35–44          | 21.01 |    19.82 |    22.21 | 18033 |
| 45–59          | 11.29 |    10.59 |    12    | 23655 |
| 60+            |  5.73 |     5.18 |     6.27 | 22728 |

**Uso 3h+ por sexo**

| sexo   |   pct |   ic_inf |   ic_sup |     n |
|:-------|------:|---------:|---------:|------:|
| Homem  |  24.1 |    23.25 |    24.94 | 42799 |
| Mulher |  24.3 |    23.51 |    25.09 | 48047 |

**PHQ-9>=10 por faixa etaria e uso 3h+**

| faixa_etaria   |   tela_lazer_3h_mais |   pct |   ic_inf |   ic_sup |     n |
|:---------------|---------------------:|------:|---------:|---------:|------:|
| 15–17          |                    0 |  8.13 |     5.39 |    10.88 |  1037 |
| 15–17          |                    1 | 11.22 |     8.43 |    14.01 |  1278 |
| 18–24          |                    0 |  9.26 |     7.48 |    11.04 |  4176 |
| 18–24          |                    1 | 12.77 |    10.81 |    14.73 |  3969 |
| 25–34          |                    0 |  8.04 |     7.15 |     8.94 | 10701 |
| 25–34          |                    1 | 12.39 |    10.6  |    14.18 |  5269 |
| 35–44          |                    0 | 10.12 |     9.29 |    10.94 | 14318 |
| 35–44          |                    1 | 12.17 |    10.35 |    13.99 |  3715 |
| 45–59          |                    0 | 11.62 |    10.85 |    12.38 | 20906 |
| 45–59          |                    1 | 13.59 |    11.61 |    15.57 |  2749 |
| 60+            |                    0 | 10.64 |     9.86 |    11.41 | 21621 |
| 60+            |                    1 | 12.02 |     8.26 |    15.78 |  1107 |

**PHQ-9>=10 por sexo**

| sexo   |   pct |   ic_inf |   ic_sup |     n |
|:-------|------:|---------:|---------:|------:|
| Homem  |  5.97 |     5.54 |     6.4  | 42799 |
| Mulher | 15.06 |    14.44 |    15.68 | 48047 |

**Uso 6h+ por faixa etaria**

| faixa_etaria   |   pct |   ic_inf |   ic_sup |     n |
|:---------------|------:|---------:|---------:|------:|
| 15–17          | 31.93 |    28.63 |    35.24 |  2315 |
| 18–24          | 25.25 |    23.49 |    27.01 |  8145 |
| 25–34          | 13.49 |    12.52 |    14.45 | 15970 |
| 35–44          |  6.88 |     6.28 |     7.49 | 18033 |
| 45–59          |  3.45 |     3.04 |     3.86 | 23655 |
| 60+            |  1.68 |     1.37 |     1.99 | 22728 |
