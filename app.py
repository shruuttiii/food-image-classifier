import streamlit as st
import numpy as np
import json
import time
import base64
from io import BytesIO
from PIL import Image
import plotly.graph_objects as go
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image

from nutrition_data import get_nutrition


def image_to_base64(img: Image.Image) -> str:
    buffered = BytesIO()
    img.convert("RGB").save(buffered, format="JPEG", quality=88)
    return base64.b64encode(buffered.getvalue()).decode()

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="FoodLens | Food Classifier & Nutrition Estimator",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------------------------------
# DESIGN TOKENS — "Porcelain & Brass"
# ----------------------------------------------------------------------------
IVORY = "#F6F1E7"
WHITE = "#FFFFFF"
EMERALD = "#1B4332"
EMERALD_SOFT = "#2D6A4F"
BRASS = "#B8860B"
WINE = "#7B241C"
TEXT_INK = "#2B2118"
TEXT_MUTED = "#8B8378"
BORDER = "#E5DDCC"

# ----------------------------------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=Space+Mono:wght@400;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background: {IVORY};
    }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header[data-testid="stHeader"] {{background: transparent;}}

    h1, h2, h3, p, span, label, div {{
        color: {TEXT_INK};
    }}

    .eyebrow {{
        font-family: 'Space Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: {BRASS};
        margin-bottom: 0.3rem;
    }}
    .hero-title {{
        font-family: 'Fraunces', serif;
        font-weight: 600;
        font-size: 3rem;
        color: {EMERALD};
        margin: 0;
        line-height: 1.1;
    }}
    .hero-subtitle {{
        font-family: 'Inter', sans-serif;
        color: {TEXT_MUTED};
        font-size: 1.02rem;
        margin-top: 0.6rem;
        margin-bottom: 0.5rem;
        max-width: 640px;
    }}
    .hero-rule {{
        border: none;
        border-top: 1px solid {BORDER};
        margin: 1.6rem 0 2rem 0;
    }}

    .section-label {{
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: {BRASS};
        margin-bottom: 0.8rem;
    }}

    section[data-testid="stFileUploaderDropzone"] {{
        background: {WHITE} !important;
        border: 1.5px dashed {BRASS} !important;
        border-radius: 6px !important;
    }}
    section[data-testid="stFileUploaderDropzone"] div,
    section[data-testid="stFileUploaderDropzone"] span,
    section[data-testid="stFileUploaderDropzone"] small {{
        color: {TEXT_INK} !important;
    }}
    section[data-testid="stFileUploaderDropzone"] button {{
        background: {EMERALD} !important;
        color: {WHITE} !important;
        border: none !important;
    }}

    .plate-card {{
        background: {WHITE};
        border-radius: 6px;
        padding: 1.8rem;
        position: relative;
        box-shadow: 0 4px 18px rgba(43, 33, 24, 0.06);
        border: 1px solid {BORDER};
    }}
    .plate-card::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 6px 6px 0 0;
        background: linear-gradient(90deg, {BRASS}, {EMERALD}, {WINE});
    }}
    .predicted-food {{
        font-family: 'Fraunces', serif;
        font-weight: 700;
        font-size: 2.3rem;
        color: {EMERALD};
        margin: 0;
        text-transform: capitalize;
    }}
    .confidence-line {{
        font-family: 'Space Mono', monospace;
        font-size: 0.85rem;
        color: {TEXT_MUTED};
        margin-top: 0.3rem;
    }}
    .confidence-value {{
        color: {BRASS};
        font-weight: 700;
    }}

    .stat-card {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 6px;
        padding: 1rem 0.5rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(43, 33, 24, 0.04);
    }}
    .stat-value {{
        font-family: 'Space Mono', monospace;
        font-size: 1.5rem;
        font-weight: 700;
        color: {EMERALD};
    }}
    .stat-label {{
        font-family: 'Space Mono', monospace;
        color: {TEXT_MUTED};
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.2rem;
    }}
    .serving-note {{
        font-family: 'Inter', sans-serif;
        font-size: 0.82rem;
        color: {TEXT_MUTED};
        margin-top: 0.9rem;
        font-style: italic;
    }}

    div[data-testid="stHorizontalBlock"] .stButton>button {{
        background: {WHITE};
        color: {TEXT_MUTED};
        border: 1px solid {BORDER};
        border-radius: 999px;
        padding: 0.4rem 0;
        font-family: 'Space Mono', monospace;
        font-weight: 700;
        font-size: 0.85rem;
        width: 100%;
    }}
    div[data-testid="stHorizontalBlock"] .stButton>button:hover {{
        border-color: {BRASS};
        color: {BRASS};
    }}

    /* ---------- Upload badge icon ---------- */
    .upload-icon-badge {{
        width: 46px;
        height: 46px;
        border-radius: 50%;
        background: {IVORY};
        border: 1.5px solid {BORDER};
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        margin-bottom: 0.6rem;
    }}

    /* ---------- Cropped preview image ---------- */
    .preview-img-wrap img {{
        border-radius: 10px;
        box-shadow: 0 6px 20px rgba(43, 33, 24, 0.14);
        border: 1px solid {BORDER};
    }}

    /* ---------- Top-3 prediction cards ---------- */
    .pred-card {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 0.7rem 1rem;
        margin-bottom: 0.55rem;
        box-shadow: 0 2px 8px rgba(43, 33, 24, 0.03);
    }}
    .pred-card.top {{
        border: 1.5px solid {EMERALD};
        background: linear-gradient(90deg, #EAF3EE, {WHITE} 40%);
    }}
    .pred-rank {{
        font-family: 'Space Mono', monospace;
        color: {TEXT_MUTED};
        font-size: 0.78rem;
        width: 22px;
    }}
    .pred-name {{
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.98rem;
        color: {TEXT_INK};
        flex-grow: 1;
        margin-left: 0.4rem;
    }}
    .pred-badge {{
        font-family: 'Space Mono', monospace;
        font-weight: 700;
        font-size: 0.82rem;
        padding: 0.25rem 0.65rem;
        border-radius: 999px;
        color: {WHITE};
    }}

    /* ---------- Healthy choice indicator ---------- */
    .health-badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        font-family: 'Space Mono', monospace;
        font-size: 0.8rem;
        font-weight: 700;
        padding: 0.35rem 0.8rem;
        border-radius: 999px;
        margin-top: 0.9rem;
    }}

    section[data-testid="stSidebar"] {{
        background: {WHITE};
        border-right: 1px solid {BORDER};
    }}
    section[data-testid="stSidebar"] * {{
        color: {TEXT_INK} !important;
    }}
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: {EMERALD} !important;
        font-family: 'Fraunces', serif !important;
    }}

    .footer-note {{
        text-align: center;
        color: {TEXT_MUTED};
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        margin-top: 2rem;
        letter-spacing: 0.05em;
    }}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# LOAD MODEL (cached)
