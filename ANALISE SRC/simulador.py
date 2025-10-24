import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
import yaml

with open("src/config.yaml", "r") as f:
    CONFIG = yaml.safe_load(f)

ETAPAS = CONFIG["ETAPAS"]
random.seed(CONFIG["SEED"])

def _simular_etapas(tipo_servico: str, start_date: datetime) -> List[Dict[str, str]]:
    status_log = []
    current_dt = start_date

    for etapa, dados in ETAPAS.items():
        min_h, max_h, _ = dados.values()
        duracao_h = random.uniform(min_h, max_h)

        if etapa == "QUOTATION_TO_START" and random.random() < CONFIG["CHANCE_ATRASO"]:
            duracao_h += random.uniform(15.0, 48.0)
        if tipo_servico == "Corretiva" and etapa == "START_TO_REPAIR_END":
            duracao_h += random.uniform(10.0, 15.0)

        current_dt += timedelta(hours=duracao_h)
        status_log.append({"etapa_code": etapa, "data_hora": current_dt.strftime("%Y-%m-%d %H:%M:%S")})

    return status_log

def gerar_dados_simulados(num_os: int = 100) -> List[Dict[str, Any]]:
    dados = []
    start_date = datetime.strptime(CONFIG["START_DATE"], "%Y-%m-%d %H:%M:%S")

    for i in range(1, num_os + 1):
        tipo_servico = random.choice(CONFIG["TIPOS_SERVICO"])
        os_entry = {
            "os_id": f"OS-{1000 + i}",
            "placa_veiculo": f"ABC{random.randint(100,999)}",
            "tipo_servico": tipo_servico,
            "entrada_dt": start_date.strftime("%Y-%m-%d %H:%M:%S"),
            "status_log": _simular_etapas(tipo_servico, start_date),
        }
        dados.append(os_entry)
        start_date += timedelta(hours=random.uniform(1.0, 5.0))

    return dados
