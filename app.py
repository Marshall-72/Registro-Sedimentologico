import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración
st.set_page_config(layout="wide")
st.title("Análisis Petrológico: Visualización de Litologías y Funciones")

# Cargar el archivo Excel
df = pd.read_excel("CE_procesado.xlsx")

# Calcular función dominante
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

# Renombrar 'Sentido de gradación' a 'Gradación'
if 'Sentido de gradación' in df_sig.columns:
    df_sig.rename(columns={'Sentido de gradación': 'Gradación'}, inplace=True)

# Clasificar la permeabilidad (numérica) como categoría
def clasificar_perm(valor):
    if valor >= 70:
        return 'Alta permeabilidad'
    elif valor >= 30:
        return 'Media permeabilidad'
    else:
        return 'Baja permeabilidad'

df_sig['Clasificación permeabilidad'] = df_sig['Permeabilidad (1-100)'].apply(clasificar_perm)

# ------------------------------------------------
# GRÁFICO 1: Dispersión Tamaño de grano vs Permeabilidad
# ------------------------------------------------
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

# ------------------------------------------------
# GRÁFICO 2: Sankey
# ------------------------------------------------
st.markdown("## Gráfico 2: Diagrama Sankey - Transición hacia Función Petrológica")

etapas = ['Litología única', 'Gradación', 'Clasificación permeabilidad', 'Función principal']
all_labels = []
source = []
target = []
value = []

# Validar existencia de columnas y construir conexiones
for i in range(len(etapas) - 1):
    origen = etapas[i]
    destino = etapas[i + 1]

    if origen not in df_sig.columns or destino not in df_sig.columns:
        st.warning(f"❗ Columna faltante: '{origen}' o '{destino}' no encontrada.")
        continue

    combinaciones = df_sig.groupby([origen, destino])['ESPESOR'].sum().reset_index(name='espesor_total')

    for _, row in combinaciones.iterrows():
        origen_val = row[origen]
        destino_val = row[destino]
        espesor = row['espesor_total']

        if origen_val not in all_labels:
            all_labels.append(origen_val)
        if destino_val not in all_labels:
            all_labels.append(destino_val)

        source.append(all_labels.index(origen_val))
        target.append(all_labels.index(destino_val))
        value.append(espesor)

# Crear gráfico Sankey
fig_sankey = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=all_labels,
        color="lightgray"
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color="rgba(0, 128, 128, 0.4)"
    )
)])

fig_sankey.update_layout(
    title_text="Sankey: De Litología a Función Petrológica (ponderado por espesor)",
    font_size=10
)

st.plotly_chart(fig_sankey, use_container_width=True)
