import streamlit as st
import requests
import mysql.connector

from backend.db import clear_predictions  # Import để dùng nút xóa

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '246357',
    'database': 'diabetesDB',
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_predictions_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions ORDER BY timestamp DESC LIMIT 10")
    predictions = cursor.fetchall()
    conn.close()
    return predictions

def display_predictions(predictions):
    st.subheader("Lịch sử dự đoán gần đây")
    if len(predictions) == 0:
        st.write("Không có dữ liệu dự đoán.")
    else:
        for pred in predictions:
            st.write(f"ID: {pred[0]}, Tuổi: {pred[2]}, Giới tính: {'Nam' if pred[1] == 1 else 'Nữ'}, BMI: {pred[6]}, Dự đoán: {'Có nguy cơ' if pred[9] == 1 else 'Không có nguy cơ'}, Thời gian: {pred[10]}")

st.set_page_config(page_title="Dự đoán Tiểu Đường", page_icon="🩺", layout="centered")

st.markdown("""
    <style>
        .big-font {
            font-size:24px !important;
            font-weight: bold;
            color: #2c3e50;
        }
        .small-note {
            font-size: 13px;
            color: gray;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='big-font'>🩺 Ứng dụng Dự đoán Bệnh Tiểu Đường</h1>", unsafe_allow_html=True)
st.markdown("#### Hãy nhập thông tin sức khỏe của bạn để hệ thống dự đoán nguy cơ mắc bệnh tiểu đường.")

with st.form("diabetes_form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("👵 Tuổi", min_value=0, max_value=120, value=30)
        gender = st.selectbox("⚧️ Giới tính", ["Nam", "Nữ"])
        bmi = st.number_input("⚖️ BMI", min_value=10.0, max_value=60.0, value=22.5)
        smoking_history = st.selectbox("🚬 Tiền sử hút thuốc", ["Không", "Trung bình", "Nặng"])

    with col2:
        hypertension = st.selectbox("💓 Tăng huyết áp", ["Không", "Có"])
        heart_disease = st.selectbox("❤️ Bệnh tim", ["Không", "Có"])
        glucose = st.number_input("🩸 Mức đường huyết (mg/dL)", min_value=50.0, max_value=400.0, value=120.0)
        hba1c = st.number_input("🧪 HbA1c (%)", min_value=3.0, max_value=15.0, value=5.5)

    submit_btn = st.form_submit_button("📊 Dự đoán nguy cơ")

gender_map = {"Nam": 1, "Nữ": 0}
smoke_map = {"Không": 0, "Trung bình": 1, "Nặng": 2}

if submit_btn:
    with st.spinner("⏳ Đang phân tích..."):
        input_data = {
            "age": age,
            "bmi": bmi,
            "gender": gender_map[gender],
            "smoking_history": smoke_map[smoking_history],
            "hypertension": 1 if hypertension == "Có" else 0,
            "heart_disease": 1 if heart_disease == "Có" else 0,
            "blood_glucose_level": glucose,
            "HbA1c_level": hba1c
        }

        try:
            response = requests.post("http://localhost:5000/predict", json=input_data)
            result = response.json()

            if "diabetes_prediction" in result:
                pred = result["diabetes_prediction"]
                if pred == 1:
                    st.error("🔴 **Kết quả:** Có NGUY CƠ bị TIỂU ĐƯỜNG.\n\nHãy liên hệ với bác sĩ để được kiểm tra thêm.")
                else:
                    st.success("🟢 **Kết quả:** Không có dấu hiệu tiểu đường theo mô hình.")
            else:
                st.warning("Lỗi trong kết quả trả về: " + str(result))

        except Exception as e:
            st.error(f"❌ Lỗi kết nối đến API: {e}")

# Hiển thị các dự đoán gần đây từ database
predictions = get_predictions_from_db()
display_predictions(predictions)

st.markdown("---")
if st.button("🗑️ Xóa tất cả lịch sử dự đoán"):
    try:
        clear_predictions()
        st.success("✅ Đã xóa toàn bộ lịch sử dự đoán.")
    except Exception as e:
        st.error(f"❌ Không thể xóa dữ liệu: {e}")
