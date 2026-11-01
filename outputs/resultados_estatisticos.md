# Resultados estatísticos (gerado automaticamente por `analise_exploratoria.py`)

Base: PNS 2019 — 90.846 adultos (15+) com tempo de tela e PHQ-9 completos.

## 1. Correlações bivariadas (Spearman)

| Tecnologia | Desfecho | ρ | IC 95% | p | n | Força |
|---|---|---:|---|---:|---:|---|
| tela | phq9 | 0.020 | [0.013; 0.026] | < 0,001 | 90,846 | desprezível |
| tela | concentracao | 0.041 | [0.035; 0.048] | < 0,001 | 90,846 | desprezível |
| tela | sono | -0.034 | [-0.040; -0.027] | < 0,001 | 90,846 | desprezível |
| tela | agitacao | -0.007 | [-0.013; -0.000] | 0,035 | 90,846 | desprezível |
| tela | humor_deprimido | 0.007 | [0.001; 0.014] | 0,025 | 90,846 | desprezível |
| tela | diag_depressao | 0.006 | [-0.000; 0.013] | 0,055 | 90,846 | desprezível |
| tela | diag_ansiedade_outros | 0.062 | [0.055; 0.068] | < 0,001 | 90,846 | desprezível |
| tv | phq9 | 0.017 | [0.011; 0.024] | < 0,001 | 90,846 | desprezível |
| tv | concentracao | -0.018 | [-0.025; -0.012] | < 0,001 | 90,846 | desprezível |
| tv | sono | 0.031 | [0.025; 0.038] | < 0,001 | 90,846 | desprezível |
| tv | agitacao | -0.003 | [-0.010; 0.003] | 0,362 | 90,846 | desprezível |
| tv | humor_deprimido | 0.015 | [0.009; 0.022] | < 0,001 | 90,846 | desprezível |
| tv | diag_depressao | 0.010 | [0.003; 0.016] | 0,003 | 90,846 | desprezível |
| tv | diag_ansiedade_outros | -0.007 | [-0.013; -0.000] | 0,039 | 90,846 | desprezível |

Pearson (horas aproximadas × escore PHQ-9): r = 0.041 [IC95% 0.034; 0.047], p < 0,001.

## 2. Correlação parcial (controle: idade, sexo, escolaridade, renda)

| Par | ρ parcial | IC 95% | p | Força |
|---|---:|---|---:|---|
| tela_x_phq9 | 0.052 | [0.045; 0.058] | < 0,001 | desprezível |
| tela_x_concentracao | 0.031 | [0.025; 0.038] | < 0,001 | desprezível |
| tela_x_sono | 0.031 | [0.025; 0.038] | < 0,001 | desprezível |
| tela_x_agitacao | 0.020 | [0.014; 0.027] | < 0,001 | desprezível |

## 3. Correlação por subgrupo (tela × PHQ-9)

| Grupo | ρ | IC 95% | n |
|---|---:|---|---:|
| sexo=Homem | 0.018 | [0.009; 0.028] | 42,799 |
| sexo=Mulher | 0.003 | [-0.006; 0.012] | 48,047 |
| idade=15–17 | 0.157 | [0.117; 0.197] | 2,315 |
| idade=18–24 | 0.141 | [0.119; 0.162] | 8,145 |
| idade=25–34 | 0.088 | [0.073; 0.104] | 15,970 |
| idade=35–44 | 0.047 | [0.033; 0.062] | 18,033 |
| idade=45–59 | 0.009 | [-0.003; 0.022] | 23,655 |
| idade=60+ | -0.055 | [-0.068; -0.042] | 22,728 |

Diferença Homem vs Mulher: z = 2.26, p 0,024.

## 4. Regressão logística ponderada (OR ajustado; EP robusto por UPA)

**PHQ-9>=10 ~ faixas de tela (ref. <1h)** — `phq9_depressao ~ tela_cat + sexo_feminino + C(faixa_etaria) + escolaridade + C(renda_faixa) + tv_ord + zona_rural` (n = 90,824)

