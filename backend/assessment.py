from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

from database.database_functions import save_prediction


app = Flask(__name__)
model_path = os.path.join("boosting_models/models", "xgboost_model.pkl")
model = joblib.load(model_path)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    try:
        age = float(data["age"])
        bmi = float(data["bmi"])
        gender = int(data["gender"])
        smoking_history = int(data["smoking_history"])
        hypertension = int(data["hypertension"])
        heart_disease = int(data["heart_disease"])
        blood_glucose_level = float(data["blood_glucose_level"])
        HbA1c_level = float(data["HbA1c_level"])
        name = data["name"]
        dob = data["dob"]

        input_data = np.array([[gender, age, hypertension, heart_disease, smoking_history,
                                bmi, HbA1c_level, blood_glucose_level]])
        prediction = model.predict(input_data)[0]

        # Gọi hàm lưu dữ liệu vào database
        save_prediction(data, int(prediction))

        return jsonify({"diabetes_prediction": int(prediction)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)