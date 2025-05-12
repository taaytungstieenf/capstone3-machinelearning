import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(layout="wide")

# Tiêu đề chính
st.markdown("<h1 style='text-align: center; color: #21130d;'>Giới Thiệu Sơ Bộ Về Tập Dữ Liệu CSV</h1>", unsafe_allow_html=True)

#st.markdown("<br><br>", unsafe_allow_html=True)

# Đưa uploader vào thanh bên
st.sidebar.markdown("### 📂 Tải lên tệp CSV")
uploaded_file = st.sidebar.file_uploader("", type=["csv"])

# Khởi tạo session_state nếu chưa có
if "preview_data" not in st.session_state:
    st.session_state.preview_data = None
if "summary_data" not in st.session_state:
    st.session_state.summary_data = None
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# Lưu trữ file đã tải lên vào session_state
if uploaded_file is not None:
    st.session_state.uploaded_file = uploaded_file

# Kiểm tra nếu có file trong session_state
if st.session_state.uploaded_file is not None:
    uploaded_file = st.session_state.uploaded_file

    try:
        # Nếu đã có dữ liệu preview_data và summary_data thì không gửi lại yêu cầu API
        if st.session_state.preview_data is None or st.session_state.summary_data is None:
            # Đọc nội dung file một lần duy nhất
            file_bytes = uploaded_file.read()

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

        else:
            st.info("✅ Dữ liệu đã được tải và lưu trong session.")

    except Exception as e:
        st.error(f"❌ Không thể kết nối đến API: {e}")

    # Tabs hiển thị dữ liệu
    if st.session_state.preview_data or st.session_state.summary_data:
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