# ----------------------------------------------------------------------------
@st.cache_resource
def load_food_model():
    model = load_model("food_classifier_model.h5")
    with open("class_labels.json") as f:
        idx_to_class = {int(k): v for k, v in json.load(f).items()}
    return model, idx_to_class


def predict(img: Image.Image, model, idx_to_class, top_k=3):
    img_resized = img.resize((224, 224)).convert("RGB")
    arr = keras_image.img_to_array(img_resized) / 255.0
    arr = np.expand_dims(arr, axis=0)
    preds = model.predict(arr, verbose=0)[0]
    top_indices = preds.argsort()[-top_k:][::-1]
    results = [(idx_to_class[i], float(preds[i])) for i in top_indices]
    return results


def macro_donut(protein, carbs, fat, calories):
    labels = ["Protein", "Carbs", "Fat"]
    values = [protein, carbs, fat]
    colors = [EMERALD, BRASS, WINE]
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.65,
        marker=dict(colors=colors, line=dict(color=WHITE, width=2)),
        textinfo="label+percent",
        textposition="outside",
        textfont=dict(family="Inter", size=12, color=TEXT_INK),
    ))
    fig.update_layout(
        height=320,
        margin=dict(l=60, r=60, t=40, b=40),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        annotations=[dict(
            text=f"<b>{calories}</b><br>kcal",
            x=0.5, y=0.5,
            font=dict(family="Space Mono", size=20, color=TEXT_INK),
            showarrow=False
        )]
    )
    return fig


