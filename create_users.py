import cv2
import os

def capture_faces(name):
    print(f"\n📸 Starting camera for {name}...")
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("❌ ERROR: Camera not accessible.")
        return

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    count = 0
    save_path = f"faces/{name}"
    os.makedirs(save_path, exist_ok=True)

    while True:
        ret, frame = cam.read()
        if not ret:
            print("❌ ERROR: Couldn't read from camera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi = frame[y:y+h, x:x+w]
            img_path = os.path.join(save_path, f"{count}.jpg")
            cv2.imwrite(img_path, roi)
            count += 1
            print(f"✅ Saved image {count} for {name}")
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Show the live video
        cv2.imshow("Capturing Face - Press Q to stop", frame)

        # Break after 5 images or on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 5:
            break

    cam.release()
    cv2.destroyAllWindows()
    print(f"✅ Done capturing for {name}.")

# Main loop for all members
members = ["member1", "member2", "member3", "member4","member5"]
for person in members:
    input(f"\n🔔 Press Enter to start capturing for {person}")
    capture_faces(person)
