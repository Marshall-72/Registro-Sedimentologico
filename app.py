import streamlit as st
import pandas as pd

# Datos de ejemplo con Litología, Profundidad, Color y Descripción
data = {
    "Profundidad Inicio (m)": [0, 4, 554, 555, 1305, 1820, 1821, 2566, 3086, 3087, 3947, 4497, 4498, 5236],
    "Profundidad Fin (m)": [4, 554, 555, 1305, 1820, 1821, 2566, 3086, 3087, 3947, 4497, 4498, 5236, 5810],
    "Litología": [
        "Travertino", "Arenisca con piroclastos", "Yeso", "Arcosa", "Caliza", "Sal",
        "Arenisca de grano grueso", "Shale calcáreo", "Marga", "Arenisca con feldespatos",
        "Caliza", "Lutita", "Arenisca cuarzosa", "Caliza"
    ],
    "Color": [
        "beige", "marrón", "blanco", "marrón", "gris azul", "blanco",
        "beige", "negro", "marrón claro", "marrón", "gris oscuro", "gris", "beige", "gris oscuro"
    ],
    "Descripción": [
        "travertino beige de grano muy fino, con estratificación paralela",
        "arenisca con piroclastos marrón de grano fino subanguloso, con estratificación paralela",
        "yeso blanco de grano fino, con estratificación simple",
        "arcosa marrón de grano fino subredondeado, con estratificación cruzada",
        "caliza gris azulada mudstone, con estratificación simple y, con vetilleo",
        "sal blanca fibrosa de grano medio, con estratificación simple",
        "arenisca beige de grano grueso subanguloso, con estratificación cruzada",
        "shale calcáreo negro de grano subanguloso, con laminación fisible",
        "marga marrón de grano muy fino, con estratificación simple",
        "arenisca con feldespatos marrón de grano fino subanguloso, con estratificación paralela",
        "caliza gris oscura wackestone con biocalstos, con estratificación cóncava",
        "lutita gris de grano fino subanguloso, con estratificación paralela, y con una vetilla",
        "arenisca cuarzosa beige de grano fino subredondeado, con estratificación paralela",
        "caliza gris oscura mudstone, con estratificación cóncava"
    ]
}

# Convertir los datos a un DataFrame
df = pd.DataFrame(data)

# Definir una paleta de colores para las litologías
color_map = {
    "Travertino": "beige",
    "Arenisca con piroclastos": "marrón",
    "Yeso": "blanco",
    "Arcosa": "marrón",
    "Caliza": "gris azul",
    "Sal": "blanco",
    "Arenisca de grano grueso": "beige",
    "Shale calcáreo": "negro",
    "Marga": "marrón claro",
    "Arenisca con feldespatos": "marrón",
    "Lutita": "gris oscuro",
    "Arenisca cuarzosa": "beige",
}

# Agregar color a cada litología
df["Color Hex"] = df["Litología"].map(color_map)

# Crear la columna de Intervalo (Inicio - Fin)
df["Intervalo (m)"] = df["Profundidad Inicio (m)"].astype(str) + " - " + df["Profundidad Fin (m)"].astype(str)

# Remover la columna "Color Hex" ya que no la necesitamos
df = df.drop(columns=["Color Hex"])

# Crear la columna de Litología con imágenes
image_map = {
    "Travertino": "https://via.placeholder.com/50x50/8B4513/FFFFFF?text=T",  # Imagen de ejemplo
    "Arenisca con piroclastos": "https://via.placeholder.com/50x50/F4A300/FFFFFF?text=A",
    "Yeso": "https://via.placeholder.com/50x50/FFFFFF/000000?text=Y",
    "Arcosa": "https://via.placeholder.com/50x50/FF6347/FFFFFF?text=Ar",
    "Caliza": "https://via.placeholder.com/50x50/6A5ACD/FFFFFF?text=C",
    "Sal": "https://via.placeholder.com/50x50/FFF8DC/000000?text=S",
    "Arenisca de grano grueso": "https://via.placeholder.com/50x50/F0E68C/000000?text=AGG",
    "Shale calcáreo": "https://via.placeholder.com/50x50/708090/FFFFFF?text=SC",
    "Marga": "https://via.placeholder.com/50x50/D2B48C/FFFFFF?text=M",
    "Arenisca con feldespatos": "https://via.placeholder.com/50x50/DAA520/FFFFFF?text=AF",
    "Lutita": "https://via.placeholder.com/50x50/8B4513/FFFFFF?text=L",
    "Arenisca cuarzosa": "https://via.placeholder.com/50x50/F0E68C/000000?text=AC",
}

# Asignar la URL de la imagen correspondiente a cada litología
df["Litología Imagen"] = df["Litología"].map(image_map)

# Mostrar la tabla con los cambios aplicados
st.write("### Columna Estratigráfica")
st.dataframe(df)

# Mostrar descripción de la columna estratigráfica
st.write("""
    **Descripción de la Columna Estratigráfica**:
    Esta tabla muestra la estratificación de los diferentes estratos, con su correspondiente litología, 
    intervalos de profundidad y descripción. Las imágenes en la columna de Litología representan los materiales.
""")
