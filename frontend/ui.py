import streamlit as st
import requests
from datetime import date
from utils.funcs import get_predictions_from_db, delete_all_predictions, display_predictions

st.set_page_config(page_title="Dự đoán Tiểu Đường", page_icon="🩺", layout="wide")

# CSS
st.markdown("""
<style> ... </style>
""", unsafe_allow_html=True)

# Tiêu đề
st.markdown(
    """
    <style>
        .app-title {
            text-align: center;
            padding-top: 10px;
            padding-bottom: 30px;
        }
        .app-title h1 {
            font-size: 42px;
            font-weight: bold;
            background: -webkit-linear-gradient(left, #2C3E50, #3498DB);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            margin: 0;
        }
    </style>
    <div class="app-title">
        <h1>🩺 Ứng dụng Dự đoán Bệnh Tiểu Đường</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Form nhập liệu ---
col_left, col_right = st.columns([1.2, 1])
with col_left:
    st.markdown("#### 👤 Nhập thông tin cá nhân")
    with st.form("patient_form"):
        name = st.text_input("👤 Họ tên")
        dob = st.date_input("📅 Ngày sinh", value=date(1990, 1, 1),
                            min_value=date(1900, 1, 1), max_value=date.today())
        st.markdown("#### 🧬 Thông tin sức khỏe")
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
    predictions = get_predictions_from_db()
    display_predictions(predictions, st)

    st.markdown("---")
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
