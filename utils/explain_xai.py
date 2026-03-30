import requests
import json

API_KEY = "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"

def explain_prediction(data):

    values = data.tolist()[0]

    prompt = f"""
Patient Heart Data:
Age: {values[0]}
Sex: {values[1]}
Chest Pain: {values[2]}
Blood Pressure: {values[3]}
Cholesterol: {values[4]}
Fasting Blood Sugar: {values[5]}
ECG: {values[6]}
Max Heart Rate: {values[7]}
Exercise Angina: {values[8]}
Old Peak: {values[9]}
Slope: {values[10]}
CA: {values[11]}
Thal: {values[12]}

Explain why heart disease risk may be present and give health suggestions.
"""

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    result = response.json()

    explanation = result["choices"][0]["message"]["content"]

    suggestion = [
        "Maintain healthy diet",
        "Exercise regularly",
        "Avoid smoking",
        "Consult cardiologist"
    ]

    return explanation, suggestion