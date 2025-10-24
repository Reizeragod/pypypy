import plotly.express as px
import pandas as pd
import os
from typing import Dict

def gerar_grafico_pareto_plotly(tempos_medios: pd.Series, etapas: Dict[str, Dict[str, str]], output_path: str):
    df_pareto = tempos_medios.reset_index()
    df_pareto.columns = ["Etapa", "Tempo_Medio_H"]
    df_pareto["Etapa_Nome"] = df_pareto["Etapa"].map(lambda k: etapas[k]["nome"])
    df_pareto["Percentual"] = (df_pareto["Tempo_Medio_H"] / df_pareto["Tempo_Medio_H"].sum()) * 100
    df_pareto["Acumulado"] = df_pareto["Percentual"].cumsum()

    fig = px.bar(df_pareto, x="Etapa_Nome", y="Tempo_Medio_H", color="Tempo_Medio_H",
                 text_auto=".2f", title="Pareto - Gargalos no Processo de Serviço")
    fig.add_scatter(x=df_pareto["Etapa_Nome"], y=df_pareto["Acumulado"],
                    mode="lines+markers", name="Percentual Acumulado", yaxis="y2")

    fig.update_layout(
        yaxis2=dict(title="Percentual Acumulado (%)", overlaying="y", side="right", range=[0, 100]),
        xaxis_title="Etapas do Processo",
        yaxis_title="Tempo Médio (Horas)",
        template="plotly_white",
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.write_html(output_path)
    print(f"✅ Pareto exportado: {output_path}")
