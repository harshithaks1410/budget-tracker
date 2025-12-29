import os
import cv2
import numpy as np
import pickle

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

face_data = []
face_labels = []
label_ids = {}
current_id = 0

for root, dirs, files in os.walk("faces"):
    for dir_name in dirs:
        path = os.path.join(root, dir_name)
        for img_name in os.listdir(path):
            if img_name.endswith(".jpg") or img_name.endswith(".png"):
                img_path = os.path.join(path, img_name)
                image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if image is None:
                    continue

                face_data.append(image)

                if dir_name not in label_ids:
                    label_ids[dir_name] = current_id
                    current_id += 1
                face_labels.append(label_ids[dir_name])

model = cv2.face.LBPHFaceRecognizer_create()
model.train(face_data, np.array(face_labels))
model.save("face_model.yml")

with open("labels.pkl", "wb") as f:
    print("📦 Labels being saved:", label_ids)  # <-- ADD THIS LINE
    pickle.dump(label_ids, f)
