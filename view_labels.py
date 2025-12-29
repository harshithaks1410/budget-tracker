import pickle

with open("labels.pkl", "rb") as f:
    labels = pickle.load(f)

print(labels)
