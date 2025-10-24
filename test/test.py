import pytest
from src.simulador import gerar_dados_simulados, ETAPAS
from src.analise import extrair_tempos_por_etapa, identificar_gargalos

def test_gerar_dados_simulados():
    dados = gerar_dados_simulados(5)
    assert isinstance(dados, list)
    assert "status_log" in dados[0]
    assert len(dados) == 5

def test_extrair_tempos_por_etapa():
    dados = gerar_dados_simulados(3)
    df = extrair_tempos_por_etapa(dados)
    assert not df.empty
    assert "LEAD_TIME_TOTAL_H" in df.columns

def test_identificar_gargalos():
    dados = gerar_dados_simulados(10)
    df = extrair_tempos_por_etapa(dados)
    gargalos = identificar_gargalos(df, ETAPAS)
    assert isinstance(gargalos, dict) or hasattr(gargalos, "head")
    assert len(gargalos) > 0
