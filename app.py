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
df["Color Hex"] = df["Color Hex"].apply(lambda x: f"background-color: {x}")

# Mostrar la tabla con colores aplicados
st.write("### Columna Estratigráfica")
st.dataframe(df.style.applymap(lambda x: 'background-color : ' + x, subset=["Color Hex"]).hide_columns())

# Mostrar descripción de la columna estratigráfica
st.write("""
    **Descripción de la Columna Estratigráfica**:
    Esta tabla muestra la estratificación de los diferentes estratos, con su correspondiente litología, 
    intervalos de profundidad y descripción.
""")
