# Install required packages
# pip install streamlit opencv-python numpy playsound

import streamlit as st
import cv2
import numpy as np
from scipy.spatial import distance
import tempfile
from playsound import playsound
from threading import Thread

# -------------------------
# Functions
# -------------------------
def play_sound(path):
    Thread(target=playsound, args=(path,), daemon=True).start()

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def detect_eyes(frame, face_cascade, eye_cascade):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    eyes_coords = []

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            eye = frame[y+ey:y+ey+eh, x+ex:x+ex+ew]
            eyes_coords.append((x+ex, y+ey, ew, eh))
            cv2.rectangle(frame, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (0,255,0), 2)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)
    return frame, eyes_coords

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="🛌 Drowsiness Detection", layout="wide")
st.title("🛌 Real-Time Drowsiness Detection")
st.markdown("""
Monitor your alertness while studying or working.  
- **Normal** → Green status  
- **Eyes closing** → Yellow alert  
- **Sleep detected** → Red warning + alert sound  
""")

# Upload optional sounds
alert_file = st.file_uploader("Upload alert sound (eye closing)", type=["mp3"])
break_file = st.file_uploader("Upload break sound (sleep)", type=["mp3"])

# Default sounds if none uploaded
alert_path = "alert.mp3"
break_path = "break.mp3"
if alert_file:
    temp_alert = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_alert.write(alert_file.read())
    alert_path = temp_alert.name
if break_file:
    temp_break = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_break.write(break_file.read())
    break_path = temp_break.name

st.sidebar.header("Instructions")
st.sidebar.write("""
1. Allow webcam access.  
2. Make sure your face is visible to the camera.  
3. Click 'Start Detection' to begin monitoring.  
4. Sit upright for accurate detection.
""")

# -------------------------
# Parameters
# -------------------------
EAR_THRESHOLD = 0.25
CONSEC_FRAMES = 15
frame_counter = 0

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# -------------------------
# Camera Input
# -------------------------
stframe = st.image([])
start_button = st.button("Start Detection")

if start_button:
    st.success("Webcam started. Monitoring drowsiness...")
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("Cannot access webcam!")
            break

        frame, eyes_coords = detect_eyes(frame, face_cascade, eye_cascade)

        # Simple drowsiness logic: eyes missing in frame => closed
        if len(eyes_coords) < 2:  # both eyes not detected
            frame_counter += 1
            if frame_counter == 5:
                play_sound(alert_path)
            if frame_counter >= CONSEC_FRAMES:
                st.warning("SLEEP DETECTED! TAKE A BREAK!")
                play_sound(break_path)
                cv2.putText(frame, "SLEEP DETECTED!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255), 2)
        else:
            frame_counter = 0
            cv2.putText(frame, "ALERT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB")

    cap.release()