def render_prediction_cards(results):
    badge_colors = [EMERALD, BRASS, WINE]
    html = ""
    for i, (name, conf) in enumerate(results):
        top_class = "top" if i == 0 else ""
        display_name = name.replace('_', ' ').title()
        html += f"""
        <div class="pred-card {top_class}">
            <span class="pred-rank">#{i+1}</span>
            <span class="pred-name">{display_name}</span>
            <span class="pred-badge" style="background:{badge_colors[i]};">{conf*100:.1f}%</span>
        </div>
        """
    st.markdown(html, unsafe_allow_html=True)


def healthy_indicator(calories):
    if calories < 300:
        color, bg, label, emoji = EMERALD, "#DDEDE3", "Healthy", "🟢"
    elif calories < 500:
        color, bg, label, emoji = BRASS, "#F5E9CC", "Moderate", "🟡"
    else:
        color, bg, label, emoji = WINE, "#F3DAD6", "High calorie", "🔴"
    st.markdown(
        f'<div class="health-badge" style="color:{color}; background:{bg};">'
        f'{emoji} {label}</div>',
        unsafe_allow_html=True
    )


# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## FoodLens")
    st.markdown("A computer vision mini-project: food image classification with nutrition estimation.")
    st.markdown("---")
    st.markdown("### How it works")
    st.markdown("""
    1. Upload a food photo
    2. MobileNetV2 (transfer learning) classifies it
    3. Top-3 predictions shown with confidence
    4. Nutrition estimated for a standard serving
    """)
    st.markdown("---")
    st.markdown("### Model")
    st.markdown("""
    - Architecture: MobileNetV2 (transfer learning)
    - Classes: 15 food categories
    - Framework: TensorFlow / Keras
    """)
    st.markdown("---")
    st.markdown("### Note on nutrition")
    st.markdown(
        "Values are estimates for a standard serving size, not measured "
        "from the image — a 2D photo has no depth or scale reference."
    )

