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
