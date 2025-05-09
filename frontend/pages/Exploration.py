import streamlit as st
import pandas as pd
import requests

st.title("Khám phá dữ liệu CSV")

uploaded_file = st.file_uploader("Chọn file CSV", type=["csv"])

if uploaded_file is not None:
    if st.button("Xem trước 10 dòng đầu"):
        files = {"file": uploaded_file.getvalue()}
        try:
            response = requests.post("http://localhost:8000/preview", files={"file": uploaded_file})
            if response.status_code == 200:
                preview_data = response.json()["preview"]
                df = pd.DataFrame(preview_data)
                st.write("📄 10 dòng đầu của file:")
                st.dataframe(df)
            else:
                st.error(f"Lỗi từ server: {response.json().get('error')}")
        except Exception as e:
            st.error(f"Không thể kết nối đến API: {e}")