| Termo | OR | IC 95% | p |
|---|---:|---|---:|
| tela_cat[T.Não usa] | 1.22 | [1.07; 1.38] | 0,002 |
| tela_cat[T.1–2h] | 0.92 | [0.80; 1.06] | 0,260 |
| tela_cat[T.2–3h] | 1.00 | [0.86; 1.16] | 0,970 |
| tela_cat[T.3–6h] | 1.22 | [1.04; 1.44] | 0,017 |
| tela_cat[T.6h+] | 1.72 | [1.47; 2.03] | < 0,001 |
| C(faixa_etaria)[T.18–24] | 1.29 | [1.00; 1.65] | 0,049 |
| C(faixa_etaria)[T.25–34] | 1.20 | [0.93; 1.54] | 0,159 |
| C(faixa_etaria)[T.35–44] | 1.34 | [1.05; 1.71] | 0,020 |
| C(faixa_etaria)[T.45–59] | 1.51 | [1.18; 1.94] | 0,001 |
| C(faixa_etaria)[T.60+] | 1.22 | [0.94; 1.59] | 0,139 |
| C(renda_faixa)[T.2.0] | 0.95 | [0.82; 1.10] | 0,487 |
| C(renda_faixa)[T.3.0] | 0.86 | [0.75; 0.99] | 0,038 |
| C(renda_faixa)[T.4.0] | 0.78 | [0.67; 0.92] | 0,002 |
| C(renda_faixa)[T.5.0] | 0.75 | [0.60; 0.93] | 0,009 |
| C(renda_faixa)[T.6.0] | 0.64 | [0.50; 0.81] | < 0,001 |
| C(renda_faixa)[T.7.0] | 0.68 | [0.54; 0.87] | 0,002 |
| sexo_feminino | 2.78 | [2.54; 3.04] | < 0,001 |
| escolaridade | 0.94 | [0.91; 0.96] | < 0,001 |
| tv_ord | 0.96 | [0.93; 0.99] | 0,013 |
| zona_rural | 0.57 | [0.51; 0.64] | < 0,001 |

**PHQ-9>=10 ~ tendência ordinal de tela** — `phq9_depressao ~ tela_lazer_ord + sexo_feminino + C(faixa_etaria) + escolaridade + C(renda_faixa) + tv_ord + zona_rural` (n = 90,824)

| Termo | OR | IC 95% | p |
|---|---:|---|---:|
| C(faixa_etaria)[T.18–24] | 1.28 | [1.00; 1.65] | 0,051 |
| C(faixa_etaria)[T.25–34] | 1.15 | [0.89; 1.47] | 0,289 |
| C(faixa_etaria)[T.35–44] | 1.26 | [0.98; 1.61] | 0,067 |
| C(faixa_etaria)[T.45–59] | 1.46 | [1.14; 1.86] | 0,003 |
| C(faixa_etaria)[T.60+] | 1.27 | [0.98; 1.65] | 0,070 |
| C(renda_faixa)[T.2.0] | 0.93 | [0.80; 1.08] | 0,337 |
| C(renda_faixa)[T.3.0] | 0.84 | [0.73; 0.96] | 0,013 |
| C(renda_faixa)[T.4.0] | 0.75 | [0.64; 0.87] | < 0,001 |
| C(renda_faixa)[T.5.0] | 0.71 | [0.57; 0.88] | 0,002 |
| C(renda_faixa)[T.6.0] | 0.60 | [0.48; 0.76] | < 0,001 |
| C(renda_faixa)[T.7.0] | 0.64 | [0.51; 0.81] | < 0,001 |
| tela_lazer_ord | 1.06 | [1.03; 1.09] | < 0,001 |
| sexo_feminino | 2.75 | [2.51; 3.01] | < 0,001 |
| escolaridade | 0.92 | [0.90; 0.94] | < 0,001 |
| tv_ord | 0.97 | [0.94; 1.00] | 0,034 |
| zona_rural | 0.59 | [0.53; 0.67] | < 0,001 |

