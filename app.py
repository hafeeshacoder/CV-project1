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
    <h1 style='text-align: center;'>🎨 Multi-Color Detection System</h1>
    <h4 style='text-align: center; color: gray;'>
    Detect multiple colors from an uploaded image
    </h4>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ---------- INFO BOX ----------
st.info(
    "📌 Upload an image containing multiple colors. "
    "The system will automatically identify and list the colors present."
)

# ---------------- COLOR DEFINITIONS (RGB) ---------------- #
COLORS = {
    "Red": lambda r, g, b: r > 150 and g < 100 and b < 100,
    "Green": lambda r, g, b: g > 150 and r < 100 and b < 100,
    "Blue": lambda r, g, b: b > 150 and r < 100 and g < 100,
    "Yellow": lambda r, g, b: r > 150 and g > 150 and b < 100,
    "Black": lambda r, g, b: r < 50 and g < 50 and b < 50,
    "White": lambda r, g, b: r > 200 and g > 200 and b > 200,
    "Orange": lambda r, g, b: r > 200 and g > 100 and b < 80,
    "Purple": lambda r, g, b: r > 120 and b > 120 and g < 100,
}

# ---------------- COLOR DETECTION FUNCTION ---------------- #
def detect_colors(image_array):
    detected = set()
    pixels = image_array.reshape(-1, 3)

    for r, g, b in pixels[::500]:
        for color, rule in COLORS.items():
            if rule(r, g, b):
                detected.add(color)

    return list(detected)

# ---------- LAYOUT ----------
left, right = st.columns([1, 1])

# ---------------- IMAGE UPLOAD ---------------- #
with left:
    st.subheader("📁 Upload Image")
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=["jpg", "jpeg", "png"]
    )

# ---------------- OUTPUT ---------------- #
with right:
    st.subheader("📊 Detection Results")

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        image_array = np.array(image)

        colors_found = detect_colors(image_array)

        st.image(
            image,
            caption="🖼 Uploaded Image",
            use_column_width=True
        )

        st.success(f"🎯 Number of Colors Detected: {len(colors_found)}")

        if colors_found:
            st.markdown("### 🎨 Detected Colors")
            for color in colors_found:
                st.write(f"✔ {color}")
        else:
            st.warning("No dominant colors detected.")

# ---------- FOOTER ----------
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    🧠 Mini Project | Computer Vision | Multi-Color Detection  
    </div>
    """,
    unsafe_allow_html=True
)
