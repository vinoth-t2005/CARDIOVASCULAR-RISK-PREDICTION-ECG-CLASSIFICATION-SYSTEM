import pandas as pd
import joblib

from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


# -----------------------------
# LOAD DATASET
# -----------------------------

df = pd.read_csv("../dataset/heart.csv")

print("Dataset Shape:", df.shape)
print(df.head())


# -----------------------------
# FEATURES AND TARGET
# -----------------------------

X = df.drop("target", axis=1)

y = df["target"]


# -----------------------------
# TRAIN TEST SPLIT
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# -----------------------------
# CREATE MODEL
# -----------------------------

model = XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=4,
    random_state=42
)


# -----------------------------
# TRAIN MODEL
# -----------------------------

model.fit(X_train, y_train)


# -----------------------------
# PREDICTION
# -----------------------------

y_pred = model.predict(X_test)


# -----------------------------
# EVALUATION
# -----------------------------

accuracy = accuracy_score(y_test, y_pred)

accuracy_percent = int(accuracy * 100)

print("\nModel Accuracy:", accuracy_percent, "%")

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))


# -----------------------------
# SAVE MODEL
# -----------------------------

joblib.dump(model, "heart_xgboost.pkl")

print("\nModel saved successfully as heart_xgboost.pkl")