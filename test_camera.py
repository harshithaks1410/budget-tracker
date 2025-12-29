import cv2

# Try camera index 1 instead of 0
cam = cv2.VideoCapture(-1)  # or try 2, 3 if needed
if not cam.isOpened():
    print("❌ Camera not accessible at index 1")
else:
    print("✅ Camera is working! Press Q to quit.")
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        cv2.imshow("Camera Test", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
