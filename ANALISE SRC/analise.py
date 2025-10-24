import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

def extrair_tempos_por_etapa(dados_json: List[Dict[str, Any]]) -> pd.DataFrame:
    registros = []
    for os in dados_json:
        registro = {"OS_ID": os["os_id"], "TIPO_SERVICO": os["tipo_servico"]}
        entrada = datetime.strptime(os["entrada_dt"], "%Y-%m-%d %H:%M:%S")
        anterior = entrada
        for log in os["status_log"]:
            atual = datetime.strptime(log["data_hora"], "%Y-%m-%d %H:%M:%S")
            registro[log["etapa_code"]] = (atual - anterior).total_seconds() / 3600
            anterior = atual
        registro["LEAD_TIME_TOTAL_H"] = (anterior - entrada).total_seconds() / 3600
        registros.append(registro)
    return pd.DataFrame(registros)

def identificar_gargalos(df: pd.DataFrame, etapas: Dict[str, Any], top_n: int = 3) -> pd.Series:
    etapas_keys = list(etapas.keys())
    tempos_medios = df[etapas_keys].mean().sort_values(ascending=False)
    return tempos_medios.head(top_n)
