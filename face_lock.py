import cv2
import pickle
import time
import os
import subprocess
import webbrowser

# Load face recognizer and face cascade
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face_model.yml")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Load labels
with open("labels.pkl", "rb") as f:
    labels = pickle.load(f)
    labels = {v: k for k, v in labels.items()}

CONFIDENCE_THRESHOLD = 60  # Accept only if below this
last_warning_time = 0
app_started = False

print("🔁 Starting face recognition...")
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        id_, confidence = recognizer.predict(roi_gray)

        if confidence < CONFIDENCE_THRESHOLD:
            name = labels[id_]
            print(f"✅ Recognized: {name} (Confidence: {confidence:.2f})")
            if not app_started:
                app_started = True
                print("🔓 Access Granted! Opening Budget Tracker...")

                # Start Flask app in a new terminal
                subprocess.Popen(["start", "cmd", "/k", "python app.py"], shell=True)

                # Wait a moment for the server to start, then open browser
                time.sleep(2)
                webbrowser.open("http://127.0.0.1:5000")

            cap.release()
            cv2.destroyAllWindows()
            exit()

        else:
            current_time = time.time()
            if current_time - last_warning_time > 3:
                print("❌ Wrong Face Detected")
                last_warning_time = current_time

    cv2.imshow("Face Lock - Press Q to Quit", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("🔒 Exiting Face Lock...")
        break

cap.release()
cv2.destroyAllWindows()
