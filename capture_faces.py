import cv2
import os

# Ask for the member name
member_name = input("Enter the member name (e.g., member1): ").strip()
folder_path = os.path.join("faces", member_name)

# Create folder if not exists
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Start webcam
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

count = 0
print("📸 Capturing face images. Look at the camera...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame from camera.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_img = gray[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (200, 200))
        img_path = os.path.join(folder_path, f"{count}.jpg")
        cv2.imwrite(img_path, face_img)
        count += 1
        print(f"Saved {img_path}")
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Capturing Faces", frame)

    if cv2.waitKey(1) & 0xFF == ord('q') or count >= 20:
        break

cap.release()
cv2.destroyAllWindows()
print("✅ Face capture complete.")
