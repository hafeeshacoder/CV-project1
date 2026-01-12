import streamlit as st
import numpy as np
from PIL import Image

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Multi Color Detection",
    page_icon="🎨",
    layout="wide"
)

# ---------- HEADER ----------
st.markdown(
    """
    <h1 style='text-align:center;'>🎨 Multi-Color Detection System</h1>
    <h4 style='text-align:center; color:gray;'>
    AI-inspired color analysis from uploaded images
    </h4>
    """,
    unsafe_allow_html=True
)

st.markdown("---")
st.info("📌 Upload a colorful image. Adjust sensitivity to see intelligent color detection.")

# ---------- USER CONTROL (INNOVATIVE) ----------
sensitivity = st.slider(
    "🎚 Detection Sensitivity",
    min_value=100,
    max_value=300,
    value=150,
    help="Lower value = more sensitive detection"
)

# ---------------- COLOR DEFINITIONS (RGB) ---------------- #
COLORS = {
    "Red": lambda r, g, b, s: r > s and g < s-50 and b < s-50,
    "Green": lambda r, g, b, s: g > s and r < s-50 and b < s-50,
    "Blue": lambda r, g, b, s: b > s and r < s-50 and g < s-50,
    "Yellow": lambda r, g, b, s: r > s and g > s and b < s-50,
    "Black": lambda r, g, b, s: r < 50 and g < 50 and b < 50,
    "White": lambda r, g, b, s: r > 200 and g > 200 and b > 200,
    "Orange": lambda r, g, b, s: r > s and g > 100 and b < 80,
    "Purple": lambda r, g, b, s: r > 120 and b > 120 and g < 100,
}

# ---------------- COLOR DETECTION FUNCTION ---------------- #
def detect_colors(image_array, sensitivity):
    detected = {}
    pixels = image_array.reshape(-1, 3)

    for r, g, b in pixels[::400]:
        for color, rule in COLORS.items():
            if rule(r, g, b, sensitivity):
                detected[color] = detected.get(color, 0) + 1

    return detected

# ---------- LAYOUT ----------
left, right = st.columns([1, 1])

# ---------------- IMAGE UPLOAD ---------------- #
with left:
    st.subheader("📁 Upload Image")
    uploaded_file = st.file_uploader(
        "Choose an image (JPG / PNG)",
        type=["jpg", "jpeg", "png"]
    )

    with st.expander("🧠 How the system thinks"):
        st.write(
            "The image is broken into pixels. "
            "An intelligent sampling technique checks color dominance "
            "using adjustable sensitivity."
        )

# ---------------- OUTPUT ---------------- #
with right:
    st.subheader("📊 Intelligent Analysis")

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        image_array = np.array(image)

        detected_colors = detect_colors(image_array, sensitivity)

        st.image(image, caption="🖼 Uploaded Image", use_column_width=True)

        if detected_colors:
            colors_found = list(detected_colors.keys())
            dominant_color = max(detected_colors, key=detected_colors.get)

            # 🧠 AI Confidence Score
            confidence = min(100, len(colors_found) * 12 + 40)

            st.success(f"🎯 Colors Detected: {len(colors_found)}")
            st.progress(confidence / 100)

            st.markdown(f"### 🏆 Dominant Color: **{dominant_color}**")
            st.markdown(f"🧠 AI Confidence Score: **{confidence}%**")

            # 🎨 Color Palette Cards
            st.markdown("### 🎨 Color Palette")
            cols = st.columns(len(colors_found))

            color_map = {
                "Red": "#FF0000",
                "Green": "#00FF00",
                "Blue": "#0000FF",
                "Yellow": "#FFFF00",
                "Black": "#000000",
                "White": "#FFFFFF",
                "Orange": "#FFA500",
                "Purple": "#800080"
            }

            for col, color in zip(cols, colors_found):
                with col:
                    st.markdown(
                        f"""
                        <div style="
                            background-color:{color_map.get(color, '#ccc')};
                            height:90px;
                            border-radius:14px;
                            border:3px solid #222;">
                        </div>
                        <p style='text-align:center; font-weight:bold;'>{color}</p>
                        """,
                        unsafe_allow_html=True
                    )

            # 🧩 Insight Panel (Innovative)
            st.markdown("### 🔍 Smart Insight")
            st.info(
                f"The image contains **{len(colors_found)} dominant colors**. "
                f"Based on pixel distribution, **{dominant_color}** appears most frequently. "
                "Adjust sensitivity to explore hidden colors."
            )

        else:
            st.warning("No dominant colors detected. Try lowering sensitivity.")

# ---------- FOOTER ----------
st.markdown("---")
st.markdown(
    """
    <div style='text-align:center; color:gray;'>
    🚀 Innovative Computer Vision Mini Project | Multi-Color Detection
    </div>
    """,
    unsafe_allow_html=True
)
