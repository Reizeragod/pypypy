import pandas as pd
from datetime import datetime
import json
import random

# --- SIMULAÇÃO DA BASE DE DADOS (Estrutura NoSQL/JSON) ---
def gerar_dados_simulados(num_os=30):
    """Gera dados simulados de Ordens de Serviço (OS) em formato JSON."""
    os_data = []
    
    # Simula 3 meses de operações
    start_date = datetime(2025, 7, 1)
    
    # Define as etapas e simula a duração média em horas
    etapas = {
        'CHECK_IN_TO_DIAG': (0.5, 2.0), # Tempo de espera e diagnóstico inicial
        'DIAG_TO_QUOTATION': (0.5, 3.0), # Elaboração do Orçamento
        'QUOTATION_TO_START': (1.0, 10.0), # **Ponto Crítico:** Espera por Aprovação/Peças
        'START_TO_REPAIR_END': (4.0, 24.0) # Reparo (maior variabilidade)
    }

    for i in range(1, num_os + 1):
        os_entry = {
            'os_id': f'OS-{1000 + i}',
            'entrada_dt': start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'status_log': []
        }
        
        current_dt = start_date
        
        for etapa, (min_h, max_h) in etapas.items():
            duracao_h = random.uniform(min_h, max_h)
            
            if etapa == 'QUOTATION_TO_START' and i % 5 == 0:
                 duracao_h *= 3 

            current_dt = current_dt.replace(minute=current_dt.minute + random.randint(1, 15))
            current_dt = current_dt.replace(hour=current_dt.hour + int(duracao_h), minute=current_dt.minute + int((duracao_h % 1) * 60))
            
            os_entry['status_log'].append({
                'etapa': etapa,
                'data_hora': current_dt.strftime('%Y-%m-%d %H:%M:%S')
            })

        os_data.append(os_entry)
        start_date = start_date.replace(hour=start_date.hour + random.randint(2, 6))

    return os_data

# --- FUNÇÃO DE ANÁLISE ---

def analisar_lead_time(dados_json):
    """Processa dados JSON, calcula Lead Time e identifica o gargalo."""
    
    registros = []
    
    for os in dados_json:
        entrada = datetime.strptime(os['entrada_dt'], '%Y-%m-%d %H:%M:%S')
        
        fim_reparo = datetime.strptime(os['status_log'][-1]['data_hora'], '%Y-%m-%d %H:%M:%S')
        
        lead_time_total = (fim_reparo - entrada).total_seconds() / 3600 # Total em horas
        
        tempos_etapas = {}
        momento_anterior = entrada
        
        for log in os['status_log']:
            momento_atual = datetime.strptime(log['data_hora'], '%Y-%m-%d %H:%M:%S')
            duracao = (momento_atual - momento_anterior).total_seconds() / 3600
            tempos_etapas[log['etapa']] = duracao
            momento_anterior = momento_atual

        registro = {
            'OS_ID': os['os_id'],
            'Lead_Time_Total_H': lead_time_total,
            **tempos_etapas
        }
        registros.append(registro)

    # Cria um DataFrame Pandas para facilitar a análise
    df = pd.DataFrame(registros)
    
    print("-" * 50)
    print(f"ANÁLISE DE {len(df)} ORDENS DE SERVIÇO")
    print("-" * 50)
    
    print("MÉTRICAS GERAIS:")
    print(f"  Lead Time Médio Total (horas): {df['Lead_Time_Total_H'].mean():.2f}h")
    print(f"  Desvio Padrão do Lead Time: {df['Lead_Time_Total_H'].std():.2f}h (indicador de variabilidade)")
    print("-" * 50)
    
    tempos_medios_etapas = df.drop(['OS_ID', 'Lead_Time_Total_H'], axis=1).mean().sort_values(ascending=False)
    
    print("GASTOS MÉDIOS DE TEMPO POR ETAPA (GARGALO - PARETO):")
    for etapa, tempo in tempos_medios_etapas.items():
        print(f"  - {etapa:<25}: {tempo:.2f} horas")

    print("-" * 50)
    print(f"DIAGNÓSTICO: O maior tempo médio consumido é em '{tempos_medios_etapas.index[0]}'.")
    print("Essa é a etapa candidata a ser o GARGALO PRINCIPAL (80% dos atrasos).")
    

# --- EXECUÇÃO DO PROGRAMA ---

dados_brutos_json = gerar_dados_simulados(num_os=50)
analisar_lead_time(dados_brutos_json)