import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import unidecode  # para eliminar tildes

# Diccionario para colores
color_map = {
    "beige": "#F5F5DC",
    "marrón": "#A0522D",
    "marron": "#A0522D",
    "blanco": "#FFFFFF",
    "gris azul": "#6B7B8C",
    "gris oscuro": "#4B4B4B",
    "negro": "#000000",
    "marrón claro": "#CD853F",
    "marron claro": "#CD853F",
    "gris": "#808080",  # Asignar un gris válido
    # Puedes añadir más colores si es necesario
}

st.title("Columna Estratigráfica Interactiva")

uploaded_file = st.file_uploader("Carga un archivo Excel (.xlsx) con los datos estratigráficos", type=["xlsx"])

def normalize_col(col_name):
    # Pasar a minúsculas, quitar tildes y espacios
    return unidecode.unidecode(col_name.strip().lower().replace(" ", "").replace("_",""))

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Mostrar columnas detectadas para ayudar al usuario
        st.write("Columnas detectadas en el archivo:", df.columns.tolist())

        # Normalizamos columnas para hacer matching flexible
        norm_cols = {normalize_col(c): c for c in df.columns}

        # Definir qué columnas buscamos y sus nombres normalizados
        needed = {
            "profundidadinicio(m)": None,
            "profundidadfin(m)": None,
            "litologia": None,
            "color": None,
            "descripcion": None
        }

        # Mapear columnas
        for key in needed.keys():
            if key in norm_cols:
                needed[key] = norm_cols[key]
            else:
                st.error(f"No se encontró columna requerida similar a '{key}'")
                st.stop()

        # Renombrar df con nombres estándar para facilitar uso
        df = df.rename(columns={
            needed["profundidadinicio(m)"]: "Profundidad Inicio (m)",
            needed["profundidadfin(m)"]: "Profundidad Fin (m)",
            needed["litologia"]: "Litologia",
            needed["color"]: "Color",
            needed["descripcion"]: "Descripción"
        })

        # Añadir espesor (m) para los estratos
        df["Espesor (m)"] = df["Profundidad Fin (m)"] - df["Profundidad Inicio (m)"]

        # Normalizar color
        def obtener_color(c):
            c_lower = str(c).strip().lower()
            return color_map.get(c_lower, "#808080")  # Si no se encuentra, asignamos gris

        df["Color_hex"] = df["Color"].apply(obtener_color)

        # Crear figura de Plotly
        fig = go.Figure()

        # Tamaño fijo para cada estrato
        fixed_height = 20  # Ajustar el tamaño fijo que quieras para todos los estratos

        # Agregar cada estrato al gráfico
        for idx, row in df.iterrows():
            fig.add_shape(
                type="rect",
                x0=0, x1=1,
                y0=row["Profundidad Inicio (m)"],  # Mantener la profundidad inicial
                y1=row["Profundidad Inicio (m)"] + fixed_height,  # Usar el tamaño fijo
                fillcolor=row["Color_hex"],
                line=dict(color="black", width=1)
            )
            fig.add_annotation(
                x=0.5,
                y=(row["Profundidad Inicio (m)"] + (row["Profundidad Inicio (m)"] + fixed_height)) / 2,
                text=row["Litologia"],
                showarrow=False,
                font=dict(color="black", size=10),
                yanchor="middle",
                xanchor="center",
                textangle=90
            )
            fig.add_trace(go.Scatter(
                x=[0.5],
                y=[(row["Profundidad Inicio (m)"] + (row["Profundidad Inicio (m)"] + fixed_height)) / 2],
                mode="markers",
                marker=dict(size=30, color="rgba(0,0,0,0)"),
                hovertemplate=(
                    f"<b>{row['Litologia']}</b><br>" +
                    f"Profundidad: {row['Profundidad Inicio (m)']} - {row['Profundidad Fin (m)']} m<br>" +
                    f"Espesor: {row['Espesor (m)']} m<br>" +
                    f"Descripción: {row['Descripción']}"
                )
            ))

        fig.update_yaxes(
            title="Profundidad (m)",
            tickmode="array",
            tickvals=df["Profundidad Inicio (m)"],  # Establecer la escala de profundidades
            ticktext=df["Profundidad Inicio (m)"].astype(str),
            range=[0, df["Profundidad Inicio (m)"].max() + fixed_height * len(df)]
        )
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
