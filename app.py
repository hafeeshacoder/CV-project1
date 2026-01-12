import streamlit as st
import numpy as np
from PIL import Image

st.set_page_config(page_title="Multi Color Detection", layout="wide")

st.title("🎨 Multi-Color Detection (Image Upload Only)")
st.warning("Live camera disabled for cloud stability")

# Import cv2 ONLY after Streamlit loads
import cv2

COLOR_RANGES = {
    "Red": [(0, 120, 70), (10, 255, 255)],
    "Green": [(40, 70, 70), (80, 255, 255)],
    "Blue": [(100, 150, 50), (140, 255, 255)],
    "Yellow": [(20, 100, 100), (30, 255, 255)],
    "Black": [(0, 0, 0), (180, 255, 30)],
    "White": [(0, 0, 200), (180, 50, 255)],
}

def detect_colors(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    found = []

    for name, (low, high) in COLOR_RANGES.items():
        mask = cv2.inRange(hsv, np.array(low), np.array(high))
        if cv2.countNonZero(mask) > 1500:
            found.append(name)

    return list(set(found))

uploaded = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    img_np = np.array(img)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    colors = detect_colors(img_bgr)

    st.image(img, caption="Uploaded Image", use_column_width=True)
    st.success(f"Detected {len(colors)} colors")
    st.write(colors)
