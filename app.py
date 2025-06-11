import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Tamaño de Grano vs. Permeabilidad")

# Cargar Excel local
df = pd.read_excel("CE_procesado.xlsx")

# Calcular función principal si no existe
def funcion_principal(row):
    funcs = {'Reservorio': row['% Reservorio'], 'Sello': row['% Sello'], 'Roca Madre': row['% Roca Madre']}
    top = max(funcs, key=funcs.get)
    return top if funcs[top] > 50 else 'No significativa'

if 'Función principal' not in df.columns:
    df['Función principal'] = df.apply(funcion_principal, axis=1)

df_sig = df[df['Función principal'] != 'No significativa']

# Gráfico interactivo
fig = px.scatter(
    df_sig,
    x='Tamaño de grano (1-100)',
    y='Permeabilidad (1-100)',
    color='Función principal',
    size='ESPESOR',
    hover_name='Litología única',
    title="Tamaño de Grano vs. Permeabilidad",
    labels={
        'Tamaño de grano (1-100)': 'Tamaño de grano',
        'Permeabilidad (1-100)': 'Permeabilidad',
        'ESPESOR': 'Espesor (m)'
    }
)

st.plotly_chart(fig, use_container_width=True)