**Concentração frequente ~ faixas de tela (ref. <1h)** — `concentracao_frequente ~ tela_cat + sexo_feminino + C(faixa_etaria) + escolaridade + C(renda_faixa) + tv_ord + zona_rural` (n = 90,824)

| Termo | OR | IC 95% | p |
|---|---:|---|---:|
| tela_cat[T.Não usa] | 1.37 | [1.18; 1.59] | < 0,001 |
| tela_cat[T.1–2h] | 0.88 | [0.74; 1.05] | 0,152 |
| tela_cat[T.2–3h] | 0.95 | [0.79; 1.14] | 0,579 |
| tela_cat[T.3–6h] | 1.32 | [1.09; 1.59] | 0,004 |
| tela_cat[T.6h+] | 1.62 | [1.35; 1.95] | < 0,001 |
| C(faixa_etaria)[T.18–24] | 1.01 | [0.77; 1.32] | 0,931 |
| C(faixa_etaria)[T.25–34] | 0.85 | [0.65; 1.10] | 0,217 |
| C(faixa_etaria)[T.35–44] | 0.84 | [0.65; 1.09] | 0,179 |
| C(faixa_etaria)[T.45–59] | 0.93 | [0.72; 1.20] | 0,555 |
| C(faixa_etaria)[T.60+] | 0.76 | [0.58; 1.01] | 0,057 |
| C(renda_faixa)[T.2.0] | 1.04 | [0.87; 1.23] | 0,695 |
| C(renda_faixa)[T.3.0] | 0.92 | [0.78; 1.09] | 0,352 |
| C(renda_faixa)[T.4.0] | 0.91 | [0.76; 1.09] | 0,288 |
| C(renda_faixa)[T.5.0] | 0.92 | [0.71; 1.20] | 0,544 |
| C(renda_faixa)[T.6.0] | 0.76 | [0.58; 0.98] | 0,036 |
| C(renda_faixa)[T.7.0] | 0.97 | [0.73; 1.28] | 0,808 |
| sexo_feminino | 2.05 | [1.85; 2.26] | < 0,001 |
| escolaridade | 0.95 | [0.92; 0.98] | 0,002 |
| tv_ord | 0.96 | [0.93; 1.00] | 0,042 |
| zona_rural | 0.63 | [0.55; 0.73] | < 0,001 |

**Interação ODS 5: PHQ-9>=10 ~ tela 3h+ × sexo** — `phq9_depressao ~ tela_lazer_3h_mais * sexo_feminino + C(faixa_etaria) + escolaridade + C(renda_faixa) + tv_ord + zona_rural` (n = 90,824)

| Termo | OR | IC 95% | p |
|---|---:|---|---:|
| C(faixa_etaria)[T.18–24] | 1.29 | [1.00; 1.66] | 0,046 |
| C(faixa_etaria)[T.25–34] | 1.17 | [0.92; 1.51] | 0,206 |
| C(faixa_etaria)[T.35–44] | 1.31 | [1.03; 1.67] | 0,029 |
| C(faixa_etaria)[T.45–59] | 1.52 | [1.19; 1.94] | < 0,001 |
| C(faixa_etaria)[T.60+] | 1.30 | [1.01; 1.68] | 0,040 |
| C(renda_faixa)[T.2.0] | 0.93 | [0.80; 1.08] | 0,358 |
| C(renda_faixa)[T.3.0] | 0.84 | [0.73; 0.96] | 0,013 |
| C(renda_faixa)[T.4.0] | 0.75 | [0.65; 0.88] | < 0,001 |
| C(renda_faixa)[T.5.0] | 0.71 | [0.57; 0.88] | 0,002 |
| C(renda_faixa)[T.6.0] | 0.61 | [0.48; 0.77] | < 0,001 |
| C(renda_faixa)[T.7.0] | 0.65 | [0.51; 0.82] | < 0,001 |
| tela_lazer_3h_mais | 1.35 | [1.11; 1.63] | 0,002 |
| sexo_feminino | 2.72 | [2.46; 3.01] | < 0,001 |
| tela_lazer_3h_mais:sexo_feminino | 1.05 | [0.85; 1.29] | 0,666 |
| escolaridade | 0.92 | [0.90; 0.95] | < 0,001 |
| tv_ord | 0.96 | [0.93; 0.99] | 0,017 |
| zona_rural | 0.59 | [0.53; 0.66] | < 0,001 |

