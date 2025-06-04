import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Título de la app
st.title("Columna Estratigráfica")

# Diccionario con los colores mapeados a sus valores hexadecimales
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
    "gris": "#808080"
}

# Subir archivo
uploaded_file = st.file_uploader("Sube tu archivo de datos", type=["xlsx", "csv"])

if uploaded_file is not None:
    # Leer el archivo
    if uploaded_file.name.endswith("xlsx"):
        data = pd.read_excel(uploaded_file)
    else:
        data = pd.read_csv(uploaded_file)

    # Mostrar los primeros datos
    st.write(data.head())

    # Reemplazar los colores con sus valores hexadecimales
    data['Color'] = data['Color'].apply(lambda x: color_map.get(x, '#808080'))  # Usar gris como valor por defecto

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(12, 10))

    # Longitud fija para todas las barras (ahora reducida un poco más)
    fixed_length = 4  # Aumento ligeramente el largo de las barras para más espacio

    # Inicializar la posición de la barra (y-axis)
    y_pos = np.arange(len(data))

    # Dibujar las barras con longitud fija y color correspondiente, sin espacio entre barras
    for i, row in data.iterrows():
        ax.barh(y_pos[i], fixed_length, height=0.9, color=row['Color'], align='center')  # height=0.9 para eliminar espacio

    # Ajustar la posición de las etiquetas de los intervalos para evitar solapamientos
    for i, row in data.iterrows():
        # Crear el intervalo de profundidad
        depth_interval = f"{row['Profundidad Inicio (m)']} - {row['Profundidad Fin (m)']}"
        
        # Colocar el intervalo a la izquierda de la barra, más alejado
        ax.text(-1.2, y_pos[i], depth_interval, va='center', fontsize=10, color='black')  # Desplazo más a la izquierda para evitar solapamiento
        
        # Agregar la descripción a la derecha de la barra
        ax.text(fixed_length + 0.1, y_pos[i] - 0.2, row['Descripcion'], va='center', fontsize=8, color='black')

    # Colocar el encabezado en la parte superior del gráfico utilizando plt.text()
    plt.text(0.5, 1.02, "Profundidad (m)              Litología                              Descripción            ", ha='center', va='center', fontsize=14, fontweight='bold', transform=ax.transAxes)
 
    # Eliminar el nombre del eje Y
    ax.set_ylabel('')  

    # Eliminar los números y el nombre del eje horizontal (eje X)
    ax.set_xticks([])  # Eliminar los ticks del eje X
    ax.set_xlabel('')  # Eliminar el nombre del eje X

    # Eliminar las etiquetas de los estratos en el eje Y
    ax.set_yticks([])  # Eliminar las etiquetas del eje Y

    # Eliminar las líneas de borde de la gráfica (spines)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Invertir el eje y para que los estratos más profundos estén abajo
    ax.invert_yaxis()

    # Ajustar el layout y mostrar la gráfica
    plt.tight_layout()
    st.pyplot(fig)
