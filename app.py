# app.py
import streamlit as st
import numpy as np
import mediapipe as mp
from scipy.spatial import distance
from PIL import Image

st.set_page_config(page_title="Drowsiness Detection App", page_icon="😴", layout="centered")

st.title("😴 Real-Time Drowsiness Detection")
st.markdown(
    """
Upload an image or take a picture with your webcam.
The app will detect your eyes and check if you are drowsy.
"""
)

# MediaPipe face mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# EAR (Eye Aspect Ratio) function
def compute_EAR(eye_landmarks):
    # eye_landmarks: list of 6 points (x, y)
    A = distance.euclidean(eye_landmarks[1], eye_landmarks[5])
    B = distance.euclidean(eye_landmarks[2], eye_landmarks[4])
    C = distance.euclidean(eye_landmarks[0], eye_landmarks[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Streamlit camera input
img_file = st.camera_input("Take a picture")

if img_file is not None:
    image = Image.open(img_file)
    st.image(image, caption="Captured Image", use_column_width=True)

    # Convert PIL image to numpy array
    image_np = np.array(image)

    # Convert RGB to BGR (MediaPipe uses RGB)
    image_rgb = image_np[:, :, ::-1]

    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    ) as face_mesh:

        results = face_mesh.process(image_rgb)

        if not results.multi_face_landmarks:
            st.warning("😐 No face detected. Please try again.")
        else:
            face_landmarks = results.multi_face_landmarks[0]

            # Eye landmark indices from MediaPipe
            left_eye_indices = [33, 160, 158, 133, 153, 144]  # Left eye
            right_eye_indices = [263, 387, 385, 362, 380, 373]  # Right eye

            left_eye = []
            right_eye = []

            h, w, _ = image_np.shape

            for idx in left_eye_indices:
                lm = face_landmarks.landmark[idx]
                left_eye.append((int(lm.x * w), int(lm.y * h)))

            for idx in right_eye_indices:
                lm = face_landmarks.landmark[idx]
                right_eye.append((int(lm.x * w), int(lm.y * h)))

            # Compute EAR
            left_EAR = compute_EAR(left_eye)
            right_EAR = compute_EAR(right_eye)
            avg_EAR = (left_EAR + right_EAR) / 2.0

            # Threshold for drowsiness
            EAR_THRESHOLD = 0.25

            st.write(f"👁️ Eye Aspect Ratio (EAR): {avg_EAR:.2f}")

            if avg_EAR < EAR_THRESHOLD:
                st.error("⚠️ Drowsiness Detected! Please take a break.")
            else:
                st.success("😊 Eyes are open. You are alert!")

            # Draw eye landmarks
            annotated_image = image_np.copy()
            for eye in [left_eye, right_eye]:
                for (x, y) in eye:
                    annotated_image = cv2.circle(annotated_image, (x, y), 2, (0, 255, 0), -1)
            
            st.image(annotated_image[:, :, ::-1], caption="Eyes Detected", use_column_width=True)
