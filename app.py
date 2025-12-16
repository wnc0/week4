import streamlit as st
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# 1️⃣ Load CSV Palette
# ----------------------------
@st.cache_data
def load_palettes():
    df = pd.read_csv("colors.csv")

    palette_dict = {}
    for _, row in df.iterrows():
        rgb = (row["r"]/255, row["g"]/255, row["b"]/255)
        palette_dict[row["name"]] = rgb

    # 每个颜色名 = 一个主题（单色极简）
    palettes = {name: [rgb] for name, rgb in palette_dict.items()}
    return palettes

PALETTES = load_palettes()

# ----------------------------
# 2️⃣ Blob generator
# ----------------------------
def blob(center=(0.5, 0.5), r=0.2, points=150, wobble=0.1):
    angles = np.linspace(0, 2*np.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# ----------------------------
# 3️⃣ Poster generation
# ----------------------------
def generate_poster(theme, wobble_val):
    fig, ax = plt.subplots(figsize=(7, 10))
    ax.set_facecolor((0.98, 0.98, 0.97))
    ax.axis("off")

    palette = PALETTES[theme]
    n_layers = 12

    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.1, 0.35)
        x, y = blob(center=(cx, cy), r=rr, wobble=wobble_val)
        color = random.choice(palette)
        alpha = random.uniform(0.2, 0.5)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor="none")

    # 随机小编号签名
    for _ in range(3):
        ax.text(
            random.uniform(0.05, 0.9),
            random.uniform(0.05, 0.95),
            f"#{random.randint(100, 999)}",
            fontsize=8,
            color=random.choice(palette),
            alpha=0.7
        )

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return fig

# ----------------------------
# 4️⃣ Streamlit UI
# ----------------------------
st.title("CSV Palette Generative Poster")

theme = st.selectbox("Color Theme", list(PALETTES.keys()))
wobble_val = st.slider(
    "Blob Wobble",
    min_value=0.01,
    max_value=0.3,
    value=0.1,
    step=0.01
)

if st.button("Generate Poster"):
    fig = generate_poster(theme, wobble_val)
    st.pyplot(fig)
