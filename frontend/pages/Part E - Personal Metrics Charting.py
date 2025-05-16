import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from database.database_functions import get_predictions_from_db

st.set_page_config(
    page_title="EDA",
    layout="wide",
    page_icon="⚕️"
)
st.markdown("<h1 style='text-align: center; color: #21130d;'>Báo Cáo Tình Trạng Sức Khỏe</h1>", unsafe_allow_html=True)
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

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

predictions = get_predictions_from_db()

if not predictions:
    st.warning("⚠️ Không có dữ liệu để hiển thị.")
else:
    latest = predictions[0]
    name, dob = latest[1], latest[2]
    age, gender, bmi, glucose, hba1c, prediction, timestamp = latest[3:]

    st.markdown(f"""
    <div style="font-size: 16px; padding: 4px 0;">
        👤 <b>Họ tên:</b> {name} | 📅 <b>Ngày sinh:</b> {dob} | 🕒 <b>Thời gian:</b> {timestamp} | 🧪 <b>Kết quả:</b> {'<span style="color:red;">🚨 Nguy cơ tiểu đường</span>' if prediction == 1 else '<span style="color:green;">✅ Không có nguy cơ</span>'}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

    # Giá trị và ngưỡng
    labels = ['BMI', 'Đường huyết (mg/dL)', 'HbA1c (%)']
    values = [bmi, glucose, hba1c]
    thresholds = [24.9, 130, 7]  # Ngưỡng tối đa cho vùng an toàn

    def get_color(val, threshold):
        if val <= threshold:
            return '#58D68D'
        elif val <= threshold * 1.15:
            return '#F4D03F'
        else:
            return '#EC7063'

    colors = [get_color(v, t) for v, t in zip(values, thresholds)]

    # Tạo biểu đồ
    fig, ax = plt.subplots(figsize=(7, 5))

    bars = ax.bar(
        labels, values,
        color=colors, width=0.5, edgecolor='black', linewidth=0.7
    )

    # Vẽ các mức threshold
    for i, threshold in enumerate(thresholds):
        ax.axhline(
            y=threshold, color='purple', linestyle='--', linewidth=1,
            label=f'Ngưỡng {i + 1}: {threshold}'
        )

    # Hiển thị legend
    ax.legend(loc='upper right', fontsize=9)

    # Tạo trục phụ bên phải
    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    ax2.set_yticks(thresholds)
    ax2.set_yticklabels([str(t) for t in thresholds], fontsize=9, color='purple')
    ax2.tick_params(axis='y', length=0)
    ax2.get_xaxis().set_visible(False)

    # Ghi nhãn
    ax.set_ylabel("Giá trị", fontsize=12, rotation=0, labelpad=40)
    ax.set_title("Biểu Đồ Sức Khỏe", fontsize=15, color='#333')

    # Thêm giá trị trên đầu cột
    ax.bar_label(bars, fmt='%.1f', fontsize=10, rotation=0, label_type='edge', padding=3)

    # Thêm lưới và legend
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.legend(loc='upper right', fontsize=9)

    # Tinh chỉnh trục x
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=10)

    # Gọn layout
    plt.tight_layout()
    plt.show()

    # Chia giao diện 2 cột
    col1, col2 = st.columns([1.25, 1])

    with col1:
        st.pyplot(fig)

    with col2:
        st.markdown("<h3 style='text-align: center; color: #21130d;'>🔍 Đánh giá chỉ số</h3>", unsafe_allow_html=True)

        # BMI
        if bmi < 18.5:
            st.warning(f"**BMI = {bmi:.1f}**: Thiếu cân. Bạn nên trao đổi với bác sĩ để kiểm tra dinh dưỡng.")
        elif bmi <= 24.9:
            st.success(f"**BMI = {bmi:.1f}**: Bình thường. Bạn đang có cân nặng lý tưởng.")
        elif bmi <= 29.9:
            st.warning(f"**BMI = {bmi:.1f}**: Thừa cân. Nên theo dõi chế độ ăn uống và vận động.")
        else:
            st.error(f"**BMI = {bmi:.1f}**: Béo phì. Nguy cơ cao với các bệnh chuyển hoá, hãy tham khảo chuyên gia y tế.")

        # Glucose
        if glucose < 80:
            st.warning(f"**Đường huyết = {glucose:.1f} mg/dL**: Có thể là hạ đường huyết. Hãy kiểm tra lại lúc đói.")
        elif glucose <= 130:
            st.success(f"**Đường huyết = {glucose:.1f} mg/dL**: Trong giới hạn bình thường.")
        elif glucose <= 180:
            st.warning(f"**Đường huyết = {glucose:.1f} mg/dL**: Sau ăn hơi cao, nên theo dõi thêm.")
        else:
            st.error(f"**Đường huyết = {glucose:.1f} mg/dL**: Vượt mức cho phép, nguy cơ tiểu đường cao.")

        # HbA1c
        if hba1c < 5.7:
            st.success(f"**HbA1c = {hba1c:.1f}%**: Bình thường.")
        elif hba1c <= 6.4:
            st.warning(f"**HbA1c = {hba1c:.1f}%**: Tiền tiểu đường. Cần kiểm soát chế độ ăn uống và luyện tập.")
        else:
            st.error(f"**HbA1c = {hba1c:.1f}%**: Nguy cơ tiểu đường rõ rệt. Nên gặp bác sĩ để được tư vấn.")

        st.info("👉 Xin hãy cập nhật chỉ số sức khoẻ thường xuyên để kịp thời phòng ngừa bệnh.")
