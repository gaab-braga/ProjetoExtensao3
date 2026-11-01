"""
etl_processor.py — ETL dos microdados da PNS 2019 (IBGE) para o Dossiê de Evidências.

Projeto de Extensão IESB · Grupo 1 (Problem Space)
Pergunta: como o uso intenso de telas para lazer (inclui redes sociais e vídeos curtos) influencia ansiedade e déficit de atenção?

Fonte oficial: IBGE — Pesquisa Nacional de Saúde 2019, microdados (arquivo de posição fixa PNS_2019.txt).
  https://ftp.ibge.gov.br/PNS/2019/Microdados/Dados/
  https://ftp.ibge.gov.br/PNS/2019/Microdados/Documentacao/  (dicionário + input SAS)

Uso:
  python etl_processor.py                                   # usa data/raw/PNS_2019.txt (ou o .zip do IBGE)
  python etl_processor.py --raw caminho/PNS_2019_20220525.zip --input data/raw/input_PNS_2019.txt

Saídas:
  data/processed/pns2019_telas_saude_mental.csv   (1 linha por morador selecionado com entrevista realizada)
  data/processed/etl_relatorio.json               (contagens de cada etapa, nulos, distribuição de códigos)
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "data" / "raw"
OUT_DIR = ROOT / "data" / "processed"

# ---------------------------------------------------------------------------
# 1. LAYOUT — posição inicial (1-indexada) e largura de cada variável no PNS_2019.txt.
#    Extraído do layout oficial (input_PNS_2019.txt / dicionário IBGE, versão 20220525).
#    Se o input SAS oficial estiver disponível, o ETL confere estas posições contra ele.
# ---------------------------------------------------------------------------
LAYOUT: dict[str, tuple[int, int]] = {
    # desenho amostral e identificação
    "V0001": (1, 2),        # Unidade da Federação
    "V0024": (3, 7),        # Estrato
    "UPA_PNS": (10, 9),     # Unidade Primária de Amostragem
    "V0006_PNS": (19, 4),   # Nº de ordem do domicílio
    "V0026": (31, 1),       # Situação censitária (1 urbano, 2 rural)
    "V0025A": (33, 1),      # Morador selecionado p/ questionário individual (1 = sim)
    "C00301": (104, 2),     # Nº de ordem do morador
    # demografia
    "C006": (108, 1),       # Sexo (1 homem, 2 mulher)
    "C008": (117, 3),       # Idade
    "C009": (120, 1),       # Cor ou raça
    "VDD004A": (1514, 1),   # Nível de instrução (1 sem instrução ... 7 superior completo)
    "VDF004": (1535, 1),    # Faixa de rendimento domiciliar per capita (em salários mínimos)
    "A01901": (81, 1),      # Algum morador tem acesso à internet no domicílio
    "C011": (133, 1),       # Estado civil (1 casado, 2 divorciado/separado, 3 viúvo, 4 solteiro)
    "VDE001": (1515, 1),    # Condição na força de trabalho (1 na força, 2 fora)
    "VDE002": (1516, 1),    # Condição de ocupação (1 ocupado, 2 desocupado)
    # controle da entrevista individual
    "M001": (527, 1),       # Entrevista do adulto selecionado (1 = realizada)
    # PHQ-9 (Módulo N) — "Nas duas últimas semanas, com que frequência..."
    "N010": (564, 1),       # problemas no sono
    "N011": (565, 1),       # cansaço / falta de energia
    "N012": (566, 1),       # pouco interesse ou prazer (anedonia)
    "N013": (567, 1),       # problemas para se concentrar nas atividades habituais  <-- ATENÇÃO
    "N014": (568, 1),       # problemas na alimentação
    "N015": (569, 1),       # lentidão ou muita agitação/inquietação
    "N016": (570, 1),       # sentiu-se deprimido, "pra baixo" ou sem perspectiva
    "N017": (571, 1),       # sentiu-se mal consigo mesmo / fracasso
    "N018": (572, 1),       # pensou em se ferir / melhor estar morto
    # Tecnologia / telas (Módulo P — estilo de vida)
    "P04501": (705, 1),     # horas/dia assistindo televisão
    "P04502": (706, 1),     # horas/dia de tempo livre em computador, tablet ou celular p/ lazer
                            # ("utilizar redes sociais, ver notícias, vídeos, jogar etc.")
    # Diagnósticos autorreferidos (Módulo Q)
    "Q092": (986, 1),       # diagnóstico de depressão por médico/profissional de saúde mental
    "Q11006": (1007, 1),    # diagnóstico de OUTRA doença mental (transtorno de ansiedade, pânico, TOC...)
    # peso amostral
    "V00291": (1426, 14),   # Peso do morador selecionado com calibração
}

PHQ_ITEMS = ["N010", "N011", "N012", "N013", "N014", "N015", "N016", "N017", "N018"]

# ---------------------------------------------------------------------------
# 2. CODIFICAÇÕES (questionário oficial PNS 2019)
# ---------------------------------------------------------------------------
# P04501 / P04502 — categorias do questionário:
#   1 Menos de uma hora | 2 De 1h a menos de 2h | 3 De 2h a menos de 3h
#   4 De 3h a menos de 6h | 5 Seis horas ou mais | 6 Não assiste TV / Não costuma usar no tempo livre
# Escala ordinal: 0 = não usa, 1..5 = faixas crescentes.
TELA_ORDINAL = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 0}
TELA_HORAS_APROX = {0: 0.0, 1: 0.5, 2: 1.5, 3: 2.5, 4: 4.5, 5: 7.0}  # ponto médio (5 = 6h+ -> 7h, convenção)
TELA_ROTULO = {0: "Não usa", 1: "<1h", 2: "1–2h", 3: "2–3h", 4: "3–6h", 5: "6h+"}

# PHQ-9 — 1 Nenhum dia | 2 Menos da metade dos dias | 3 Mais da metade dos dias | 4 Quase todos os dias
PHQ_ORDINAL = {1: 0, 2: 1, 3: 2, 4: 3}

SEXO = {1: "Homem", 2: "Mulher"}
ESTADO_CIVIL = {1: "Casado", 2: "Divorciado/separado", 3: "Viúvo", 4: "Solteiro"}
REGIAO = {1: "Norte", 2: "Nordeste", 3: "Sudeste", 4: "Sul", 5: "Centro-Oeste"}  # 1º dígito do código da UF
RACA = {1: "Branca", 2: "Preta", 3: "Amarela", 4: "Parda", 5: "Indígena"}
SIM_NAO = {1: 1, 2: 0}
FAIXAS_IDADE = [(15, 17, "15–17"), (18, 24, "18–24"), (25, 34, "25–34"),
                (35, 44, "35–44"), (45, 59, "45–59"), (60, 200, "60+")]


def phq9_algoritmo(itens: pd.DataFrame) -> pd.Series:
    """Algoritmo diagnóstico do PHQ-9 (Kroenke et al., 2001; critérios DSM para episódio depressivo maior):
    >= 5 dos 9 sintomas em 'mais da metade dos dias' (escala 0–3 >= 2), sendo obrigatório humor deprimido (N016)
    ou anedonia (N012); o item de ideação (N018) conta se presente em qualquer frequência (>= 1)."""
    nucleo = ["phq_sono", "phq_cansaco", "phq_anedonia", "phq_concentracao", "phq_apetite",
              "phq_agitacao", "phq_humor_deprimido", "phq_autoestima"]
    n_sintomas = (itens[nucleo] >= 2).sum(axis=1) + (itens["phq_ideacao"] >= 1).astype(int)
    cardinal = (itens["phq_anedonia"] >= 2) | (itens["phq_humor_deprimido"] >= 2)
    return ((n_sintomas >= 5) & cardinal).astype(int)


def sha256(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Leitura
# ---------------------------------------------------------------------------
def localizar_bruto(caminho: Path | None) -> Path:
    if caminho:
        return caminho
    candidatos = sorted(RAW_DIR.glob("PNS_2019*.txt")) + sorted(RAW_DIR.glob("PNS_2019*.zip"))
    if not candidatos:
        sys.exit(
            "[ERRO] Microdados não encontrados em data/raw/.\n"
            "Baixe https://ftp.ibge.gov.br/PNS/2019/Microdados/Dados/ (arquivo PNS_2019_*.zip)\n"
            "e coloque o .zip (ou o PNS_2019.txt extraído) em data/raw/."
        )
    return candidatos[0]


def abrir_texto(caminho: Path) -> io.TextIOBase:
    if caminho.suffix.lower() == ".zip":
        zf = zipfile.ZipFile(caminho)
        nomes = [n for n in zf.namelist() if n.lower().endswith(".txt")]
        if not nomes:
            sys.exit(f"[ERRO] Nenhum .txt dentro de {caminho}")
        print(f"[INFO] Lendo {nomes[0]} de dentro de {caminho.name}")
        return io.TextIOWrapper(zf.open(nomes[0]), encoding="latin-1")
    return open(caminho, encoding="latin-1")


def conferir_layout_com_input_sas(input_path: Path | None) -> dict:
    """Confere as posições do LAYOUT contra o input SAS oficial do IBGE (linhas '@0001 V0001 $2.')."""
    if input_path is None:
        cands = sorted(RAW_DIR.glob("input_PNS_2019*.txt"))
        input_path = cands[0] if cands else None
    if input_path is None or not input_path.exists():
        print("[AVISO] input_PNS_2019.txt não encontrado: usando layout embutido (não conferido).")
        return {"conferido": False}
    texto = input_path.read_text(encoding="latin-1")
    oficial = {}
    for m in re.finditer(r"@(\d+)\s+(\w+)\s+\$?(\d+)\.", texto):
        oficial[m.group(2).upper()] = (int(m.group(1)), int(m.group(3)))
    divergencias = {v: {"embutido": LAYOUT[v], "oficial": oficial.get(v)}
                    for v in LAYOUT if oficial.get(v) != LAYOUT[v]}
    if divergencias:
        print("[ERRO] Layout embutido diverge do input SAS oficial:")
        for v, d in divergencias.items():
            print(f"   {v}: embutido={d['embutido']} oficial={d['oficial']}")
        sys.exit(1)
    print(f"[OK] Posições das {len(LAYOUT)} variáveis conferidas com {input_path.name}.")
    return {"conferido": True, "arquivo": input_path.name}


def ler_microdados(caminho: Path) -> tuple[pd.DataFrame, int]:
    nomes = list(LAYOUT)
    colspecs = [(ini - 1, ini - 1 + larg) for ini, larg in LAYOUT.values()]
    blocos, total = [], 0
    with abrir_texto(caminho) as fh:
        leitor = pd.read_fwf(fh, colspecs=colspecs, names=nomes, dtype=str, header=None,
                             chunksize=50_000, na_filter=False)
        for bloco in leitor:
            total += len(bloco)
            # Mantém só o morador selecionado (questionário individual) — reduz memória cedo.
            bloco = bloco[bloco["V0025A"].str.strip() == "1"]
            blocos.append(bloco)
    return pd.concat(blocos, ignore_index=True), total


def para_numero(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.str.strip().replace("", np.nan), errors="coerce")


def para_peso(s: pd.Series) -> pd.Series:
    """Peso V00291: aceita com ponto decimal explícito ou com 8 decimais implícitos (informat 14.8)."""
    s = s.str.strip()
    tem_ponto = s.str.contains(".", regex=False)
    v = pd.to_numeric(s.replace("", np.nan), errors="coerce")
    return v.where(tem_ponto, v / 1e8)


# ---------------------------------------------------------------------------
# Transformação
# ---------------------------------------------------------------------------
def validar_codigos(df: pd.DataFrame, var: str, validos: set[int], rel: dict) -> None:
    """Registra a distribuição bruta, converte 9 = 'Ignorado' (dicionário IBGE) em nulo e aborta se houver código desconhecido."""
    contagem = df[var].value_counts(dropna=False).sort_index()
    rel.setdefault("distribuicao_codigos_brutos", {})[var] = {str(k): int(v) for k, v in contagem.items()}
    if 9 not in validos:
        rel.setdefault("ignorados_9_convertidos_em_nulo", {})[var] = int((df[var] == 9).sum())
        df.loc[df[var] == 9, var] = np.nan
    invalidos = set(df[var].dropna().astype(int)) - validos
    if invalidos:
        sys.exit(f"[ERRO] {var} tem códigos inesperados {sorted(invalidos)}. "
                 f"Confira o dicionário oficial antes de prosseguir.")


def transformar(df: pd.DataFrame, rel: dict) -> pd.DataFrame:
    for c in df.columns:
        df[c] = para_peso(df[c]) if c == "V00291" else para_numero(df[c])

    n0 = len(df)
    df = df[df["M001"] == 1]                         # entrevista individual realizada
    rel["etapas"]["2_entrevista_realizada_M001"] = len(df)
    df = df[df["V00291"] > 0]                        # peso válido
    rel["etapas"]["3_peso_valido"] = len(df)
    df = df[df["C008"] >= 15].copy()                 # universo do questionário individual (15+)
    rel["etapas"]["4_idade_15_mais"] = len(df)
    rel["etapas"]["removidos_filtros"] = n0 - len(df)

    for v in ("P04501", "P04502"):
        validar_codigos(df, v, set(TELA_ORDINAL), rel)
    for v in PHQ_ITEMS:
        validar_codigos(df, v, set(PHQ_ORDINAL), rel)
    for v in ("Q092", "Q11006", "C006"):
        validar_codigos(df, v, {1, 2}, rel)
    validar_codigos(df, "C011", set(ESTADO_CIVIL), rel)

    out = pd.DataFrame(index=df.index)
    # identificação e desenho amostral
    out["uf"] = df["V0001"].astype("Int64")
    out["estrato"] = df["V0024"].astype("Int64")
    out["upa"] = df["UPA_PNS"].astype("Int64")
    out["peso"] = df["V00291"]
    out["zona_rural"] = (df["V0026"] == 2).astype("Int64")

    # demografia
    out["sexo"] = df["C006"].map(SEXO)
    out["sexo_feminino"] = (df["C006"] == 2).astype("Int64")
    out["idade"] = df["C008"].astype("Int64")
    out["faixa_etaria"] = pd.cut(df["C008"], bins=[f[0] - 1 for f in FAIXAS_IDADE] + [200],
                                 labels=[f[2] for f in FAIXAS_IDADE]).astype(str)
    out["raca_cor"] = df["C009"].map(RACA)                       # 9 = ignorado -> nulo
    out["escolaridade"] = df["VDD004A"].where(df["VDD004A"].between(1, 7)).astype("Int64")
    out["renda_faixa"] = df["VDF004"].where(df["VDF004"].between(1, 7)).astype("Int64")
    out["internet_domicilio"] = df["A01901"].map(SIM_NAO).astype("Int64")
    out["regiao"] = (df["V0001"] // 10).map(REGIAO)
    out["estado_civil"] = df["C011"].map(ESTADO_CIVIL)
    out["ocupacao"] = np.select([df["VDE002"] == 1, df["VDE002"] == 2, df["VDE001"] == 2],
                                ["Ocupado", "Desocupado", "Fora da força de trabalho"], default=None)

    # tecnologia
    out["tela_lazer_ord"] = df["P04502"].map(TELA_ORDINAL).astype("Int64")
    out["tela_lazer_horas"] = out["tela_lazer_ord"].map(TELA_HORAS_APROX).astype(float)
    out["tela_lazer_cat"] = out["tela_lazer_ord"].map(TELA_ROTULO)
    out["tela_lazer_3h_mais"] = (out["tela_lazer_ord"] >= 4).astype("Int64").where(out["tela_lazer_ord"].notna())
    out["tv_ord"] = df["P04501"].map(TELA_ORDINAL).astype("Int64")
    out["tv_horas"] = out["tv_ord"].map(TELA_HORAS_APROX).astype(float)

    # saúde mental — itens PHQ-9 em escala 0–3
    nomes_itens = {"N010": "phq_sono", "N011": "phq_cansaco", "N012": "phq_anedonia",
                   "N013": "phq_concentracao", "N014": "phq_apetite", "N015": "phq_agitacao",
                   "N016": "phq_humor_deprimido", "N017": "phq_autoestima", "N018": "phq_ideacao"}
    for cod, nome in nomes_itens.items():
        out[nome] = df[cod].map(PHQ_ORDINAL).astype("Int64")
    itens = list(nomes_itens.values())
    completo = out[itens].notna().all(axis=1)
    out["phq9_escore"] = out[itens].sum(axis=1, min_count=9).where(completo).astype("Int64")
    out["phq9_depressao"] = (out["phq9_escore"] >= 10).astype("Int64").where(completo)  # ponto de corte validado
    out["phq9_algoritmo"] = phq9_algoritmo(out[itens]).astype("Int64").where(completo)  # validação externa (~5,7%)
    out["phq9_gravidade"] = pd.cut(out["phq9_escore"].astype(float), bins=[-1, 4, 9, 14, 19, 27],
                                   labels=["Mínima", "Leve", "Moderada", "Mod. grave", "Grave"]).astype(str)
    # déficit de atenção / sono frequentes = "mais da metade dos dias" ou "quase todos os dias"
    out["concentracao_frequente"] = (out["phq_concentracao"] >= 2).astype("Int64").where(out["phq_concentracao"].notna())
    out["sono_frequente"] = (out["phq_sono"] >= 2).astype("Int64").where(out["phq_sono"].notna())
    out["agitacao_frequente"] = (out["phq_agitacao"] >= 2).astype("Int64").where(out["phq_agitacao"].notna())

    # diagnósticos autorreferidos
    out["diag_depressao"] = df["Q092"].map(SIM_NAO).astype("Int64")
    out["diag_outro_transtorno_mental"] = df["Q11006"].map(SIM_NAO).astype("Int64")

    # tratamento de nulos: análise principal exige tela + PHQ-9 completos (casos completos, documentado)
    rel["nulos_por_coluna"] = {c: int(out[c].isna().sum()) for c in out.columns}
    analise = out["tela_lazer_ord"].notna() & out["phq9_escore"].notna()
    rel["etapas"]["5_casos_completos_tela_phq9"] = int(analise.sum())
    rel["etapas"]["excluidos_por_nulo_tela_ou_phq9"] = int((~analise).sum())
    return out[analise].reset_index(drop=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raw", type=Path, help="PNS_2019.txt ou o .zip oficial do IBGE")
    ap.add_argument("--input", type=Path, help="input_PNS_2019.txt (SAS) oficial para conferir o layout")
    ap.add_argument("--out", type=Path, default=OUT_DIR / "pns2019_telas_saude_mental.csv")
    args = ap.parse_args()

    bruto = localizar_bruto(args.raw)
    rel: dict = {"fonte": "IBGE — Pesquisa Nacional de Saúde 2019 (microdados)", "arquivo": bruto.name, "etapas": {}}
    rel["layout"] = conferir_layout_com_input_sas(args.input)
    rel["sha256_arquivo_bruto"] = sha256(bruto)

    print(f"[INFO] Lendo {bruto} …")
    df, total = ler_microdados(bruto)
    rel["etapas"]["0_registros_no_arquivo"] = total
    rel["etapas"]["1_morador_selecionado_V0025A"] = len(df)
    print(f"[INFO] {total:,} registros; {len(df):,} moradores selecionados.")

    final = transformar(df, rel)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    final.to_csv(args.out, index=False)
    (args.out.parent / "etl_relatorio.json").write_text(json.dumps(rel, ensure_ascii=False, indent=2))

    print("[OK] Etapas do ETL:")
    for k, v in rel["etapas"].items():
        print(f"   {k:<40} {v:>10,}")
    print(f"[OK] Base analítica: {args.out}  ({len(final):,} linhas × {final.shape[1]} colunas)")


if __name__ == "__main__":
    main()
