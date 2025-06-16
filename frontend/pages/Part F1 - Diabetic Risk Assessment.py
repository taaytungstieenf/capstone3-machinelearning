import streamlit as st
import requests
import sys
import os
from datetime import date

# Thêm thư mục cha vào path để import database functions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from database.database_functions import delete_all_predictions, get_predictions_from_db


# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Assessment",
    layout="wide",
    page_icon="⚕️"
)

st.markdown("""
    <h1 style='text-align: center;
               color: #2c3e50;
               font-size: 40px;
               font-family: "Trebuchet MS", sans-serif;
               text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);'>
        🚀 Dự Đoán Bệnh Tiểu Đường
    </h1>
""", unsafe_allow_html=True)
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)


# --- HÀM HỖ TRỢ ---
def display_predictions(predictions):
    if not predictions:
        st.write("Không có dữ liệu dự đoán.")
    else:
        for pred in predictions:
            st.markdown(
                f"""
                <div style="font-size:21.7px; color:#1f77b4; font-weight:bold;">
                    Thời gian: {pred[9]}
                </div>
                """,
                unsafe_allow_html=True
            )
            col1, col2, col3, col4 = st.columns([1.25, 1, 1, 1.25])
            with col1:
                st.write(f"👤 **Tên:** {pred[1]}")
                st.write(f"📅 **Ngày sinh:** {pred[2]}")
            with col2:
                st.write(f"🔢 **Tuổi:** {pred[3]}")
                st.write(f"⚧️ **Giới tính:** {'Nam' if pred[4] == 1 else 'Nữ'}")
            with col3:
                st.write(f"📐 **BMI:** {pred[5]}")
                st.write(f"🩸 **Đường huyết:** {pred[6]}")
            with col4:
                st.write(f"💉 **HbA1c:** {pred[7]}")
                result = '🔴 Có nguy cơ' if pred[8] == 1 else '🟢 Không có nguy cơ'
                st.write(f"🔔 **Kết quả:** {result}")


def set_confirm_delete():
    st.session_state.confirm_delete = True


# --- GIAO DIỆN CHÍNH ---
col_left, col_right = st.columns([1, 2])

# --- Nhập liệu bên trái ---
with col_left:
    st.markdown("<h3 style='text-align: center;'>📝 Nhập thông tin cá nhân</h3>", unsafe_allow_html=True)
    with st.form("patient_form"):
        name = st.text_input("👤 Họ và tên")
        dob = st.date_input("📅 Ngày sinh", value=date(1990, 1, 1), min_value=date(1900, 1, 1), max_value=date.today())
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("🔢 Tuổi hiện tại", 0, 120, 30)
            gender = st.selectbox("⚧️ Giới tính", ["Nam", "Nữ"])
            smoking_history = st.selectbox("🚬 Tiền sử hút thuốc", ["Không", "Trung bình", "Nặng"])
            bmi = st.number_input("📐 Chỉ số khối cơ thể (BMI)", 10.0, 60.0, 22.5)
        with col2:
            hypertension = st.selectbox("💓 Có tăng huyết áp?", ["Không", "Có"])
            heart_disease = st.selectbox("❤️ Có tiền sử bệnh tim?", ["Không", "Có"])
            glucose = st.number_input("🩸 Chỉ số đường huyết", 50.0, 400.0, 120.0)
            hba1c = st.number_input("💉 Tỷ lệ đường trong máu (HbA1c)", 3.0, 15.0, 5.5)

        submit_btn = st.form_submit_button("Tiến hành dự đoán")

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


# --- Lịch sử dự đoán bên phải ---
with col_right:
    st.markdown("<h3 style='text-align: center;'>📜 Lịch sử dự đoán gần đây</h3>", unsafe_allow_html=True)
    with st.expander("Nhấn để xem"):
        predictions = get_predictions_from_db()
        display_predictions(predictions)

    if st.session_state.get("confirm_delete", False):
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
    else:
        st.button("Xoá toàn bộ lịch sử dự đoán", on_click=set_confirm_delete)


# --- Footer ---
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

st.markdown("""
    <div class="footer">
        © 2025 Nguyễn Đức Tây | All rights reserved.
    </div>
""", unsafe_allow_html=True)