**Interação idade: PHQ-9>=10 ~ tela 3h+ × jovem (15-24)** — `phq9_depressao ~ tela_lazer_3h_mais * jovem + sexo_feminino + escolaridade + C(renda_faixa) + tv_ord + zona_rural` (n = 90,824)

| Termo | OR | IC 95% | p |
|---|---:|---|---:|
| C(renda_faixa)[T.2.0] | 0.93 | [0.81; 1.08] | 0,373 |
| C(renda_faixa)[T.3.0] | 0.85 | [0.74; 0.97] | 0,019 |
| C(renda_faixa)[T.4.0] | 0.77 | [0.66; 0.89] | < 0,001 |
| C(renda_faixa)[T.5.0] | 0.73 | [0.59; 0.89] | 0,003 |
| C(renda_faixa)[T.6.0] | 0.62 | [0.50; 0.78] | < 0,001 |
| C(renda_faixa)[T.7.0] | 0.66 | [0.53; 0.83] | < 0,001 |
| tela_lazer_3h_mais | 1.31 | [1.18; 1.46] | < 0,001 |
| jovem | 0.87 | [0.72; 1.07] | 0,189 |
| tela_lazer_3h_mais:jovem | 1.08 | [0.84; 1.39] | 0,546 |
| sexo_feminino | 2.76 | [2.52; 3.02] | < 0,001 |
| escolaridade | 0.92 | [0.90; 0.94] | < 0,001 |
| tv_ord | 0.96 | [0.93; 0.99] | 0,020 |
| zona_rural | 0.59 | [0.53; 0.66] | < 0,001 |

**Diag. ansiedade/outros (Q11006) ~ faixas de tela (ref. <1h)** — `diag_outro_transtorno_mental ~ tela_cat + sexo_feminino + C(faixa_etaria) + escolaridade + C(renda_faixa) + tv_ord + zona_rural` (n = 90,824)

| Termo | OR | IC 95% | p |
|---|---:|---|---:|
| tela_cat[T.Não usa] | 1.00 | [0.85; 1.19] | 0,968 |
| tela_cat[T.1–2h] | 0.91 | [0.77; 1.07] | 0,264 |
| tela_cat[T.2–3h] | 0.97 | [0.80; 1.18] | 0,774 |
| tela_cat[T.3–6h] | 1.21 | [1.01; 1.46] | 0,037 |
| tela_cat[T.6h+] | 1.42 | [1.16; 1.75] | < 0,001 |
| C(faixa_etaria)[T.18–24] | 1.50 | [1.09; 2.08] | 0,014 |
| C(faixa_etaria)[T.25–34] | 1.55 | [1.15; 2.09] | 0,004 |
| C(faixa_etaria)[T.35–44] | 1.64 | [1.22; 2.20] | 0,001 |
| C(faixa_etaria)[T.45–59] | 1.56 | [1.16; 2.09] | 0,003 |
| C(faixa_etaria)[T.60+] | 1.04 | [0.76; 1.42] | 0,807 |
| C(renda_faixa)[T.2.0] | 1.03 | [0.84; 1.27] | 0,779 |
| C(renda_faixa)[T.3.0] | 1.23 | [1.01; 1.49] | 0,042 |
| C(renda_faixa)[T.4.0] | 1.21 | [0.99; 1.48] | 0,066 |
| C(renda_faixa)[T.5.0] | 1.59 | [1.24; 2.03] | < 0,001 |
| C(renda_faixa)[T.6.0] | 1.69 | [1.29; 2.20] | < 0,001 |
| C(renda_faixa)[T.7.0] | 2.06 | [1.57; 2.71] | < 0,001 |
| sexo_feminino | 2.23 | [2.02; 2.47] | < 0,001 |
| escolaridade | 1.04 | [1.00; 1.07] | 0,051 |
| tv_ord | 0.97 | [0.93; 1.01] | 0,119 |
| zona_rural | 0.77 | [0.66; 0.90] | 0,001 |

