import os
import cv2
import numpy as np
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

DATASET_PATH = "../dataset/images"

IMG_SIZE = 64

data = []
labels = []

# -----------------------------
# LOAD DATASET
# -----------------------------

classes = ["normal", "abnormal"]

for label, folder in enumerate(classes):

    path = os.path.join(DATASET_PATH, folder)

    for img_name in os.listdir(path):

        img_path = os.path.join(path, img_name)

        img = cv2.imread(img_path)

        if img is None:
            continue

        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

        img = img / 255.0

        img = img.flatten()

        data.append(img)

        labels.append(label)

data = np.array(data)
labels = np.array(labels)

print("Dataset Loaded:", data.shape)

# -----------------------------
# TRAIN TEST SPLIT
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    data,
    labels,
    test_size=0.2,
    random_state=42
)

# -----------------------------
# XGBOOST MODEL
# -----------------------------

model = xgb.XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8
)

model.fit(X_train, y_train)

# -----------------------------
# TEST MODEL
# -----------------------------

pred = model.predict(X_test)

acc = accuracy_score(y_test, pred)

print("Accuracy :", acc)

# -----------------------------
# SAVE MODEL
# -----------------------------

joblib.dump(model, "image_xgboost.pkl")

print("Model saved : image_xgboost.pkl")