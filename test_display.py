import cv2

cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("❌ Camera not accessible.")
    exit()

print("📸 Camera started. Press 'q' to quit.")

while True:
    ret, frame = cam.read()
    if not ret:
        print("❌ Failed to read frame.")
        break

    cv2.imshow("🟢 Live Camera Feed", frame)

    # Wait for 1ms, exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
