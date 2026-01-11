# app.py
import streamlit as st
import numpy as np
import cv2
from scipy.spatial import distance
import tempfile

st.set_page_config(
    page_title="🛌 Drowsiness Detection",
    page_icon="😴",
    layout="wide"
)

st.title("😴 Real-Time Drowsiness Detection (Browser-friendly)")

st.markdown("""
This app detects **drowsiness in real-time** using your webcam.  

- **Normal:** Continue  
- **Eyes Closing:** Alert sound  
- **Sleep Detected:** Take a forced break  
""")

# -----------------------
# EAR calculation
# -----------------------
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

# -----------------------
# Upload sounds
# -----------------------
alert_file = st.file_uploader("Upload alert sound (eye closing)", type=["mp3"])
break_file = st.file_uploader("Upload break sound (sleep detected)", type=["mp3"])

alert_path = break_path = None
if alert_file and break_file:
    alert_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    break_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    with open(alert_path, "wb") as f:
        f.write(alert_file.read())
    with open(break_path, "wb") as f:
        f.write(break_file.read())
    st.success("Sounds uploaded successfully! You can start detection.")

# -----------------------
# Start webcam detection
# -----------------------
if st.button("Start Detection"):

    if not alert_path or not break_path:
        st.warning("Please upload both alert and break sounds first!")
    else:
        # Load OpenCV Haar cascades (built-in)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

        EAR_THRESHOLD = 0.25
        CONSEC_FRAMES = 15
        frame_counter = 0

        stframe = st.empty()  # Placeholder for webcam frames

        st.info("Click 'Take Photo' repeatedly to simulate real-time detection in the browser!")

        while True:
            img_file_buffer = st.camera_input("Take a selfie")
            if img_file_buffer is None:
                break

            # Convert uploaded image to OpenCV format
            file_bytes = np.asarray(bytearray(img_file_buffer.read()), dtype=np.uint8)
            frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            status_text = "😃 Normal"

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray)
                
                ear_list = []
                for (ex, ey, ew, eh) in eyes:
                    eye_roi = roi_gray[ey:ey+eh, ex:ex+ew]
                    # Approximate EAR using width/height ratio
                    ear = ew / eh
                    ear_list.append(ear)
                    # Draw rectangle around eyes
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0,255,0), 2)

                if ear_list:
                    ear_avg = np.mean(ear_list)
                    if ear_avg < EAR_THRESHOLD:
                        frame_counter += 1
                        if frame_counter >= CONSEC_FRAMES:
                            status_text = "💤 SLEEP DETECTED! TAKE A BREAK!"
                            st.audio(break_path, format="audio/mp3")
                    else:
                        if frame_counter >= 5:
                            st.audio(alert_path, format="audio/mp3")
                            status_text = "😴 Eyes Closing!"
                        frame_counter = 0

            # Display status on frame
            cv2.putText(frame, status_text, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            # Convert to RGB for Streamlit
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            stframe.image(frame_rgb, channels="RGB")
