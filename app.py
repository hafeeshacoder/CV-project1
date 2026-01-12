import streamlit as st
import numpy as np
from PIL import Image

st.set_page_config(page_title="Multi Color Detection", layout="wide")

st.title("🎨 Multi-Color Detection (Image Upload)")
st.write("Detect multiple colors from an uploaded image")

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

    for r, g, b in pixels[::500]:  # sample pixels
        for color, rule in COLORS.items():
            if rule(r, g, b):
                detected.add(color)

    return list(detected)

# ---------------- IMAGE UPLOAD ---------------- #
uploaded_file = st.file_uploader(
    "Upload an Image", type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    image_array = np.array(image)

    colors_found = detect_colors(image_array)

    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.success(f"Number of Colors Detected: {len(colors_found)}")
    st.write("Detected Colors:")
    st.write(colors_found)

