import pandas as pd
from datetime import datetime, timedelta
import random
import json
import logging
from typing import List, Dict, Any, Tuple
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# --- CONFIGURAÇÃO GLOBAL ---
CONFIG = {
    "start_date": datetime(2025, 7, 1, 8, 0, 0),
    "seed": 42,
    "chance_atraso": 0.35,
    "volume_dados": 100
}

ETAPAS = {
    'CHECK_IN_TO_DIAG': (1.0, 3.0, 'Espera/Diagnóstico Inicial'),
    'DIAG_TO_QUOTATION': (0.5, 2.0, 'Elaboração Orçamento'),
    'QUOTATION_TO_START': (2.0, 15.0, 'Aprovação Cliente/Espera Peças'),
    'START_TO_REPAIR_END': (5.0, 30.0, 'Reparo na Baia')
}

random.seed(CONFIG["seed"])

# --- FUNÇÕES DE SIMULAÇÃO ---

def _simular_etapas(tipo_servico: str, start_date: datetime) -> List[Dict[str, str]]:
    status_log = []
    current_dt = start_date

    for etapa, (min_h, max_h, _) in ETAPAS.items():
        duracao_h = random.uniform(min_h, max_h)
        if etapa == 'QUOTATION_TO_START' and random.random() < CONFIG["chance_atraso"]:
            duracao_h += random.uniform(15.0, 48.0)
        if tipo_servico == 'Corretiva' and etapa == 'START_TO_REPAIR_END':
            duracao_h += random.uniform(10.0, 15.0)

        current_dt += timedelta(hours=duracao_h)
        status_log.append({'etapa_code': etapa, 'data_hora': current_dt.strftime('%Y-%m-%d %H:%M:%S')})

    return status_log

def gerar_dados_simulados(num_os: int = 50) -> List[Dict[str, Any]]:
    dados = []
    start_date = CONFIG["start_date"]

    for i in range(1, num_os + 1):
        tipo_servico = random.choice(['Preventiva', 'Corretiva', 'Garantia'])
        os_entry = {
            'os_id': f'OS-{1000 + i}',
            'placa_veiculo': f'ABC{random.randint(100, 999)}',
            'tipo_servico': tipo_servico,
            'entrada_dt': start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'status_log': _simular_etapas(tipo_servico, start_date)
        }
        dados.append(os_entry)
        start_date += timedelta(hours=random.uniform(1.0, 5.0))
    return dados

# --- FUNÇÕES DE ANÁLISE ---

def extrair_tempos_por_etapa(dados_json: List[Dict[str, Any]]) -> pd.DataFrame:
    registros = []
    for os in dados_json:
        registro = {'OS_ID': os['os_id'], 'TIPO_SERVICO': os['tipo_servico']}
        entrada = datetime.strptime(os['entrada_dt'], '%Y-%m-%d %H:%M:%S')
        anterior = entrada

        for log in os['status_log']:
            atual = datetime.strptime(log['data_hora'], '%Y-%m-%d %H:%M:%S')
            registro[log['etapa_code']] = (atual - anterior).total_seconds() / 3600
            anterior = atual

        registro['LEAD_TIME_TOTAL_H'] = (anterior - entrada).total_seconds() / 3600
        registros.append(registro)
    return pd.DataFrame(registros)

def identificar_gargalos(df: pd.DataFrame, top_n: int = 3) -> pd.Series:
    etapas = [e for e in ETAPAS.keys()]
    tempos_medios = df[etapas].mean().sort_values(ascending=False)
    return tempos_medios.head(top_n)

# --- VISUALIZAÇÃO ---

def gerar_grafico_pareto(tempos_medios: pd.Series) -> None:
    etapas_nome = {k: v[2] for k, v in ETAPAS.items()}
    df_pareto = tempos_medios.reset_index()
    df_pareto.columns = ['Etapa', 'Tempo_Medio_H']
    df_pareto['Etapa_Nome'] = df_pareto['Etapa'].map(etapas_nome)
    df_pareto['Percentual'] = (df_pareto['Tempo_Medio_H'] / df_pareto['Tempo_Medio_H'].sum()) * 100
    df_pareto['Acumulado'] = df_pareto['Percentual'].cumsum()

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.bar(df_pareto['Etapa_Nome'], df_pareto['Tempo_Medio_H'], color='skyblue')
    ax2 = ax1.twinx()
    ax2.plot(df_pareto['Etapa_Nome'], df_pareto['Acumulado'], color='red', marker='o')
    ax2.axhline(80, color='gray', linestyle=':')
    plt.title('Pareto - Gargalos no Processo de Serviço')
    plt.tight_layout()
    plt.show()

# --- PIPELINE PRINCIPAL ---

if __name__ == "__main__":
    dados = gerar_dados_simulados(CONFIG["volume_dados"])
    df = extrair_tempos_por_etapa(dados)

    print(f"Lead Time Médio: {df['LEAD_TIME_TOTAL_H'].mean():.2f}h")
    print(df.groupby('TIPO_SERVICO')['LEAD_TIME_TOTAL_H'].agg(['mean', 'std']))
    gargalos = identificar_gargalos(df)
    print("\nTop 3 Gargalos:")
    print(gargalos)
    gerar_grafico_pareto(gargalos)
