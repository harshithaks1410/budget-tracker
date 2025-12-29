import cv2
import os
import numpy as np
import pickle

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}
x_train = []
y_labels = []

faces_dir = "faces"

for root, dirs, files in os.walk(faces_dir):
    for file in files:
        if file.endswith("jpg") or file.endswith("png"):
            path = os.path.join(root, file)
            label = os.path.basename(root)

            if label not in label_ids:
                label_ids[label] = current_id
                current_id += 1

            id_ = label_ids[label]

            image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            faces = face_cascade.detectMultiScale(image, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                roi = image[y:y + h, x:x + w]
                x_train.append(roi)
                y_labels.append(id_)

# Save the labels
with open("labels.pkl", "wb") as f:
    pickle.dump(label_ids, f)

# Train the model
recognizer.train(x_train, np.array(y_labels))
recognizer.save("face_model.yml")

print("✅ Model trained and saved as face_model.yml and labels.pkl")
