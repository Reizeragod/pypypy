import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def _validar_dado_os(os: Dict[str, Any]) -> bool:
    return all(k in os for k in ("os_id", "tipo_servico", "entrada_dt", "status_log"))

def _converter_para_datetime(dt_str: str) -> datetime:
    try:
        return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        raise ValueError(f"Data inválida detectada: {dt_str} ({e})")

def _calcular_lead_time(status_log: List[Dict[str, str]], entrada: datetime) -> Tuple[Dict[str, float], float]:
    etapas_duracao = {}
    anterior = entrada
    for log in status_log:
        if "etapa_code" not in log or "data_hora" not in log:
            continue
        atual = _converter_para_datetime(log["data_hora"])
        duracao_h = max((atual - anterior).total_seconds() / 3600, 0.0)
        etapas_duracao[log["etapa_code"]] = duracao_h
        anterior = atual
    return etapas_duracao, (anterior - entrada).total_seconds() / 3600

def extrair_tempos_por_etapa(
    dados_json: List[Dict[str, Any]],
    cache_path: Optional[str] = "data/cache_analise.parquet",
    usar_cache: bool = True
) -> pd.DataFrame:
    """
    Extrai tempos por etapa e calcula Lead Time total.
    Se cache habilitado, carrega/parquetiza automaticamente.
    """
    if usar_cache and os.path.exists(cache_path):
        print(f"⚡ Carregando cache: {cache_path}")
        return pd.read_parquet(cache_path)

    registros = []
    for os in dados_json:
        if not _validar_dado_os(os):
            continue
        entrada = _converter_para_datetime(os["entrada_dt"])
        etapas, lead_time_total = _calcular_lead_time(os["status_log"], entrada)
        registro = {"OS_ID": os["os_id"], "TIPO_SERVICO": os["tipo_servico"], **etapas, "LEAD_TIME_TOTAL_H": lead_time_total}
        registros.append(registro)

    if not registros:
        raise ValueError("Nenhuma OS válida encontrada.")

    df = pd.DataFrame(registros).fillna(0)

    if usar_cache:
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        df.to_parquet(cache_path, index=False)
        print(f"✅ Cache salvo: {cache_path}")

    return df

def identificar_gargalos(df: pd.DataFrame, etapas: Dict[str, Any], top_n: int = 3) -> pd.Series:
    etapas_keys = [e for e in etapas.keys() if e in df.columns]
    if not etapas_keys:
        raise KeyError("Nenhuma etapa correspondente encontrada.")
    return df[etapas_keys].mean().sort_values(ascending=False).head(top_n)

def gerar_resumo_estatistico(df: pd.DataFrame) -> pd.DataFrame:
    if "TIPO_SERVICO" not in df or "LEAD_TIME_TOTAL_H" not in df:
        raise KeyError("Colunas obrigatórias ausentes.")
    resumo = (
        df.groupby("TIPO_SERVICO")["LEAD_TIME_TOTAL_H"]
        .agg(["mean", "std", "min", "max"])
        .rename(columns={
            "mean": "Média (h)",
            "std": "Desvio Padrão (h)",
            "min": "Mínimo (h)",
            "max": "Máximo (h)"
        })
        .sort_values("Média (h)", ascending=False)
    )
    return resumo

def detectar_outliers(df: pd.DataFrame, etapas: Dict[str, Any]) -> pd.DataFrame:
    """
    Detecta outliers por método IQR (Interquartile Range).
    Retorna DataFrame com flag booleana por etapa.
    """
    etapas_keys = [e for e in etapas.keys() if e in df.columns]
    outlier_flags = pd.DataFrame(index=df.index)

    for etapa in etapas_keys:
        Q1 = df[etapa].quantile(0.25)
        Q3 = df[etapa].quantile(0.75)
        IQR = Q3 - Q1
        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR
        outlier_flags[etapa + "_OUTLIER"] = ~df[etapa].between(limite_inferior, limite_superior)

    df_out = pd.concat([df, outlier_flags], axis=1)
    df_out["NUM_OUTLIERS"] = outlier_flags.sum(axis=1)
    return df_out

def visualizar_boxplot(df: pd.DataFrame, etapas: Dict[str, Any], interativo: bool = False):
    """
    Gera visualização boxplot por etapa para identificar variabilidade e outliers.
    """
    etapas_keys = [e for e in etapas.keys() if e in df.columns]
    df_melt = df.melt(value_vars=etapas_keys, var_name="Etapa", value_name="Tempo (h)")

    if interativo:
        fig = px.box(df_melt, x="Etapa", y="Tempo (h)", color="Etapa",
                     title="Distribuição dos Tempos por Etapa (Boxplot)",
                     points="outliers")
        fig.update_xaxes(tickangle=45)
        fig.show()
    else:
        plt.figure(figsize=(10, 6))
        sns.boxplot(x="Etapa", y="Tempo (h)", data=df_melt, palette="Set3", showfliers=True)
        plt.xticks(rotation=45)
        plt.title("Distribuição dos Tempos por Etapa (Boxplot)")
        plt.tight_layout()
        plt.show()
