import streamlit as st
import cv2
import numpy as np
from PIL import Image
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

st.set_page_config(page_title="Multi Color Detection", layout="wide")

st.title("🎨 Multi-Color Detection using OpenCV")
st.write("Detect colors from **Image Upload** or **Live Camera**")

# ---------------- COLOR RANGES (HSV) ---------------- #
COLOR_RANGES = {
    "Red": [(0, 120, 70), (10, 255, 255)],
    "Green": [(40, 70, 70), (80, 255, 255)],
    "Blue": [(100, 150, 50), (140, 255, 255)],
    "Yellow": [(20, 100, 100), (30, 255, 255)],
    "Orange": [(10, 100, 20), (20, 255, 255)],
    "Purple": [(125, 50, 50), (150, 255, 255)],
    "White": [(0, 0, 200), (180, 50, 255)],
    "Black": [(0, 0, 0), (180, 255, 30)]
}

# ---------------- IMAGE COLOR DETECTION FUNCTION ---------------- #
def detect_colors(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    detected_colors = []

    for color, (lower, upper) in COLOR_RANGES.items():
        lower = np.array(lower)
        upper = np.array(upper)
        mask = cv2.inRange(hsv, lower, upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 800:
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(image, (x, y), (x+w, y+h), (0,255,0), 2)
                    cv2.putText(image, color, (x, y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
                    detected_colors.append(color)
                    break

    return image, list(set(detected_colors))

# ---------------- OPTION SELECTION ---------------- #
option = st.sidebar.radio(
    "Choose Detection Mode",
    ("📁 Upload Image", "🎥 Live Camera")
)

# ---------------- IMAGE UPLOAD OPTION ---------------- #
if option == "📁 Upload Image":
    st.subheader("📁 Upload Image for Color Detection")

    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        image_np = np.array(image)
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        output_image, colors = detect_colors(image_bgr)

        st.image(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB),
                 caption="Detected Colors", use_column_width=True)

        st.success(f"🎯 Number of Colors Detected: {len(colors)}")
        st.write("🖌 Detected Colors:", colors)

# ---------------- LIVE CAMERA OPTION ---------------- #
class VideoProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        processed_img, colors = detect_colors(img)
        return processed_img

if option == "🎥 Live Camera":
    st.subheader("🎥 Live Camera Color Detection")
    st.info("Allow camera access when prompted")

    webrtc_streamer(
        key="color-detection",
        video_processor_factory=VideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
    )

    st.write("🟢 Detects multiple colors in real time")

---

## ▶ How to Run the Project

```bash
streamlit run app.py
