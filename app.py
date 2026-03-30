from flask import Flask, render_template, request, send_file, redirect, session
import numpy as np
import joblib
import os
import cv2
import sqlite3

# Custom module imports
from utils.explain_xai import explain_prediction
from utils.graph import generate_graph
from utils.report import generate_report

app = Flask(__name__)
app.secret_key = "heart_ai_secret"

# DATABASE CONNECTION
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# CREATE USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT
)
""")

# CREATE SEARCH LOG TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS search_logs(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
search_data TEXT
)
""")

conn.commit()

# -----------------------------
# LOAD MODELS
# -----------------------------
# Model files correct-ana path-la irukanum
model = joblib.load("model/heart_xgboost.pkl")
image_model = joblib.load("model/image_xgboost.pkl")

# Folders create pannuvatharku
os.makedirs("static/uploads", exist_ok=True)
os.makedirs("static/graphs", exist_ok=True)
os.makedirs("static/reports", exist_ok=True)

# -----------------------------
# ROUTES
# -----------------------------

@app.route("/")
def index():

    if "user" not in session:
        return redirect("/login")

    return render_template("index.html")

@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/login")

    return render_template("dashboard.html")

# HEART DISEASE PREDICTION
@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    if request.method == "POST":
        # Form values-ai float-aga mathuvatharku
        age = float(request.form["age"])
        sex = float(request.form["sex"])
        cp = float(request.form["cp"])
        trestbps = float(request.form["trestbps"])
        chol = float(request.form["chol"])
        fbs = float(request.form["fbs"])
        restecg = float(request.form["restecg"])
        thalach = float(request.form["thalach"])
        exang = float(request.form["exang"])
        oldpeak = float(request.form["oldpeak"])
        slope = float(request.form["slope"])

        ca = request.form.get("ca")
        ca = float(ca) if ca else 0.0
        thal = float(request.form["thal"])

        data = np.array([[
            age, sex, cp, trestbps, chol, fbs, 
            restecg, thalach, exang, oldpeak, 
            slope, ca, thal
        ]])

        pred = model.predict(data)[0]
        prob = model.predict_proba(data)[0][1]

        result = "Abnormal" if pred == 0 else "Normal"

        # XAI matrum Report generation
        explanation, suggestion = explain_prediction(data)
        graph = generate_graph(data[0])
        report = generate_report(result, explanation)

        return render_template(
            "result.html",
            result=result,
            probability=round(prob * 100, 2),
            explanation=explanation,
            suggestion=suggestion,
            graph=graph,
            report=report
        )

    return render_template("prediction.html")

# IMAGE CLASSIFICATION
@app.route("/classification", methods=["GET", "POST"])
def classify_image():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            filepath = os.path.join("static/uploads", file.filename)
            file.save(filepath)

            # Image processing
            img = cv2.imread(filepath)
            img = cv2.resize(img, (64, 64))
            img = img / 255.0
            img = img.flatten().reshape(1, -1)

            pred = image_model.predict(img)[0]
            prob = model.predict_proba(data)[0]
            
            normal_prob = prob[1] * 100
            abnormal_prob = prob[0] * 100

            if pred == 1:
                result = f"Normal : {round(normal_prob,2)} %"
            else:
                result = f"Abnormal : {round(abnormal_prob,2)} %"
            graph = generate_graph(img[0][:6]) # Sample data for graph
            report = generate_report(result, ["Image Classification Result"])

            return render_template(
                "result.html",
                result=result,
                probability=round(prob * 100, 2),
                explanation=["AI based image classification"],
                suggestion=["Consult doctor if abnormal pattern detected"],
                graph=graph,
                report=report
            )

    return render_template("classification.html")

# REPORT DOWNLOAD - Corrected path syntax
@app.route("/download/<path:filename>")
def download(filename):
    return send_file(filename, as_attachment=True)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # ADMIN LOGIN
        if username == "admin" and password == "admin123":
            session["admin"] = username
            return redirect("/admin_dashboard")

        # USER LOGIN
        user = cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username,password)
        ).fetchone()

        if user:
            session["user"] = username
            return redirect("/")

    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        cursor.execute(
        "INSERT INTO users(username,password) VALUES(?,?)",
        (username,password))

        conn.commit()

        return redirect("/login")

    return render_template("register.html")

@app.route("/admin_dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect("/login")

    total_users = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    total_search = cursor.execute("SELECT COUNT(*) FROM search_logs").fetchone()[0]

    return render_template("admin_dashboard.html",
                           total_users=total_users,
                           total_search=total_search)

# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)