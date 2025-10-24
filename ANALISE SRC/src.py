import yaml
from simulador import gerar_dados_simulados, ETAPAS
from analise import extrair_tempos_por_etapa, identificar_gargalos
from visualizacao import gerar_grafico_pareto_plotly
import pandas as pd
import os

with open("src/config.yaml", "r") as f:
    CONFIG = yaml.safe_load(f)

def main():
    print("🚀 Iniciando simulação...")
    dados = gerar_dados_simulados(CONFIG["NUM_OS"])
    df = extrair_tempos_por_etapa(dados)

    output_csv = os.path.join("data", "analise_oficina.csv")
    os.makedirs("data", exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"✅ Dados salvos em {output_csv}")

    lead_time_medio = df["LEAD_TIME_TOTAL_H"].mean()
    print(f"\n📊 Lead Time Médio Total: {lead_time_medio:.2f}h")

    gargalos = identificar_gargalos(df, ETAPAS)
    print("\n🔥 Top Gargalos:\n", gargalos)

    gerar_grafico_pareto_plotly(gargalos, ETAPAS, "reports/pareto_gargalos.html")

if __name__ == "__main__":
    main()
