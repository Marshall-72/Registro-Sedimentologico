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

    # Longitud fija para todas las barras (ahora reducida a la mitad)
    fixed_length = 5  # Reducción de la longitud a la mitad (5 metros de longitud fija)

    # Inicializar la posición de la barra (y-axis)
    y_pos = np.arange(len(data))

    # Dibujar las barras con longitud fija y color correspondiente, sin espacio entre barras
    for i, row in data.iterrows():
        ax.barh(y_pos[i], fixed_length, height=1.0, color=row['Color'], align='center')  # height=1.0 para eliminar espacio

    # Agregar el espesor y la descripción a la izquierda de cada barra
    for i, row in data.iterrows():
        # Colocar la etiqueta de espesor a la izquierda de la barra
        ax.text(-0.2, y_pos[i], f"{row['Espesor (m)']} m", va='center', fontsize=10, color='black')
        
        # Agregar la descripción a la derecha de la barra
        ax.text(fixed_length + 0.05, y_pos[i] - 0.2, row['Descripcion'], va='center', fontsize=8, color='black')

    # Colocar las etiquetas de los contactos entre las barras en las profundidades de fin
    for i in range(1, len(data)):  # Comenzar desde el segundo estrato para marcar el contacto
        # Profundidad de contacto entre estratos (fin del estrato anterior)
        depth_contact = data.loc[i, 'Profundidad Inicio (m)']
        
        # Colocamos la etiqueta unos centímetros más arriba
        ax.text(-0.3, y_pos[i] + 0.1, f"{depth_contact} m", va='center', fontsize=10, color='black')  # Ajustamos la posición vertical

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
