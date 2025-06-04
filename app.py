import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Mapa de colores para convertir nombres a hex
color_map = {
    "beige": "#F5F5DC",
    "marrón": "#A0522D",
    "blanco": "#FFFFFF",
    "gris azul": "#6B7B8C",
    "gris oscuro": "#4B4B4B",
    "negro": "#000000",
    "marrón claro": "#CD853F",
    # Puedes añadir más colores si es necesario
}

st.title("Columna Estratigráfica Interactiva")

uploaded_file = st.file_uploader("Carga un archivo Excel (.xlsx) con los datos estratigráficos", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Validar columnas necesarias
        required_cols = ["Profundidad Inicio (m)", "Profundidad Fin (m)", "Litologia", "Color", "Descripción"]
        if not all(col in df.columns for col in required_cols):
            st.error(f"El archivo Excel debe contener las columnas: {', '.join(required_cols)}")
        else:
            df["Espesor (m)"] = df["Profundidad Fin (m)"] - df["Profundidad Inicio (m)"]

            def obtener_color(c):
                c_lower = str(c).strip().lower()
                return color_map.get(c_lower, c_lower)

            df["Color_hex"] = df["Color"].apply(obtener_color)

            fig = go.Figure()

            for idx, row in df.iterrows():
                fig.add_shape(
                    type="rect",
                    x0=0, x1=1,
                    y0=row["Profundidad Inicio (m)"],
                    y1=row["Profundidad Fin (m)"],
                    fillcolor=row["Color_hex"],
                    line=dict(color="black", width=1)
                )
                fig.add_annotation(
                    x=0.5,
                    y=(row["Profundidad Inicio (m)"] + row["Profundidad Fin (m)"]) / 2,
                    text=row["Litologia"],
                    showarrow=False,
                    font=dict(color="black", size=10),
                    yanchor="middle",
                    xanchor="center",
                    textangle=90
                )
                fig.add_trace(go.Scatter(
                    x=[0.5],
                    y=[(row["Profundidad Inicio (m)"] + row["Profundidad Fin (m)"]) / 2],
                    mode="markers",
                    marker=dict(size=30, color="rgba(0,0,0,0)"),
                    hovertemplate=(
                        f"<b>{row['Litologia']}</b><br>" +
                        f"Profundidad: {row['Profundidad Inicio (m)']} - {row['Profundidad Fin (m)']} m<br>" +
                        f"Espesor: {row['Espesor (m)']} m<br>" +
                        f"Descripción: {row['Descripción']}<br>" +
                        f"Facies: {row.get('Facies', 'N.D.')}<br>" +
                        f"Ambiente: {row.get('Ambiente', 'N.D.')}"
                    )
                ))

            fig.update_yaxes(autorange="reversed", title="Profundidad (m)", dtick=500)
            fig.update_xaxes(visible=False)
            fig.update_layout(
                height=900,
                width=350,
                margin=dict(l=20, r=20, t=40, b=20),
                title="Columna Estratigráfica",
                hovermode="closest"
            )

            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error al leer el archivo Excel: {e}")
else:
    st.info("Por favor, carga un archivo Excel (.xlsx) para visualizar la columna estratigráfica.")

