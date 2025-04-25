import streamlit as st
import requests
import mysql.connector

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
    cursor.execute('''
        SELECT p.id, pt.name, pt.dob, p.age, p.gender, p.bmi, p.blood_glucose_level,
               p.HbA1c_level, p.prediction, p.timestamp
        FROM predictions p
        JOIN patients pt ON p.patient_id = pt.id
        ORDER BY p.timestamp DESC
        LIMIT 10
    ''')
    predictions = cursor.fetchall()
    conn.close()
    return predictions

def display_predictions(predictions):
    st.subheader("🧾 Lịch sử dự đoán gần đây")
    if not predictions:
        st.write("Không có dữ liệu dự đoán.")
    else:
        for pred in predictions:
            st.write(f"""
            👤 Tên: {pred[1]} | 🎂 Ngày sinh: {pred[2]}  
            🧓 Tuổi: {pred[3]} | ⚧️ Giới tính: {'Nam' if pred[4] == 1 else 'Nữ'} | ⚖️ BMI: {pred[5]}  
            🩸 Glucose: {pred[6]} | HbA1c: {pred[7]}  
            📊 Kết quả: {'🚨 Có nguy cơ' if pred[8] == 1 else '✅ Không có nguy cơ'} | 🕒 {pred[9]}
            """)

st.set_page_config(page_title="Dự đoán Tiểu Đường", page_icon="🩺", layout="centered")

st.markdown(
    """
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
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='big-font'>🩺 Ứng dụng Dự đoán Bệnh Tiểu Đường</h1>", unsafe_allow_html=True)

st.markdown("#### 👤 Nhập thông tin cá nhân")

with st.form("patient_form"):
    name = st.text_input("👤 Họ tên")
    dob = st.date_input("📅 Ngày sinh")
    st.markdown("#### 🧬 Thông tin sức khỏe")

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
    if not name or not dob:
        st.warning("❗ Vui lòng nhập đầy đủ họ tên và ngày sinh.")
    else:
        with st.spinner("⏳ Đang phân tích..."):
            input_data = {
                "name": name,
                "dob": dob.strftime("%Y-%m-%d"),
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
                        st.error("🔴 **Kết quả:** Có NGUY CƠ bị TIỂU ĐƯỜNG.")
                    else:
                        st.success("🟢 **Kết quả:** Không có dấu hiệu tiểu đường.")
                else:
                    st.warning("Lỗi trong kết quả trả về: " + str(result))
            except Exception as e:
                st.error(f"❌ Lỗi kết nối đến API: {e}")

# Hiển thị dự đoán gần đây
predictions = get_predictions_from_db()
display_predictions(predictions)