**Usuários 15-24 anos: PHQ-9>=10 ~ tendência por faixa de tela** — `phq9_depressao ~ tela_lazer_ord + sexo_feminino + idade + escolaridade + C(renda_faixa) + tv_ord + zona_rural` (n = 9,173)

| Termo | OR | IC 95% | p |
|---|---:|---|---:|
| C(renda_faixa)[T.2.0] | 1.07 | [0.72; 1.60] | 0,725 |
| C(renda_faixa)[T.3.0] | 1.11 | [0.78; 1.59] | 0,560 |
| C(renda_faixa)[T.4.0] | 1.13 | [0.76; 1.69] | 0,545 |
| C(renda_faixa)[T.5.0] | 1.11 | [0.59; 2.10] | 0,746 |
| C(renda_faixa)[T.6.0] | 0.70 | [0.35; 1.40] | 0,320 |
| C(renda_faixa)[T.7.0] | 0.73 | [0.34; 1.56] | 0,416 |
| tela_lazer_ord | 1.20 | [1.07; 1.35] | 0,002 |
| sexo_feminino | 3.20 | [2.36; 4.35] | < 0,001 |
| idade | 1.03 | [0.99; 1.08] | 0,164 |
| escolaridade | 0.89 | [0.79; 1.00] | 0,047 |
| tv_ord | 0.84 | [0.76; 0.93] | < 0,001 |
| zona_rural | 0.50 | [0.36; 0.70] | < 0,001 |

**Usuários 25-44 anos: PHQ-9>=10 ~ tendência por faixa de tela** — `phq9_depressao ~ tela_lazer_ord + sexo_feminino + idade + escolaridade + C(renda_faixa) + tv_ord + zona_rural` (n = 27,754)

| Termo | OR | IC 95% | p |
|---|---:|---|---:|
| C(renda_faixa)[T.2.0] | 0.84 | [0.65; 1.08] | 0,182 |
| C(renda_faixa)[T.3.0] | 0.72 | [0.56; 0.92] | 0,008 |
| C(renda_faixa)[T.4.0] | 0.65 | [0.50; 0.85] | 0,002 |
| C(renda_faixa)[T.5.0] | 0.62 | [0.43; 0.89] | 0,010 |
| C(renda_faixa)[T.6.0] | 0.68 | [0.44; 1.06] | 0,092 |
| C(renda_faixa)[T.7.0] | 0.68 | [0.44; 1.04] | 0,077 |
| tela_lazer_ord | 1.15 | [1.09; 1.22] | < 0,001 |
| sexo_feminino | 3.01 | [2.57; 3.52] | < 0,001 |
| idade | 1.02 | [1.01; 1.03] | 0,002 |
| escolaridade | 0.95 | [0.91; 1.01] | 0,079 |
| tv_ord | 0.98 | [0.92; 1.04] | 0,455 |
| zona_rural | 0.63 | [0.52; 0.76] | < 0,001 |

**Usuários 45+ anos: PHQ-9>=10 ~ tendência por faixa de tela** — `phq9_depressao ~ tela_lazer_ord + sexo_feminino + idade + escolaridade + C(renda_faixa) + tv_ord + zona_rural` (n = 23,358)

