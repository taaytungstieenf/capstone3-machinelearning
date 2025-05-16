import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Introduction", layout="wide", page_icon="⚕️",)
st.markdown(
    """
    <h1 style='text-align: center;
               color: #2c3e50;
               font-size: 40px;
               font-family: "Trebuchet MS", sans-serif;
               text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);'>
        ℹ️ Giới Thiệu Tập Dữ Liệu
    </h1>
    """,
    unsafe_allow_html=True
)



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
        z-index: 999;
    }
    </style>
    <div class="footer">
        © 2025 Nguyễn Đức Tây | All rights reserved.
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader("", type=["csv"]) # Đặt thanh upload dataset ở sidebar của streamlit

# Khởi tạo session_state
if "preview_data" not in st.session_state:
    st.session_state.preview_data = None
if "summary_data" not in st.session_state:
    st.session_state.summary_data = None
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# Lưu trữ file đã tải lên vào session_state (giữ tập dữ liệu khi chuyển tab trên sidebar)
if uploaded_file is not None:
   st.session_state.uploaded_file = uploaded_file

# Kiểm tra nếu có file trong session_state
if st.session_state.uploaded_file is not None:
    uploaded_file = st.session_state.uploaded_file
    try:
        if st.session_state.preview_data is None or st.session_state.summary_data is None: # Nếu đã có dữ liệu preview_data & summary_data thì không gửi lại API
            file_bytes = uploaded_file.read() # Đọc nội dung file một lần duy nhất

            # Gửi tới API /preview
            preview_response = requests.post(
                "http://localhost:8000/preview",
                files={"file": (uploaded_file.name, file_bytes, uploaded_file.type)}
            )

            # Reset lại stream cho lần gửi tiếp theo
            file_bytes_io = io.BytesIO(file_bytes)
            file_bytes_io.name = uploaded_file.name

            # Gửi tới API /summary
            summary_response = requests.post(
                "http://localhost:8000/summary",
                files={"file": (uploaded_file.name, file_bytes_io, uploaded_file.type)}
            )

            # Xử lý phản hồi
            if preview_response.status_code == 200:
                st.session_state.preview_data = preview_response.json()["preview"]
            else:
                st.error(f"❌ Lỗi preview: {preview_response.json().get('error')}")

            if summary_response.status_code == 200:
                st.session_state.summary_data = summary_response.json()["summary"]
            else:
                st.error(f"❌ Lỗi summary: {summary_response.json().get('error')}")

    except Exception as e:
        st.error(f"❌ Không thể kết nối đến API: {e}")

    if st.session_state.preview_data or st.session_state.summary_data: # Tạo tab hiện thị dữ liệu
        tab1, tab2, tab3 = st.tabs(["📄 Xem trước dữ liệu", "🆔 Tên cột và kiểu dữ liệu", "📊 Thống kê tổng quát"])

        with tab1:
            if st.session_state.preview_data:
                df = pd.DataFrame(st.session_state.preview_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("⏳ Chưa có dữ liệu xem trước.")

        with tab2:
            if st.session_state.summary_data:
                summary = st.session_state.summary_data

                st.markdown(
                    f"**🔢 Số dòng:** `{summary['num_rows']}` &nbsp; **🔠 Số cột:** `{summary['num_columns']}`",
                    unsafe_allow_html=True
                )

                col_info_df = pd.DataFrame({
                    "Tên cột": summary["columns"],
                    "Kiểu dữ liệu": [summary["dtypes"].get(col, "Không rõ") for col in summary["columns"]]
                })
                st.dataframe(col_info_df, use_container_width=True)
            else:
                st.info("⏳ Chưa có dữ liệu thống kê.")

        with tab3:
            if st.session_state.preview_data:
                describe_df = pd.DataFrame(summary["describe"])
                st.dataframe(describe_df, use_container_width=True)
            else:
                st.info("⏳ Chưa có dữ liệu thống kê.")

else:
    st.info("⏳ Vui lòng tải lên tệp CSV.")
