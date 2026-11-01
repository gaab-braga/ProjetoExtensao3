"""Testes dos métodos amostrais e das recodificações do ETL (dados sintéticos, sem microdados do IBGE)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from metodos_amostrais import e_value, fap, media_amostral, reri, svyglm, wald  # noqa: E402
from etl_processor import PHQ_ORDINAL, TELA_ORDINAL, phq9_algoritmo  # noqa: E402


@pytest.fixture(scope="module")
def dados():
    rng = np.random.default_rng(7)
    n = 6000
    df = pd.DataFrame({
        "estrato": rng.integers(0, 30, n),
        "peso": rng.uniform(50, 3000, n),
        "a": rng.integers(0, 2, n),
        "b": rng.integers(0, 2, n),
    })
    df["upa"] = df["estrato"] * 100 + rng.integers(0, 8, n)
    # desfecho com efeitos multiplicativos puros (sem interação na escala log)
    p = 0.08 * np.exp(0.4 * df["a"] + 0.3 * df["b"])
    df["y"] = (rng.uniform(size=n) < p).astype(int)
    return df


def test_intercepto_poisson_igual_media_linearizada(dados):
    """Poisson só com intercepto: exp(b) = proporção ponderada e EP(log) = EP(p)/p (delta exato)."""
    est, se, _ = media_amostral(dados, "y")
    aj = svyglm(dados, "y ~ 1")
    assert np.exp(aj.b[0]) == pytest.approx(est, rel=1e-8)
    assert aj.ep[0] == pytest.approx(se / est, rel=1e-6)


def test_dominio_mantem_upas_e_bate_com_media(dados):
    dom = dados["a"] == 1
    est, se, n = media_amostral(dados, "y", dominio=dom)
    aj = svyglm(dados, "y ~ 1", dominio=dom)
    assert aj.n == n
    assert np.exp(aj.b[0]) == pytest.approx(est, rel=1e-8)
    assert aj.ep[0] == pytest.approx(se / est, rel=1e-6)


def test_poisson_recupera_razao_de_prevalencia(dados):
    aj = svyglm(dados, "y ~ a + b")
    rp = aj.coef("a")["RP"]
    assert 1.2 < rp < 2.0          # verdadeiro = exp(0.4) ≈ 1.49
    assert aj.coef("a")["ic95"][0] < rp < aj.coef("a")["ic95"][1]


def test_gauss_identidade_diferenca_de_prevalencias(dados):
    aj = svyglm(dados, "y ~ a", familia="gauss-identidade")
    p1, _, _ = media_amostral(dados, "y", dominio=dados["a"] == 1)
    p0, _, _ = media_amostral(dados, "y", dominio=dados["a"] == 0)
    assert aj.coef("a")["dif_pp"] == pytest.approx(100 * (p1 - p0), rel=1e-6)


def test_reri_definicao_e_wald(dados):
    aj = svyglm(dados, "y ~ a * b")
    r = reri(aj, "a", "b", "a:b")
    assert r["RERI"] == pytest.approx(r["RP11"] - r["RP10"] - r["RP01"] + 1)
    w = wald(aj, ["a:b"])
    assert w["gl"] == 1 and 0 <= w["p"] <= 1


def test_e_value_valores_conhecidos():
    # VanderWeele & Ding (2017): RR = 2 -> E-value = 2 + sqrt(2) ≈ 3.41
    assert e_value(2.0)["estimativa"] == pytest.approx(2 + np.sqrt(2))
    assert e_value(1.5, 0.9)["limite_ic"] == 1.0
    assert e_value(0.5)["estimativa"] == pytest.approx(2 + np.sqrt(2))


def test_fap_miettinen():
    # 50% dos casos expostos com RP 2 -> FAP = 0.5 * (1/2) = 0.25
    assert fap({"x": 0.5}, {"x": 2.0}) == pytest.approx(0.25)


def test_recodificacoes_etl():
    assert TELA_ORDINAL[6] == 0 and TELA_ORDINAL[5] == 5          # "não usa" -> 0; "6h+" -> 5
    assert [PHQ_ORDINAL[k] for k in (1, 2, 3, 4)] == [0, 1, 2, 3]


def test_phq9_algoritmo():
    itens = ["phq_sono", "phq_cansaco", "phq_anedonia", "phq_concentracao", "phq_apetite",
             "phq_agitacao", "phq_humor_deprimido", "phq_autoestima", "phq_ideacao"]
    base = dict.fromkeys(itens, 0)
    caso = {**base, "phq_humor_deprimido": 2, "phq_sono": 2, "phq_cansaco": 3, "phq_apetite": 2, "phq_concentracao": 2}
    sem_cardinal = {**base, "phq_sono": 3, "phq_cansaco": 3, "phq_apetite": 3, "phq_concentracao": 3, "phq_agitacao": 3}
    ideacao_conta = {**base, "phq_anedonia": 2, "phq_sono": 2, "phq_cansaco": 2, "phq_apetite": 2, "phq_ideacao": 1}
    df = pd.DataFrame([caso, sem_cardinal, ideacao_conta, base])
    assert phq9_algoritmo(df).tolist() == [1, 0, 1, 0]
