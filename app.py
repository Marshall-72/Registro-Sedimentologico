import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("Análisis Petrológico: Tamaño de Grano, Permeabilidad y Función Litológica")

# 🧾 Descripción e interpretación
st.markdown("## Descripción e Interpretación")
st.markdown("""
Este panel interactivo muestra dos visualizaciones clave para comprender el comportamiento petrológico de las litologías analizadas:

1. Un **gráfico de dispersión** que relaciona el **tamaño de grano** con la **permeabilidad**, codificado por la función dominante de cada estrato (reservorio, sello o roca generadora) y con tamaño proporcional al espesor.

2. Un **gráfico radar** que permite comparar visualmente la proporción relativa de función petrológica (% de probabilidad de ser reservorio, sello o generadora) para cada unidad litológica.

---

### Interpretaciones clave:

- Los **mejores reservorios** se encuentran en zonas de **alta permeabilidad y gran tamaño de grano**
- Las **rocas sello y generadoras** se agrupan en sectores de baja permeabilidad y grano fino
- La representación radar permite detectar litologías multifuncionales o especializadas por su distribución triangular
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

# 📊 Gráfico Scatter
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

# 📈 Gráfico Radar
st.markdown("## Comparación de Funciones Petrológicas por Litología")

df_radar = df_sig[['Litología única', '% Reservorio', '% Sello', '% Roca Madre']]

fig_radar = go.Figure()
for i, row in df_radar.iterrows():
    fig_radar.add_trace(go.Scatterpolar(
        r=[row['% Reservorio'], row['% Sello'], row['% Roca Madre']],
        theta=['Reservorio', 'Sello', 'Roca Generadora'],
        fill='toself',
        name=row['Litología única']
    ))

fig_radar.update_layout(
    title="Distribución de Funciones Petrológicas por Litología",
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 100])
    ),
    showlegend=True
)

st.plotly_chart(fig_radar, use_container_width=True)
