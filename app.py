import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(layout="wide")
st.title("Análisis Petrológico: Tamaño de Grano, Permeabilidad y Función Litológica")

# Descripción e interpretación
st.markdown("## Descripción e Interpretación")
st.markdown("""
Este panel interactivo muestra la relación entre el tamaño de grano y la permeabilidad de los estratos estudiados,
coloreado por la función dominante de cada uno (reservorio, sello, roca generadora), y con tamaño proporcional al espesor del estrato.
Solo se incluyen aquellos con más de 50 % de probabilidad en al menos una función, lo que permite visualizar de forma clara
las litologías con mayor potencial para cada rol dentro del sistema petrolífero.

**Interpretaciones clave**:
- Los reservorios se asocian a altos valores de permeabilidad y tamaño de grano.
- Las rocas sello se concentran en zonas de baja permeabilidad.
- Las rocas generadoras aparecen donde hay materia orgánica y baja permeabilidad.
""")

# Cargar datos
df = pd.read_excel("CE_procesado.xlsx")

# Calcular la función principal (> 50%)
def funcion_principal(row):
    funciones = {
        'Reservorio': row['% Reservorio'],
        'Sello': row['% Sello'],
        'Roca Madre': row['% Roca Madre']
    }
    top = max(funciones, key=funciones.get)
    return top if funciones[top] > 50 else 'No significativa'

df['Función principal'] = df.apply(funcion_principal, axis=1)
df_sig = df[df['Función principal'] != 'No significativa']

# Crear gráfico de dispersión
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

# Mostrar gráfico
st.plotly_chart(fig, use_container_width=True)
