from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# === Load mô hình đã huấn luyện ===
model = joblib.load("xgb_diabetes_model.pkl")

# === Định nghĩa endpoint nhận dữ liệu và trả kết quả ===
@app.route("/predict", methods=["POST"])
def predict():
    # B1: Lấy dữ liệu JSON từ request
    data = request.get_json()

    # B2: Lấy từng biến từ dữ liệu người dùng gửi
    try:
        age = float(data["age"])
        bmi = float(data["bmi"])
        gender = int(data["gender"])
        smoking_history = int(data["smoking_history"])
        hypertension = int(data["hypertension"])
        heart_disease = int(data["heart_disease"])
        blood_glucose_level = float(data["blood_glucose_level"])
        HbA1c_level = float(data["HbA1c_level"])

        # B3: Tạo input đúng định dạng cho mô hình
        input_data = np.array([[gender, age, hypertension, heart_disease, smoking_history,
                                bmi, HbA1c_level, blood_glucose_level]])

        # B4: Dự đoán
        prediction = model.predict(input_data)[0]

        # B5: Trả kết quả JSON
        return jsonify({
            "diabetes_prediction": int(prediction)  # 0: Không bị, 1: Có khả năng bị
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# === Chạy app nếu chạy trực tiếp ===
if __name__ == "__main__":
    app.run(debug=True)
