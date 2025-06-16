import streamlit as st
import pandas as pd
import io

# --- 1. Configuration (Cấu hình tập trung) ---
class AppConfig:
    PAGE_TITLE = "Introduction"
    PAGE_ICON = "⚕️"
    HEADER_HTML = """
    <h1 style='text-align: center;
               color: #2c3e50;
               font-size: 40px;
               font-family: "Trebuchet MS", sans-serif;
               text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);'>
        ℹ️ Giới Thiệu Tập Dữ Liệu
    </h1>
    """
    FOOTER_HTML = """
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
    """
    PREVIEW_ROWS = 10 # Số dòng mặc định để xem trước

# --- 2. Data Processor (Tách biệt logic xử lý dữ liệu) ---
class DataProcessor:
    @staticmethod
    @st.cache_data # Cache kết quả xử lý dữ liệu
    def process_uploaded_csv(uploaded_file_io: io.BytesIO):
        """Đọc và xử lý tệp CSV được tải lên, trả về dữ liệu xem trước và tóm tắt."""
        try:
            df = pd.read_csv(uploaded_file_io)

            # Preview data
            preview_data = df.head(AppConfig.PREVIEW_ROWS).to_dict(orient="records")

            # Summary data
            summary_data = {
                "num_rows": df.shape[0],
                "num_columns": df.shape[1],
                "columns": list(df.columns),
                "dtypes": df.dtypes.astype(str).to_dict(),
                "describe": df.describe(include='all').fillna("").to_dict()
            }
            return preview_data, summary_data
        except pd.errors.EmptyDataError:
            raise ValueError("Tệp CSV trống. Vui lòng tải lên một tệp có dữ liệu.")
        except pd.errors.ParserError:
            raise ValueError("Không thể đọc tệp CSV. Vui lòng kiểm tra định dạng tệp.")
        except Exception as e:
            raise Exception(f"Đã xảy ra lỗi khi xử lý tệp: {e}")

# --- 3. UI Renderer (Tách biệt logic hiển thị UI) ---
class UIRenderer:
    @staticmethod
    def setup_page_config():
        """Thiết lập cấu hình trang Streamlit và hiển thị header."""
        st.set_page_config(
            page_title=AppConfig.PAGE_TITLE,
            layout="wide",
            page_icon=AppConfig.PAGE_ICON
        )
        st.markdown(AppConfig.HEADER_HTML, unsafe_allow_html=True)

    @staticmethod
    def display_footer():
        """Hiển thị footer của ứng dụng."""
        st.markdown(AppConfig.FOOTER_HTML, unsafe_allow_html=True)

    @staticmethod
    def display_data_tabs(preview_data, summary_data):
        """Hiển thị các tab với dữ liệu xem trước và tóm tắt."""
        tab1, tab2, tab3 = st.tabs(["📄 Xem trước dữ liệu", "🆔 Tên cột và kiểu dữ liệu", "📊 Thống kê tổng quát"])

        with tab1:
            if preview_data:
                df_preview = pd.DataFrame(preview_data)
                st.dataframe(df_preview, use_container_width=True)
            else:
                st.info("⏳ Chưa có dữ liệu xem trước.")

        with tab2:
            if summary_data:
                st.markdown(
                    f"**🔢 Số dòng:** `{summary_data['num_rows']}` &nbsp; **🔠 Số cột:** `{summary_data['num_columns']}`",
                    unsafe_allow_html=True
                )
                col_info_df = pd.DataFrame({
                    "Tên cột": summary_data["columns"],
                    "Kiểu dữ liệu": [summary_data["dtypes"].get(col, "Không rõ") for col in summary_data["columns"]]
                })
                st.dataframe(col_info_df, use_container_width=True)
            else:
                st.info("⏳ Chưa có dữ liệu thống kê.")

        with tab3:
            if summary_data:
                describe_df = pd.DataFrame(summary_data["describe"])
                st.dataframe(describe_df, use_container_width=True)
            else:
                st.info("⏳ Chưa có dữ liệu thống kê.")

# --- 4. Main Application Logic ---
def main():
    UIRenderer.setup_page_config()
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True) # Spacer

    # Khởi tạo session_state một cách an toàn và gọn gàng hơn
    # chỉ khởi tạo nếu chưa có
    st.session_state.setdefault("preview_data", None)
    st.session_state.setdefault("summary_data", None)
    st.session_state.setdefault("uploaded_file_obj", None) # Đổi tên biến để tránh nhầm lẫn với `uploaded_file` cục bộ

    # File uploader
    uploaded_file = st.sidebar.file_uploader("Tải lên tệp CSV", type=["csv"], key="csv_uploader")

    # Xử lý khi có tệp mới được tải lên
    if uploaded_file is not st.session_state.uploaded_file_obj: # Kiểm tra xem tệp mới có khác với tệp đã xử lý trước đó không
        st.session_state.uploaded_file_obj = uploaded_file
        if uploaded_file is not None:
            # Clear cache để xử lý tệp mới
            st.cache_data.clear()
            file_bytes = uploaded_file.read()
            file_io = io.BytesIO(file_bytes)
            try:
                st.session_state.preview_data, st.session_state.summary_data = DataProcessor.process_uploaded_csv(file_io)
            except Exception as e:
                st.error(f"❌ Lỗi xử lý tệp: {e}")
                st.session_state.preview_data = None
                st.session_state.summary_data = None
        else:
            # Reset dữ liệu nếu người dùng xóa tệp đã tải lên
            st.session_state.preview_data = None
            st.session_state.summary_data = None


    # Hiển thị dữ liệu nếu đã có
    if st.session_state.preview_data or st.session_state.summary_data:
        UIRenderer.display_data_tabs(st.session_state.preview_data, st.session_state.summary_data)
    else:
        st.info("⏳ Vui lòng tải lên tệp CSV để xem thông tin.")

    UIRenderer.display_footer()

if __name__ == "__main__":
    main()