import streamlit as st

# Cấu hình trang
st.set_page_config(page_title="Ứng dụng Dự đoán Tiểu Đường", layout="wide")

# Tiêu đề
st.title("🧬 Ứng Dụng Dự Đoán Tiểu Đường")

# Phần giới thiệu
st.markdown("""
Chào mừng bạn đến với **Ứng Dụng Dự Đoán Tiểu Đường**! 🌟

Ứng dụng này sẽ giúp bạn:
- 📊 **Dự đoán nguy cơ mắc tiểu đường** dựa trên các thông tin cá nhân của bạn.
- 📂 **Khám phá dữ liệu CSV** để hiểu thêm về thông tin và mẫu dữ liệu tiểu đường.

Vui lòng chọn một chức năng từ **menu bên trái** để bắt đầu!

### Hướng dẫn sử dụng:
1. Chọn **"Dự đoán nguy cơ tiểu đường"** và nhập thông tin cá nhân của bạn để nhận kết quả dự đoán.
2. Chọn **"Khám phá dữ liệu CSV"** để tải lên tập tin và phân tích thông tin tiểu đường.
""", unsafe_allow_html=True)

# Phần giới thiệu thêm (có thể dùng hình ảnh hoặc biểu tượng)
st.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Diabetes_mellitus_type_2_%28CIM_5%29.svg/1200px-Diabetes_mellitus_type_2_%28CIM_5%29.svg.png",
    caption="Bệnh tiểu đường type 2", use_column_width=True)

# Thêm một số phần tử đẹp
st.markdown("---")  # Dòng ngăn cách giữa các phần
st.markdown("""
### Chức năng chính:
1. **Dự đoán nguy cơ tiểu đường**:
   - Bằng cách nhập thông tin của bạn vào các trường được yêu cầu, chúng tôi sẽ dự đoán nguy cơ mắc bệnh tiểu đường.

2. **Khám phá dữ liệu CSV**:
   - Bạn có thể tải lên một tệp CSV để phân tích và xem các đặc điểm của bệnh tiểu đường từ dữ liệu.
""")

# Sử dụng Expander để giấu hướng dẫn sử dụng, giúp giao diện gọn gàng
with st.expander("Hướng dẫn chi tiết"):
    st.markdown("""
    - Để dự đoán tiểu đường, bạn cần nhập các thông tin như độ tuổi, chỉ số BMI, huyết áp, lượng đường trong máu và các yếu tố khác.
    - Sau khi nhập xong, kết quả dự đoán sẽ được hiển thị ngay lập tức.
    - Đối với chức năng khám phá dữ liệu, bạn chỉ cần tải lên một tệp CSV theo định dạng chuẩn và chúng tôi sẽ giúp bạn phân tích và trực quan hóa dữ liệu.
    """)

# Thêm một phần CTA (Call To Action)
st.markdown("""
### Hãy bắt đầu khám phá ngay bây giờ!
- Chọn một chức năng từ **menu bên trái** để bắt đầu hành trình của bạn!
""")

