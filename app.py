import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración general
st.set_page_config(layout="wide")
st.title("Análisis Petrológico: Litologías, Parámetros y Funciones")

# Cargar archivo Excel
df = pd.read_excel("CE_procesado.xlsx")

# Calcular función dominante (>50%)
def funcion_principal(row):
    funciones = {
        'Reservorio': row['% Reservorio'],
        'Sello': row['% Sello'],
        'Roca Madre': row['% Roca Madre']
    }
    top = max(funciones, key=funciones.get)
    return top if funciones[top] > 50 else 'No significativa'

df['Función principal'] = df.apply(funcion_principal, axis=1)
df_sig = df[df['Función principal'] != 'No significativa'].copy()

# Renombrar si es necesario
if 'Sentido de gradación' in df_sig.columns:
    df_sig.rename(columns={'Sentido de gradación': 'Gradación'}, inplace=True)

# Clasificar permeabilidad
def clasificar_perm(valor):
    if valor >= 70:
        return 'Alta permeabilidad'
    elif valor >= 30:
        return 'Media permeabilidad'
    else:
        return 'Baja permeabilidad'

df_sig['Clasificación permeabilidad'] = df_sig['Permeabilidad (1-100)'].apply(clasificar_perm)

# ------------------------------
# GRÁFICO 1: Dispersión
# ------------------------------
st.markdown("## Gráfico 1: Tamaño de Grano vs. Permeabilidad")

fig_scatter = px.scatter(
    df_sig,
    x='Tamaño de grano (1-100)',
    y='Permeabilidad (1-100)',
    color='Función principal',
    size='ESPESOR',
    hover_name='Litología única',
    title="Relación entre Tamaño de Grano y Permeabilidad (funciones > 50%)",
    labels={
        'Tamaño de grano (1-100)': 'Tamaño de grano',
        'Permeabilidad (1-100)': 'Permeabilidad',
        'ESPESOR': 'Espesor (m)'
    }
)
st.plotly_chart(fig_scatter, use_container_width=True)

# ------------------------------
# GRÁFICOS 2–4: Función por litología
# ------------------------------
st.markdown("## Gráfico 2: Probabilidad de Función por Litología")

def graficar_funcion(df, columna, titulo, color):
    if columna not in df.columns:
        st.warning(f"❗ La columna '{columna}' no existe.")
        return
    if 'Litología única' not in df.columns:
        st.warning("❗ La columna 'Litología única' no existe.")
        return

    df_filtrado = df[df[columna] > 0].copy()
    if df_filtrado.empty:
        st.info(f"No hay registros con {columna} > 0.")
        return

    df_filtrado = df_filtrado.sort_values(by=columna, ascending=True)

    fig = px.bar(
        df_filtrado,
        x=columna,
        y='Litología única',
        orientation='h',
        title=titulo,
        color_discrete_sequence=[color],
        labels={columna: "Probabilidad (%)", 'Litología única': 'Litología (con profundidad)'}
    )
    st.plotly_chart(fig, use_container_width=True)

# Gráfico Roca Sello
graficar_funcion(df, '% Sello', "Probabilidad de Función: Roca Sello", "orange")

# Gráfico Roca Madre
graficar_funcion(df, '% Roca Madre', "Probabilidad de Función: Roca Madre", "brown")

# Gráfico Roca Reservorio
graficar_funcion(df, '% Reservorio', "Probabilidad de Función: Roca Reservorio", "green")
