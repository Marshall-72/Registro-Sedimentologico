import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import unidecode  # para eliminar tildes

# Diccionario de colores para litología
color_map = {
    "Arenisca": "#D2B48C",  # Color beige para Arenisca
    "Lutita": "#8B4513",  # Marrón para Lutita
    "Caliza": "#F5F5F5",  # Blanco para Caliza
    "Shale calcáreo": "#A9A9A9",  # Gris para Shale calcáreo
    "Arcosa": "#A0522D",  # Marrón claro para Arcosa
    "Sal": "#FFF8DC",  # Amarillo claro para Sal
}

# Diccionario para patrones de cada litología (simulados)
pattern_map = {
    "Arenisca": "/",
    "Lutita": "x",
    "Caliza": "|",
    "Shale calcáreo": "-",
    "Arcosa": "+",
    "Sal": "*",
}

st.title("Columna Estratigráfica Interactiva")

uploaded_file = st.file_uploader("Carga un archivo Excel (.xlsx) con los datos estratigráficos", type=["xlsx"])

def normalize_col(col_name):
    return unidecode.unidecode(col_name.strip().lower().replace(" ", "").replace("_",""))

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Mostrar las columnas del archivo
        st.write("Columnas detectadas en el archivo:", df.columns.tolist())

        # Normalizamos columnas para hacer matching flexible
        norm_cols = {normalize_col(c): c for c in df.columns}

        # Definir las columnas necesarias
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

        # Renombrar columnas para su uso
        df = df.rename(columns={
            needed["profundidadinicio(m)"]: "Profundidad Inicio (m)",
            needed["profundidadfin(m)"]: "Profundidad Fin (m)",
            needed["litologia"]: "Litologia",
            needed["color"]: "Color",
            needed["descripcion"]: "Descripción"
        })

        df["Espesor (m)"] = df["Profundidad Fin (m)"] - df["Profundidad Inicio (m)"]

        def obtener_color(c):
            c_lower = str(c).strip().lower()
            return color_map.get(c_lower, "#808080")

        df["Color_hex"] = df["Color"].apply(obtener_color)

        fig = go.Figure()

        # Establecer un tamaño fijo para los estratos
        fixed_height = 20  # Ajustar el tamaño fijo que quieras para todos los estratos

        # Agregar cada estrato al gráfico con un patrón
        for idx, row in df.iterrows():
            pattern = pattern_map.get(row["Litologia"], "/")  # Si no encuentra patrón, usa "/"
            
            fig.add_shape(
                type="rect",
                x0=0, x1=1,
                y0=row["Profundidad Inicio (m)"],
                y1=row["Profundidad Inicio (m)"] + fixed_height,
                fillcolor=row["Color_hex"],
                line=dict(color="black", width=1),
                opacity=0.6  # Control de opacidad para los patrones
            )
            
            # Agregar la textura como patrón (simulación visual usando hatch)
            fig.add_shape(
                type="rect",
                x0=0, x1=1,
                y0=row["Profundidad Inicio (m)"],
                y1=row["Profundidad Inicio (m)"] + fixed_height,
                line=dict(color="black", width=1),
                fillcolor="rgba(255,255,255,0)",  # Transparente para que el patrón se vea
                opacity=0.5,
                pattern_shape=pattern,
                pattern_density=0.1  # Cambiar la densidad del patrón
            )

            # Añadir anotación con Litología
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

            # Agregar trace con el texto informativo
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

        # Mostrar una tabla de las litologías y sus patrones
        st.write("Tabla de Litologías y Patrones")
        st.dataframe(df[["Litologia", "Color", "Descripción"]])

    except Exception as e:
        st.error(f"Error al leer el archivo Excel: {e}")
else:
    st.info("Por favor, carga un archivo Excel (.xlsx) para visualizar la columna estratigráfica.")

