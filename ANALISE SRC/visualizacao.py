import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
from typing import Dict, Optional, Literal, Union

DEFAULT_THEME = "plotly_white"
SUPPORTED_OUTPUTS = ("html", "png")

def _validar_entrada_pareto(tempos_medios: pd.Series, etapas: Dict[str, Dict[str, str]]) -> None:
    if not isinstance(tempos_medios, pd.Series):
        raise TypeError("❌ 'tempos_medios' deve ser um pandas.Series.")
    if not isinstance(etapas, dict):
        raise TypeError("❌ 'etapas' deve ser um dicionário com metadados das etapas.")
    if tempos_medios.empty:
        raise ValueError("❌ Nenhum dado encontrado em 'tempos_medios' para gerar o gráfico.")


def gerar_grafico_pareto_plotly(
    tempos_medios: pd.Series,
    etapas: Dict[str, Dict[str, str]],
    output_path: Optional[str] = None,
    titulo: str = "Análise de Pareto - Gargalos no Processo de Serviço",
    tema: str = DEFAULT_THEME,
    exportar_como: Literal["html", "png", "show"] = "show",
    mostrar_percentuais: bool = True,
    salvar_pasta: str = "outputs"
) -> Union[go.Figure, None]:
    """
    Gera gráfico de Pareto interativo (Plotly) e salva/exporta conforme configuração.

    Parâmetros:
    ----------
    - tempos_medios: pd.Series com tempos médios por etapa.
    - etapas: dicionário {codigo: {"nome": str, "descricao": str}}.
    - output_path: caminho para salvar o arquivo (se None, cria automaticamente).
    - titulo: título do gráfico.
    - tema: tema visual do Plotly (ex: 'plotly_dark', 'plotly_white').
    - exportar_como: 'show', 'html' ou 'png'.
    - mostrar_percentuais: exibir valores nas barras.
    - salvar_pasta: diretório padrão para exportação.
    """
    _validar_entrada_pareto(tempos_medios, etapas)

    df_pareto = tempos_medios.reset_index()
    df_pareto.columns = ["Etapa", "Tempo_Medio_H"]
    df_pareto["Etapa_Nome"] = df_pareto["Etapa"].map(lambda k: etapas[k]["nome"] if k in etapas else k)
    df_pareto["Percentual"] = (df_pareto["Tempo_Medio_H"] / df_pareto["Tempo_Medio_H"].sum()) * 100
    df_pareto["Acumulado"] = df_pareto["Percentual"].cumsum()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_pareto["Etapa_Nome"],
        y=df_pareto["Tempo_Medio_H"],
        name="Tempo Médio (Horas)",
        marker_color="cornflowerblue",
        text=df_pareto["Tempo_Medio_H"].round(2) if mostrar_percentuais else None,
        textposition="outside"
    ))

    fig.add_trace(go.Scatter(
        x=df_pareto["Etapa_Nome"],
        y=df_pareto["Acumulado"],
        name="Percentual Acumulado (%)",
        mode="lines+markers",
        line=dict(color="red", width=2, dash="dot"),
        yaxis="y2"
    ))

    fig.update_layout(
        title=dict(text=titulo, x=0.5, xanchor="center", font=dict(size=18)),
        xaxis=dict(title="Etapas do Processo", tickangle=45),
        yaxis=dict(title="Tempo Médio (Horas)", showgrid=True, gridcolor="lightgray"),
        yaxis2=dict(title="Percentual Acumulado (%)", overlaying="y", side="right", range=[0, 100]),
        template=tema,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        height=600,
        margin=dict(l=60, r=60, t=80, b=120),
    )

    fig.add_hline(y=80, line_dash="dot", line_color="gray", yref="y2")

    if exportar_como == "show":
        fig.show()
    else:
        os.makedirs(salvar_pasta, exist_ok=True)
        if output_path is None:
            output_path = os.path.join(salvar_pasta, f"pareto_{pd.Timestamp.now():%Y%m%d_%H%M%S}.{exportar_como}")

        if exportar_como not in SUPPORTED_OUTPUTS:
            raise ValueError(f"❌ Formato '{exportar_como}' não suportado. Use {SUPPORTED_OUTPUTS}.")

        if exportar_como == "html":
            fig.write_html(output_path)
        elif exportar_como == "png":
            fig.write_image(output_path)

        print(f"✅ Gráfico de Pareto exportado: {output_path}")

    return fig
