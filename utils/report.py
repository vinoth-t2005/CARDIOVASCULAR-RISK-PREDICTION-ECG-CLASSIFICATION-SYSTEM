from fpdf import FPDF
import uuid
import os
from datetime import datetime


def generate_report(result, explanation, suggestion):

    folder = "static/reports"
    os.makedirs(folder, exist_ok=True)

    filename = str(uuid.uuid4()) + ".pdf"

    filepath = os.path.join(folder, filename)

    pdf = FPDF()
    pdf.add_page()

    # TITLE
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0,10,"Heart Disease Prediction Report", ln=True, align="C")

    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(0,10,f"Generated Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)

    pdf.ln(5)

    # RESULT
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"Prediction Result", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.cell(0,10,f"Result: {result}", ln=True)

    pdf.ln(5)

    # AI EXPLANATION
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"Explainable AI Analysis", ln=True)

    pdf.set_font("Arial", size=12)

    if isinstance(explanation, list):

        for e in explanation:
            pdf.multi_cell(0,8,f"- {e}")

    else:

        pdf.multi_cell(0,8,explanation)

    pdf.ln(8)

    # AI SUGGESTION (API suggestion)
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"AI Medical Suggestions", ln=True)

    pdf.set_font("Arial", size=12)

    if isinstance(suggestion, list):

        for s in suggestion:
            pdf.multi_cell(0,8,f"- {s}")

    else:

        pdf.multi_cell(0,8,suggestion)

    pdf.ln(10)

    # GENERAL DOCTOR RECOMMENDATION
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"General Doctor Recommendation", ln=True)

    pdf.set_font("Arial", size=12)

    if result == "Abnormal":

        pdf.multi_cell(
            0,8,
            "The AI model indicates potential signs of heart disease. "
            "It is strongly recommended to consult a cardiologist for further diagnosis. "
            "Maintain a healthy diet, regular exercise, reduce cholesterol foods, "
            "and monitor blood pressure periodically."
        )

    else:

        pdf.multi_cell(
            0,8,
            "The AI model indicates no major risk of heart disease based on the provided data. "
            "Continue maintaining a healthy lifestyle including balanced diet, exercise, "
            "and regular medical checkups."
        )

    pdf.ln(10)

    # DISCLAIMER
    pdf.set_font("Arial","I",10)

    pdf.multi_cell(
        0,6,
        "Note: This report is generated using an AI-based medical prediction system. "
        "The results are for informational purposes only and should not replace "
        "professional medical diagnosis."
    )

    pdf.output(filepath)

    return filepath