| Termo | OR | IC 95% | p |
|---|---:|---|---:|
| C(renda_faixa)[T.2.0] | 0.79 | [0.51; 1.21] | 0,278 |
| C(renda_faixa)[T.3.0] | 0.52 | [0.35; 0.77] | 0,001 |
| C(renda_faixa)[T.4.0] | 0.45 | [0.30; 0.69] | < 0,001 |
| C(renda_faixa)[T.5.0] | 0.43 | [0.26; 0.71] | < 0,001 |
| C(renda_faixa)[T.6.0] | 0.33 | [0.20; 0.53] | < 0,001 |
| C(renda_faixa)[T.7.0] | 0.35 | [0.21; 0.59] | < 0,001 |
| tela_lazer_ord | 1.09 | [1.02; 1.16] | 0,012 |
| sexo_feminino | 2.81 | [2.33; 3.38] | < 0,001 |
| idade | 0.98 | [0.97; 0.99] | < 0,001 |
| escolaridade | 0.94 | [0.90; 0.99] | 0,011 |
| tv_ord | 1.05 | [0.99; 1.11] | 0,129 |
| zona_rural | 0.74 | [0.55; 0.98] | 0,035 |

## 4b. Sensibilidade — apenas usuários de tela (exclui 'não usa')

| Recorte | ρ | IC 95% | p | n |
|---|---:|---|---:|---:|
| todas_idades | 0.054 | [0.046; 0.062] | < 0,001 | 60,306 |
| parcial_todas_idades | 0.065 | [0.057; 0.073] | < 0,001 | 60,285 |
| concentracao_todas_idades | 0.060 | [0.052; 0.068] | < 0,001 | 60,306 |
| idade=15–17 | 0.132 | [0.088; 0.175] | < 0,001 | 2,012 |
| idade=18–24 | 0.124 | [0.102; 0.147] | < 0,001 | 7,165 |
| idade=25–34 | 0.083 | [0.066; 0.100] | < 0,001 | 13,586 |
| idade=35–44 | 0.047 | [0.031; 0.064] | < 0,001 | 14,177 |
| idade=45–59 | 0.020 | [0.004; 0.036] | 0,013 | 15,167 |
| idade=60+ | 0.025 | [0.004; 0.047] | 0,023 | 8,199 |

## 4c. Perfil por faixa de tela

| tela    |     n |   idade_media |   pct_60_mais |   pct_ate_1SM |   pct_mulheres |
|:--------|------:|--------------:|--------------:|--------------:|---------------:|
| Não usa | 30540 |          56.7 |          47   |          66.7 |           50.7 |
| <1h     | 15597 |          47.5 |          21   |          49.2 |           53.9 |
| 1–2h    | 15590 |          41.3 |          11.3 |          43.4 |           54.1 |
| 2–3h    | 11032 |          36.9 |           8.3 |          44.9 |           54.1 |
| 3–6h    | 10920 |          32.8 |           5.8 |          46.6 |           53.6 |
| 6h+     |  7167 |          28.5 |           3.5 |          55   |           52.6 |

## 5. Prevalências ponderadas

**PHQ-9>=10 por sexo e tela**

| sexo   |   tela_lazer_ord |   pct |   ic_inf |   ic_sup |     n |
|:-------|-----------------:|------:|---------:|---------:|------:|
| Homem  |                0 |  7.37 |     6.58 |     8.15 | 15586 |
| Homem  |                1 |  4.99 |     3.91 |     6.07 |  7067 |
| Homem  |                2 |  4.38 |     3.51 |     5.24 |  7060 |
| Homem  |                3 |  4.99 |     3.97 |     6.02 |  4976 |
| Homem  |                4 |  5.31 |     4.05 |     6.57 |  4887 |
| Homem  |                5 |  8.88 |     7.28 |    10.49 |  3223 |
| Mulher |                0 | 16.09 |    15.04 |    17.15 | 14954 |
| Mulher |                1 | 14.55 |    13.27 |    15.84 |  8530 |
| Mulher |                2 | 12.71 |    11.37 |    14.05 |  8530 |
| Mulher |                3 | 12.9  |    11.32 |    14.48 |  6056 |
| Mulher |                4 | 15.69 |    13.88 |    17.51 |  6033 |
| Mulher |                5 | 19.91 |    17.9  |    21.91 |  3944 |

