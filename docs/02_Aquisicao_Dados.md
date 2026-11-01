# Passo 2 — Aquisição dos microdados (CHECK-POINT)

## Status: ✅ concluído (01/11/2026)

Arquivos baixados diretamente do FTP oficial do IBGE após a liberação do domínio no ambiente:

| Arquivo | Tamanho | Conteúdo |
|---|---:|---|
| `PNS_2019_20220525.zip` | 29,5 MB (455 MB descompactado) | `PNS_2019.txt`, com 293.726 registros de posição fixa |
| `Dicionario_e_input_20220530.zip` | 172 KB | `dicionario_PNS_microdados_2019.xls`, `input_PNS_2019.txt`, `input_PNS_2019.sas` |

Para reproduzir em outra máquina, siga uma das opções abaixo.

### Opção A — Baixar manualmente (≈ 5 minutos)

1. Abra a pasta oficial: **https://ftp.ibge.gov.br/PNS/2019/Microdados/Dados/**
2. Baixe o arquivo **`PNS_2019_20220525.zip`** (ou o `PNS_2019_*.zip` mais recente da pasta).
3. Abra a pasta de documentação: **https://ftp.ibge.gov.br/PNS/2019/Microdados/Documentacao/**
4. Baixe o `.zip` de **Dicionário e input** e extraia dele o arquivo **`input_PNS_2019.txt`**. O ETL usa esse arquivo para conferir as posições das colunas. Guarde também o `dicionario_PNS_microdados_2019.xls` para consulta.
5. Coloque os arquivos em `data/raw/`:
   ```
   data/raw/PNS_2019_20220525.zip      (pode deixar zipado)
   data/raw/input_PNS_2019.txt
   ```
6. Rode:
   ```bash
   pip install -r requirements.txt
   python etl_processor.py
   python analise_exploratoria.py
   ```

> Os arquivos de `data/raw/` estão no `.gitignore`: **não faça commit dos microdados** (o GitHub limita arquivos a 100 MB).

### Opção B — Liberar o domínio para o Claude baixar sozinho

Nas configurações do ambiente de nuvem do Claude Code (menu do ambiente no título da sessão → **Edit** → **Network access**), adicione `ftp.ibge.gov.br` em **Allowed domains**.
Documentação: https://code.claude.com/docs/en/cloud-environments#network-access

## Por que não usar um espelho não oficial?

O edital exige base **pública e oficial**. Espelhos de terceiros (Kaggle, buckets pessoais) quebram a cadeia de custódia do dado. O arquivo deve vir do FTP do IBGE.
