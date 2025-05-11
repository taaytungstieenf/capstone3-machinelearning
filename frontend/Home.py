#test new tokens

import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Dự đoán Tiểu Đường",
    layout="wide",
    page_icon="🩺",)

st.markdown("""
    <style>
    .top-line {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background-color: #1abc9c;
        z-index: 10000;
    }
    </style>
    <div class="top-line"></div>
""", unsafe_allow_html=True)

# Thêm CSS định dạng
st.markdown("""
    <style>
    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #ffffff;
        padding: 15px 0;
        border-bottom: 1px solid #ddd;
        z-index: 9999;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 26px;
        font-weight: bold;
        color: #2c3e50;
    }

    .main-content {
        padding-top: 90px; /* Đẩy nội dung xuống dưới header */
    }

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

# Header
st.markdown("""
    <h1 style='
        text-align: center;
        color: #1e81b0;
        font-size: 50px;
        font-weight: 600;
        margin-bottom: 0px;
    '>
        ỨNG DỤNG DỰ ĐOÁN TIỂU ĐƯỜNG
    </h2>
""", unsafe_allow_html=True)

# Nội dung chính
st.markdown('<div class="main-content">', unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 2])

with col1:
    st.markdown("""
    ### Chức Năng Chính Của Dự Án:
    - 📂 Khám phá tập dữ liệu để hiểu thêm về các thông số và mẫu dữ liệu
    - 🔍 Phân tách và đánh giá tập dữ liệu
    - 🚀 Đánh giá các mô hình tương đồng trên cùng tập dữ liệu
    - 📊 Dự đoán nguy cơ mắc tiểu đường dựa trên các chỉ số cơ thể
    - 📈 Mô tả tổng quát các chỉ số cơ thể trên biểu đồ 
    """)

    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)

    image = Image.open("../images/diabetes1.jpg")
    st.image(image, caption="", use_container_width=True)

with col2:
    image = Image.open("../images/diabetes2.jpg")
    st.image(image, caption="", use_container_width=True)

# Đóng thẻ div cho main-content
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        © 2025 Nguyễn Đức Tây | All rights reserved.
    </div>
""", unsafe_allow_html=True)