**Concentracao frequente por sexo e tela**

| sexo   |   tela_lazer_ord |   pct |   ic_inf |   ic_sup |     n |
|:-------|-----------------:|------:|---------:|---------:|------:|
| Homem  |                0 |  6.32 |     5.59 |     7.06 | 15586 |
| Homem  |                1 |  4.17 |     3.11 |     5.22 |  7067 |
| Homem  |                2 |  3.27 |     2.56 |     3.98 |  7060 |
| Homem  |                3 |  4.51 |     3.52 |     5.5  |  4976 |
| Homem  |                4 |  5.74 |     4.58 |     6.9  |  4887 |
| Homem  |                5 |  8.02 |     6.46 |     9.58 |  3223 |
| Mulher |                0 | 10.96 |    10.08 |    11.85 | 14954 |
| Mulher |                1 |  9.1  |     8.04 |    10.15 |  8530 |
| Mulher |                2 |  8.28 |     7.17 |     9.4  |  8530 |
| Mulher |                3 |  8.12 |     6.87 |     9.37 |  6056 |
| Mulher |                4 | 11.49 |     9.82 |    13.17 |  6033 |
| Mulher |                5 | 13.85 |    12.05 |    15.66 |  3944 |

**Uso 3h+ por faixa etaria**

| faixa_etaria   |   pct |   ic_inf |   ic_sup |     n |
|:---------------|------:|---------:|---------:|------:|
| 15–17          | 58.83 |    55.32 |    62.34 |  2315 |
| 18–24          | 52.18 |    50.17 |    54.2  |  8145 |
| 25–34          | 35.96 |    34.52 |    37.4  | 15970 |
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
| 15–17          |                    0 |  8.13 |     5.62 |    10.64 |  1037 |
| 15–17          |                    1 | 11.22 |     8.59 |    13.84 |  1278 |
| 18–24          |                    0 |  9.26 |     7.57 |    10.95 |  4176 |
| 18–24          |                    1 | 12.77 |    10.86 |    14.68 |  3969 |
| 25–34          |                    0 |  8.04 |     7.14 |     8.95 | 10701 |
| 25–34          |                    1 | 12.39 |    10.62 |    14.16 |  5269 |
| 35–44          |                    0 | 10.12 |     9.29 |    10.95 | 14318 |
| 35–44          |                    1 | 12.17 |    10.38 |    13.97 |  3715 |
| 45–59          |                    0 | 11.62 |    10.85 |    12.38 | 20906 |
| 45–59          |                    1 | 13.59 |    11.7  |    15.49 |  2749 |
| 60+            |                    0 | 10.64 |     9.86 |    11.41 | 21621 |
| 60+            |                    1 | 12.02 |     8.34 |    15.69 |  1107 |

**PHQ-9>=10 por sexo**

| sexo   |   pct |   ic_inf |   ic_sup |     n |
|:-------|------:|---------:|---------:|------:|
| Homem  |  5.97 |     5.54 |     6.4  | 42799 |
| Mulher | 15.06 |    14.44 |    15.68 | 48047 |

**Geral**

| indicador              |   pct |   ic_inf |   ic_sup |     n |
|:-----------------------|------:|---------:|---------:|------:|
| phq9_depressao         | 10.78 |    10.38 |    11.18 | 90846 |
| concentracao_frequente |  7.81 |     7.45 |     8.18 | 90846 |
| tela_lazer_3h_mais     | 24.21 |    23.62 |    24.79 | 90846 |
