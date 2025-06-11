import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

st.set_page_config(layout="wide")
st.title("Sistema de Petróleo Chonta-Vivian")

fig, ax = plt.subplots(figsize=(16, 8))
ax.set_xlim(0, 20)
ax.set_ylim(0, 9)
ax.axis('off')

# Tiempos geológicos y colores
tiempos = ["TRIASICO", "JURASICO", "CRETACEO", "TERCIARIO"]
subtiempos = [["INF", "MED"], ["INF", "MED", "SUP"], ["INF", "SUP"], ["Paleog", "Neógeno"]]
x_pos = [0, 2, 5, 10]
anchos = [2, 3, 5, 10]
colors_tiempo = ['orchid', 'skyblue', 'mediumseagreen', 'gold']

for i, (t, x, w, c) in enumerate(zip(tiempos, x_pos, anchos, colors_tiempo)):
    ax.add_patch(patches.Rectangle((x, 8.5), w, 0.5, color=c, ec='black'))
    ax.text(x + w / 2, 8.75, t, ha='center', va='center', fontsize=9, weight='bold')

sub_x = 0
for i, sublist in enumerate(subtiempos):
    dx = anchos[i] / len(sublist)
    for sub in sublist:
        ax.add_patch(patches.Rectangle((sub_x, 8), dx, 0.5, color='white', ec='black'))
        ax.text(sub_x + dx / 2, 8.25, sub, ha='center', va='center', fontsize=8)
        sub_x += dx

# Unidades
unidades = ["Pucara", "Sarayaquillo", "Cu", "Ra", "AC", "Cho", "Vi", "Ca", "Vi", "Ya", "Po", "Cha", "Ma", "Co"]
pos_x = [0.5, 2.5, 4, 5, 5.5, 6, 6.5, 7, 7.5, 8, 9, 10, 11, 12]
for x, u in zip(pos_x, unidades):
    ax.text(x, 7.7, u, ha='center', va='center', fontsize=8)

# Eventos
eventos = ["UNIDAD", "ROCA MADRE", "RESERVORIO", "SELLO", "SOTERRAMIENTO",
           "TRAMPAS", "GEN / MIGR / ACUM", "PRESERVACION", "MOMENTO CRÍTICO"]
y_labels = np.arange(7.2, 0, -0.8)
for y, e in zip(y_labels, eventos):
    ax.text(-0.5, y, e, ha='right', va='center', fontsize=9)

barras = [
    (4.8, 6.4, 2, 0.6, 'yellow'), (5.2, 5.6, 2.5, 0.6, 'peru'),
    (6.5, 4.8, 3.5, 0.6, 'orange'), (9.5, 4.0, 3, 0.6, 'dodgerblue'),
    (10, 3.2, 2, 0.6, 'red'), (11, 2.4, 3, 0.6, 'darkred'), (13, 1.6, 2, 0.6, 'lightblue')
]
for x, y, w, h, c in barras:
    ax.add_patch(patches.Rectangle((x, y), w, h, color=c, ec='black'))

# Flecha momento crítico
ax.annotate('', xy=(15.5, 1.0), xytext=(15.5, 0.5),
            arrowprops=dict(facecolor='blue', edgecolor='black', width=6, headwidth=15))

# Título
ax.text(10, -0.3, "Fig. 4 - Sistema de Petróleo Chonta-Vivian", fontsize=11, ha='center')

st.pyplot(fig)
