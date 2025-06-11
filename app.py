import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Análisis Petrológico: Tamaño de Grano, Permeabilidad y Función Litológica")

# 🧾 Descripción e interpretación
st.markdown("## Descripción e Interpretación")
st.markdown("""
Este panel interactivo muestra dos visualizaciones clave para comprender el comportamiento petrológico de las litologías analizadas:

1. Un **gráfico de dispersión** que relaciona el **tamaño de grano** con la **permeabilidad**, codificado por la función dominante de cada estrato (reservorio, sello o roca generadora) y con tamaño proporcional al espesor.

2. Un **gráfico de barras agrupadas** que permite comparar visualmente la proporción relativa de función petrológica (% de probabilidad de ser reservorio, sello o generadora) para cada unidad litológica.

---

### Interpretaciones clave:

- Los **mejores reservorios** se encuentran en zonas de **alta permeabilidad y gran tamaño de grano**
- Las **rocas sello y generadoras** se agrupan en sectores de baja permeabilidad y grano fino
- La comparación por barras permite distinguir litologías multifuncionales o especializadas
""")

# 📥 Cargar datos
df = pd.read_excel("CE_procesado.xlsx")

# 🧠 Función dominante si no está calculada
def funcion_principal(row):
    funciones = {
        'Reservorio': row['% Reservorio'],
        'Sello': row['% Sello'],
        'Roca Madre': row['% Roca Madre']
    }
    top = max(funciones, key=funciones.get)
    return top if funciones[top] > 50 else 'No significativa'

if 'Función principal' not in df.columns:
    df['Función principal'] = df.apply(funcion_principal, axis=1)

df_sig = df[df['Función principal'] != 'No significativa']

# 📊 Gráfico de dispersión
fig = px.scatter(
    df_sig,
    x='Tamaño de grano (1-100)',
    y='Permeabilidad (1-100)',
    color='Función principal',
    size='ESPESOR',
    hover_name='Litología única',
    title="Relación entre Tamaño de Grano y Permeabilidad",
    labels={
        'Tamaño de grano (1-100)': 'Tamaño de grano',
        'Permeabilidad (1-100)': 'Permeabilidad',
        'ESPESOR': 'Espesor (m)'
    }
)
st.plotly_chart(fig, use_container_width=True)

# 📊 Gráfico de barras agrupadas con filtro >50%
st.markdown("## Porcentaje de Función Petrológica por Litología (Solo funciones significativas > 50%)")

# Filtrar litologías con al menos una función > 50%
df_bar = df.copy()
df_bar = df_bar[
    (df_bar['% Reservorio'] > 50) |
    (df_bar['% Sello'] > 50) |
    (df_bar['% Roca Madre'] > 50)
]

df_bar = df_bar[['Litología única', '% Reservorio', '% Sello', '% Roca Madre']]
df_bar = df_bar.melt(
    id_vars='Litología única',
    value_vars=['% Reservorio', '% Sello', '% Roca Madre'],
    var_name='Función',
    value_name='Porcentaje'
)

fig_bar = px.bar(
    df_bar,
    x='Litología única',
    y='Porcentaje',
    color='Función',
    barmode='group',
    title="Comparación de Funciones Petrológicas por Litología (>50%)",
    labels={'Litología única': 'Litología'}
)

fig_bar.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_bar, use_container_width=True)
