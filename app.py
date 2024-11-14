# app.py
from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load model, scaler, and encoders
model = joblib.load("model.joblib")
scaler = joblib.load("scaler.joblib")
le_overtime = joblib.load("le_overtime.joblib")
le_attrition = joblib.load("le_attrition.joblib")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    # Convert inputs to match model input format
    age = int(data['age'])
    job_satisfaction = int(data['job_satisfaction'])
    years_at_company = int(data['years_at_company'])
    job_level = int(data['job_level'])
    monthly_income = float(data['monthly_income'])
    total_working_years = int(data['total_working_years'])
    years_since_last_promotion = int(data['years_since_last_promotion'])
    overtime = le_overtime.transform([data['overtime']])[0]

    features = np.array([[age, job_satisfaction, years_at_company, job_level,
                          monthly_income, total_working_years,
                          years_since_last_promotion, overtime]])
    
    # Scale features
    features_scaled = scaler.transform(features)

    # Make prediction
    prediction = model.predict(features_scaled)
    prediction_label = le_attrition.inverse_transform(prediction)[0]
    return jsonify({'prediction': prediction_label})

if __name__ == "__main__":
    app.run(debug=True)
