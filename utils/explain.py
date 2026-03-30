import shap
import joblib

model = joblib.load("model/heart_xgboost.pkl")

explainer = shap.TreeExplainer(model)

feature_names = [
    "Age",
    "Sex",
    "Chest Pain",
    "Blood Pressure",
    "Cholesterol",
    "Heart Rate",
    "Oldpeak"
]


def explain_prediction(data):

    shap_values = explainer.shap_values(data)

    explanations = []

    for i, val in enumerate(shap_values[0]):

        if val > 0:
            explanations.append(f"{feature_names[i]} increases risk")

    return explanations