import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar tu archivo procesado
df = pd.read_excel("CE_procesado.xlsx")

# Determinar función dominante (>50%)
def funcion_principal(row):
    funciones = {
        'Reservorio': row['% Reservorio'],
        'Sello': row['% Sello'],
        'Roca Madre': row['% Roca Madre']
    }
    max_func = max(funciones, key=funciones.get)
    return max_func if funciones[max_func] > 50 else 'No significativa'

df['Función principal'] = df.apply(funcion_principal, axis=1)
df_sig = df[df['Función principal'] != 'No significativa']

# Crear gráfico interactivo
fig = px.scatter(
    df_sig,
    x='Tamaño de grano (1-100)',
    y='Permeabilidad (1-100)',
    color='Función principal',
    size='ESPESOR',
    hover_name='Litología única',
    title="Relación entre Tamaño de Grano y Permeabilidad",
    labels={
        'Tamaño de grano (1-100)': 'Tamaño de grano (1–100)',
        'Permeabilidad (1-100)': 'Permeabilidad (1–100)',
        'Función principal': 'Función dominante',
        'ESPESOR': 'Espesor (m)'
    }
)
fig.update_layout(height=600, width=900)
fig.show()
