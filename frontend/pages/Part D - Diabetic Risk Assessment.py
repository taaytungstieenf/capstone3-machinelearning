import streamlit as st

st.set_page_config(
    page_title="EDA",
    layout="wide",
    page_icon="⚕️"
)
st.markdown("<h1 style='text-align: center; color: #21130d;'>Thực Hiện Dự Đoán Bệnh Tiểu Đường</h1>", unsafe_allow_html=True)
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)


import requests
import sys
import os

from datetime import date
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from database.database_functions import delete_all_predictions, get_predictions_from_db


# Hàm hiển thị kết quả dự đoán
def display_predictions(predictions, st):

    if not predictions:
        st.write("Không có dữ liệu dự đoán.")
    else:
        for pred in predictions:
            st.write(f"🕒 **Thời gian:** {pred[9]}")
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            with col1:
                st.write(f"👤 **Tên:** {pred[1]}")
                st.write(f"📅 **Ngày sinh:** {pred[2]}")
            with col2:
                st.write(f"👵 **Tuổi:** {pred[3]}")
                st.write(f"⚧️ **Giới tính:** {'Nam' if pred[4] == 1 else 'Nữ'}")
            with col3:
                st.write(f"⚖️ **BMI:** {pred[5]}")
                st.write(f"🩸 **Glucose:** {pred[6]}")
            with col4:
                st.write(f"🧪 **HbA1c:** {pred[7]}")
                result = '🚨 Có nguy cơ' if pred[8] == 1 else '✅ Không có nguy cơ'
                st.write(f"📊 **Kết quả:** {result}")
            st.markdown("---")


# --- Form nhập liệu ---
col_left, col_right = st.columns([1, 2])
with col_left:
    st.markdown("<h3 style='text-align: center;'>🧾 Nhập thông tin cá nhân</h3>", unsafe_allow_html=True)
    with st.form("patient_form"):
        name = st.text_input("👤 Họ tên")
        dob = st.date_input("📅 Ngày sinh", value=date(1990, 1, 1),
                            min_value=date(1900, 1, 1), max_value=date.today())
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("👵 Tuổi", 0, 120, 30)
            gender = st.selectbox("⚧️ Giới tính", ["Nam", "Nữ"])
            bmi = st.number_input("⚖️ BMI", 10.0, 60.0, 22.5)
            smoking_history = st.selectbox("🚬 Tiền sử hút thuốc", ["Không", "Trung bình", "Nặng"])
        with col2:
            hypertension = st.selectbox("💓 Tăng huyết áp", ["Không", "Có"])
            heart_disease = st.selectbox("❤️ Bệnh tim", ["Không", "Có"])
            glucose = st.number_input("🩸 Đường huyết", 50.0, 400.0, 120.0)
            hba1c = st.number_input("🧪 HbA1c", 3.0, 15.0, 5.5)
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
                    pred = result.get("diabetes_prediction", -1)
                    if pred == 1:
                        st.error("🔴 **Kết quả:** Có NGUY CƠ bị TIỂU ĐƯỜNG.")
                    elif pred == 0:
                        st.success("🟢 **Kết quả:** Không có dấu hiệu tiểu đường.")
                    else:
                        st.warning("Lỗi trong kết quả trả về.")
                except Exception as e:
                    st.error(f"❌ Lỗi kết nối đến API: {e}")

# --- Bên phải: lịch sử & xoá ---
with col_right:
    st.markdown("<h3 style='text-align: center;'>🛢️ Lịch sử dự đoán gần đây</h3>", unsafe_allow_html=True)

    with st.expander("Nhấn để xem"):
        predictions = get_predictions_from_db()
        display_predictions(predictions, st)

    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = False

    if not st.session_state.confirm_delete:
        if st.button("🗑️ Xoá toàn bộ lịch sử dự đoán"):
            st.session_state.confirm_delete = True
    else:
        st.warning("Bạn có chắc chắn muốn xoá toàn bộ lịch sử?")
        col_confirm, col_cancel = st.columns(2)
        with col_confirm:
            if st.button("✅ Đồng ý xoá"):
                try:
                    delete_all_predictions()
                    st.success("✅ Đã xoá toàn bộ lịch sử.")
                except Exception as e:
                    st.error(f"❌ Lỗi khi xoá: {e}")
                st.session_state.confirm_delete = False
        with col_cancel:
            if st.button("❌ Huỷ bỏ"):
                st.info("Đã huỷ xoá lịch sử.")
                st.session_state.confirm_delete = False

# CSS cho footer cố định
st.markdown("""
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #f0f2f6;
        color: #333;
        text-align: center;
        padding: 10px;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Footer HTML
st.markdown("""
    <div class="footer">
        © 2025 Nguyễn Đức Tây | All rights reserved.
    </div>
""", unsafe_allow_html=True)