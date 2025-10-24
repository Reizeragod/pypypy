import pandas as pd
from datetime import datetime, timedelta
import random
import json
import matplotlib.pyplot as plt

# --- CONFIGURAÇÃO E SIMULAÇÃO DE DADOS (NO-SQL/JSON) ---

ETAPAS = {
    'CHECK_IN_TO_DIAG': (1.0, 3.0, 'Espera/Diagnóstico Inicial'),
    'DIAG_TO_QUOTATION': (0.5, 2.0, 'Elaboração Orçamento'),
    'QUOTATION_TO_START': (2.0, 15.0, 'Aprovação Cliente/Espera Peças'), 
    'START_TO_REPAIR_END': (5.0, 30.0, 'Reparo na Baia')
}

def gerar_dados_simulados_v2(num_os=50):
    """Gera dados simulados de 50 Ordens de Serviço em formato NoSQL (JSON)."""
    os_data = []
    start_date = datetime(2025, 7, 1, 8, 0, 0) 
    
    for i in range(1, num_os + 1):
        os_entry = {
            'os_id': f'OS-{1000 + i}',
            'placa_veiculo': f'ABC{random.randint(100, 999)}',
            'tipo_servico': random.choice(['Preventiva', 'Corretiva', 'Garantia']),
            'entrada_dt': start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'status_log': []
        }
        
        current_dt = start_date
        
        for etapa, (min_h, max_h, _) in ETAPAS.items():
            duracao_h = random.uniform(min_h, max_h)

            if etapa == 'QUOTATION_TO_START' and random.random() < 0.35: 
                 duracao_h += random.uniform(15.0, 48.0) 
            if os_entry['tipo_servico'] == 'Corretiva' and etapa == 'START_TO_REPAIR_END':
                 duracao_h += random.uniform(10.0, 15.0) 

            current_dt += timedelta(hours=duracao_h)
            
            os_entry['status_log'].append({
                'etapa_code': etapa,
                'data_hora': current_dt.strftime('%Y-%m-%d %H:%M:%S')
            })

        os_data.append(os_entry)
        start_date += timedelta(hours=random.uniform(1.0, 5.0))

    return os_data

# --- FUNÇÕES DE ANÁLISE E TRATAMENTO DE DADOS  ---

def extrair_tempos_por_etapa(dados_json):
    """Calcula a duração de cada sub-etapa em horas e retorna um DataFrame."""
    registros = []
    
    for os in dados_json:
        registro = {'OS_ID': os['os_id'], 'TIPO_SERVICO': os['tipo_servico']}
        entrada = datetime.strptime(os['entrada_dt'], '%Y-%m-%d %H:%M:%S')
        momento_anterior = entrada
        
        for log in os['status_log']:
            momento_atual = datetime.strptime(log['data_hora'], '%Y-%m-%d %H:%M:%S')
            duracao_h = (momento_atual - momento_anterior).total_seconds() / 3600
            
            registro[log['etapa_code']] = duracao_h
            momento_anterior = momento_atual

        registro['LEAD_TIME_TOTAL_H'] = (momento_anterior - entrada).total_seconds() / 3600
        registros.append(registro)

    return pd.DataFrame(registros)

def gerar_grafico_pareto(tempos_medios, df_analise):
    """Gera um Gráfico de Pareto para visualização dos gargalos."""
    
    df_pareto = tempos_medios.reset_index()
    df_pareto.columns = ['Etapa', 'Tempo_Medio_H']
    df_pareto['Etapa_Nome'] = df_pareto['Etapa'].map({code: nome for code, _, nome in ETAPAS.values()})
    
    df_pareto['Contribuicao_Total'] = df_pareto['Tempo_Medio_H'].sum()
    df_pareto['Percentual'] = (df_pareto['Tempo_Medio_H'] / df_pareto['Contribuicao_Total']) * 100
    df_pareto['Acumulado'] = df_pareto['Percentual'].cumsum()
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    ax1.bar(df_pareto['Etapa_Nome'], df_pareto['Tempo_Medio_H'], color='skyblue')
    ax1.set_xlabel('Etapas do Processo de Serviço')
    ax1.set_ylabel('Tempo Médio Gasto (Horas)', color='skyblue')
    ax1.tick_params(axis='y', labelcolor='skyblue')
    ax1.tick_params(axis='x', rotation=45)
    
    ax2 = ax1.twinx()
    ax2.plot(df_pareto['Etapa_Nome'], df_pareto['Acumulado'], color='red', marker='o', linestyle='--')
    ax2.set_ylabel('Percentual Acumulado (%)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.axhline(80, color='gray', linestyle=':') 

    plt.title('Análise de Pareto: Identificação de Gargalos no Processo de Serviço')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# --- EXECUÇÃO DO PROJETO DE ANÁLISE ---

dados_brutos_json = gerar_dados_simulados_v2(num_os=100) 

df_analise = extrair_tempos_por_etapa(dados_brutos_json)

lead_time_medio = df_analise['LEAD_TIME_TOTAL_H'].mean()
lead_time_std = df_analise['LEAD_TIME_TOTAL_H'].std()

lead_time_por_tipo = df_analise.groupby('TIPO_SERVICO')['LEAD_TIME_TOTAL_H'].agg(['mean', 'std'])

print("=" * 70)
print(f"DIAGNÓSTICO INICIAL DE SERVIÇOS ({len(df_analise)} Ordens de Serviço Analisadas)")
print("=" * 70)
print(f"KPI PRINCIPAL: Lead Time Médio Total: {lead_time_medio:.2f} horas")
print(f"Variabilidade (Desvio Padrão): {lead_time_std:.2f} horas")
print("\n")

print("MÉTRICAS DETALHADAS POR TIPO DE SERVIÇO:")
print(lead_time_por_tipo.rename(columns={'mean': 'Média (h)', 'std': 'Desvio Padrão (h)'}))
print("\n")

etapas_analise = [e for e in ETAPAS.keys()]
tempos_medios_etapas = df_analise[etapas_analise].mean().sort_values(ascending=False)

print("ANÁLISE DE TEMPO POR ETAPA (IDENTIFICANDO O GARGALO):")
for code, tempo in tempos_medios_etapas.items():
    nome_etapa = next(nome for c, m, nome in ETAPAS.values() if c == code)
    print(f"  - {nome_etapa:<30}: {tempo:.2f} horas")
print("-" * 70)

# Gerar a Visualização 
gerar_grafico_pareto(tempos_medios_etapas, df_analise)