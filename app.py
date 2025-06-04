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
    fig, ax = plt.subplots(figsize=(10, 10))

    # Inicializar la posición de la barra (y-axis)
    y_pos = np.arange(len(data))

    # Dibujar las barras de colores correspondientes a cada estrato en la parte izquierda
    for i, row in data.iterrows():
        ax.barh(y_pos[i], row['Espesor (m)'], height=0.9, color=row['Color'], align='center')

    # Agregar el espesor y la descripción a la derecha de cada barra
    for i, row in data.iterrows():
        ax.text(row['Espesor (m)'] + 0.05, y_pos[i], f"{row['Espesor (m)']} m", va='center', fontsize=10, color='black')
        ax.text(row['Espesor (m)'] + 0.05, y_pos[i] - 0.2, row['Descripcion'], va='center', fontsize=8, color='black')

    # Establecer los límites y etiquetas
    ax.set_xlabel('Espesor (m)')
    ax.set_ylabel('Estratos')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(data['Litologia'])
    ax.set_title('Columna Estratigráfica')

    # Invertir el eje y para que los estratos más profundos estén abajo
    ax.invert_yaxis()

    # Ajustar el layout y mostrar la gráfica
    plt.tight_layout()
    st.pyplot(fig)