# ----------------------------------------------------------------------------
# HERO
# ----------------------------------------------------------------------------
st.markdown('<p class="eyebrow">Computer vision mini-project</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-title">FoodLens</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">Upload a food photo. Get an instant classification, '
    'a confidence reading, and a nutrition estimate for a standard serving.</p>',
    unsafe_allow_html=True
)
st.markdown('<hr class="hero-rule">', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# MODEL LOAD
# ----------------------------------------------------------------------------
try:
    model, idx_to_class = load_food_model()
    model_loaded = True
except Exception:
    model_loaded = False
    st.error(
        "Model files not found. Place `food_classifier_model.h5` and "
        "`class_labels.json` (from the training notebook) in this app's folder."
    )

# ----------------------------------------------------------------------------
# SESSION STATE for serving multiplier
# ----------------------------------------------------------------------------
if "serving_mult" not in st.session_state:
    st.session_state.serving_mult = 1.0

# ----------------------------------------------------------------------------
# MAIN LAYOUT
# ----------------------------------------------------------------------------
col_upload, col_result = st.columns([1, 1.3], gap="large")

with col_upload:
    st.markdown('<p class="section-label">01 — Upload</p>', unsafe_allow_html=True)
    st.markdown('<div class="upload-icon-badge">🍽️</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Choose a food photo",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        img = Image.open(uploaded_file)
        img_b64 = image_to_base64(img)
        st.markdown(
            f'<div class="preview-img-wrap" style="text-align:center;">'
            f'<img src="data:image/jpeg;base64,{img_b64}" '
            f'style="max-height:440px; width:auto; max-width:100%; object-fit:cover; '
            f'border-radius:10px; box-shadow:0 6px 20px rgba(43,33,24,0.14); border:1px solid {BORDER};" />'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<p style="color:{TEXT_MUTED}; font-size:0.9rem; margin-top:1rem;">'
            f'Drop a JPG or PNG of a food item to begin.</p>',
            unsafe_allow_html=True
        )

with col_result:
    st.markdown('<p class="section-label">02 — Result</p>', unsafe_allow_html=True)

    if uploaded_file and model_loaded:
        with st.spinner("Analyzing image..."):
            time.sleep(0.4)
            results = predict(img, model, idx_to_class, top_k=3)

        top_class, top_conf = results[0]

        st.markdown(f"""
        <div class="plate-card">
            <p class="predicted-food">{top_class.replace('_', ' ').title()}</p>
            <p class="confidence-line">Confidence <span class="confidence-value">{top_conf*100:.1f}%</span></p>
        </div>
        """, unsafe_allow_html=True)

        render_prediction_cards(results)

        # ------------------------------------------------------------------
        # NUTRITION SECTION
        # ------------------------------------------------------------------
        st.markdown('<p class="section-label" style="margin-top:1.5rem;">03 — Nutrition estimate</p>', unsafe_allow_html=True)

        btn_cols = st.columns(5)
        serving_options = [0.5, 1.0, 1.5, 2.0, 3.0]
        for i, opt in enumerate(serving_options):
            with btn_cols[i]:
                label = f"{opt}x" if opt != 1.0 else "1x"
                if st.button(label, key=f"serve_{opt}", use_container_width=True):
                    st.session_state.serving_mult = opt

        serving_mult = st.session_state.serving_mult
        nutri = get_nutrition(top_class, serving_mult)

        if nutri:
            st.markdown(
                f'<p style="color:{TEXT_MUTED}; font-size:0.85rem; margin: 0.8rem 0 1rem 0;">'
                f'Showing <b style="color:{BRASS};">{serving_mult}x</b> a standard serving '
                f'<i>({nutri["serving_size"]})</i></p>',
                unsafe_allow_html=True
            )

            m1, m2, m3, m4 = st.columns(4)
            for col, icon, label, value, unit in zip(
                [m1, m2, m3, m4],
                ["🔥", "🥩", "🍚", "🥑"],
                ["Calories", "Protein", "Carbs", "Fat"],
                [nutri["calories"], nutri["protein_g"], nutri["carbs_g"], nutri["fat_g"]],
                ["", "g", "g", "g"]
            ):
                with col:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div style="font-size:1.3rem;">{icon}</div>
                        <div class="stat-value">{value}{unit}</div>
                        <div class="stat-label">{label}</div>
                    </div>
                    """, unsafe_allow_html=True)

            healthy_indicator(nutri["calories"])

            st.plotly_chart(
                macro_donut(nutri["protein_g"], nutri["carbs_g"], nutri["fat_g"], nutri["calories"]),
                use_container_width=True,
                config={"displayModeBar": False}
            )

            st.markdown(
                '<p class="serving-note">Estimates are based on standard serving sizes, '
                'not measured directly from the image. Actual values vary by recipe and portion.</p>',
                unsafe_allow_html=True
            )
        else:
            st.warning("Nutrition data not available for this class.")

    elif not model_loaded:
        st.info("Model not loaded — see the message above.")
    else:
        st.markdown(
            f'<p style="color:{TEXT_MUTED}; font-size:0.9rem; margin-top:1rem;">'
            'Your result will appear here once you upload an image.</p>',
            unsafe_allow_html=True
        )

# ----------------------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------------------
st.markdown(
    '<p class="footer-note">TENSORFLOW · STREAMLIT · MOBILENETV2 — COMPUTER VISION MINI PROJECT</p>',
    unsafe_allow_html=True
)
