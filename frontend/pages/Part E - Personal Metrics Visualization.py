import streamlit as st
import matplotlib.pyplot as plt
import sys
import os
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from database.database_functions import get_predictions_from_db

st.set_page_config(
    page_title="Visualization",
    layout="wide",
    page_icon="⚕️"
)
st.markdown(
    """
    <h1 style='text-align: center;
               color: #2c3e50;
               font-size: 40px;
               font-family: "Trebuchet MS", sans-serif;
               text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);'>
        📊 Báo Cáo Tình Trạng Sức Khỏe
    </h1>
    """,
    unsafe_allow_html=True
)
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
        <b>Họ tên:</b> {name} | <b>Ngày sinh:</b> {dob} | <b>Thời gian:</b> {timestamp} | <b>Kết quả:</b> {'<span style="color:red;"> Nguy cơ tiểu đường</span>' if prediction == 1 else '<span style="color:green;">Không có nguy cơ</span>'}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

    # Giá trị và ngưỡng theo thứ tự: BMI, Glucose, HbA1c
    metrics = {
        'BMI (kg/m²)': {'value': bmi, 'threshold': 24.9},
        'Glucose (mg/dL)': {'value': glucose, 'threshold': 130},
        'HbA1c (%)': {'value': hba1c, 'threshold': 7}
    }

    # Hàm xác định màu theo giá trị và ngưỡng
    def get_color(val, threshold):
        if val <= threshold:
            return '#58D68D'  # xanh lá
        elif val <= threshold * 1.15:
            return '#F4D03F'  # vàng
        else:
            return '#EC7063'  # đỏ


    # Trích xuất labels, values, thresholds, colors
    labels = list(metrics.keys())
    values = [metrics[label]['value'] for label in labels]
    thresholds = [metrics[label]['threshold'] for label in labels]
    colors = [get_color(val, thr) for val, thr in zip(values, thresholds)]

    # Tạo biểu đồ
    fig, ax = plt.subplots(figsize=(7, 5))

    bars = ax.bar(
        labels, values,
        color=colors, width=0.5, edgecolor='black', linewidth=0.7
    )

    # Vẽ các ngưỡng
    for label in labels:
        threshold = metrics[label]['threshold']
        ax.axhline(
            y=threshold, color='blue', linestyle='-', linewidth=1,
            label=f'{label}: {threshold}'
        )

    # Hiển thị legend (tránh lặp lại cùng label)
    handles, legend_labels = ax.get_legend_handles_labels()
    unique = dict(zip(legend_labels, handles))
    ax.legend(unique.values(), unique.keys(), loc='upper right', fontsize=9)

    # Tạo trục phụ bên phải
    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    ax2.set_yticks(thresholds)
    ax2.set_yticklabels([str(t) for t in thresholds], fontsize=9, color='blue')
    ax2.tick_params(axis='y', length=0)
    ax2.get_xaxis().set_visible(False)

    # Ghi nhãn
    ax.set_ylabel("Giá trị", fontsize=12, rotation=0, labelpad=40)
    ax.set_title("Biểu Đồ Sức Khỏe", fontsize=15, color='#333')

    # Thêm giá trị trên đầu cột
    ax.bar_label(bars, fmt='%.1f', fontsize=10, rotation=0, label_type='edge', padding=3)

    # Thêm lưới và legend
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.legend(
        unique.values(), unique.keys(),
        loc='upper right',
        fontsize=9,
        frameon=True,
        facecolor='white',
        edgecolor='gray',
        fancybox=True,  # làm bo góc đẹp hơn (tuỳ chọn)
        framealpha=1  # <== QUAN TRỌNG: không trong suốt
    )

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

        # Lưu biểu đồ vào bộ nhớ đệm dưới dạng PNG
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png')
        img_buffer.seek(0)

        # Tạo nút tải xuống
        st.download_button(
            label="Tải biểu đồ",
            data=img_buffer,
            file_name='bieu_do_suc_khoe.png',
            mime='image/png'
        )

    with col2:
        st.markdown("<h3 style='text-align: center; color: #21130d;'>🤓 Đánh giá chỉ số</h3>", unsafe_allow_html=True)

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

        st.info("👉 Xin hãy cập nhật chỉ số sức khoẻ thường xuyên để phòng ngừa bệnh kịp thời.")

        st.markdown("<h3 style='text-align: center; color: #21130d;'>🤔 Lời khuyên cho bạn</h3>", unsafe_allow_html=True)

        if prediction == 1:
            # 👉 Người CÓ nguy cơ tiểu đường
            st.markdown(
                """
                <div style="
                    background-color: #f9f9f9;
                    padding: 15px;
                    border-left: 5px solid gray;
                    border-radius: 8px;
                    font-size: 16px;
                ">
                    - Việc kiểm soát tốt đường huyết mỗi ngày sẽ giúp bạn sống khỏe mạnh và phòng ngừa biến chứng, hãy kiên trì với chế độ ăn uống và luyện tập phù hợp.<br>
                    - Hãy duy trì theo dõi sức khỏe định kỳ và trao đổi thường xuyên với bác sĩ để có hướng điều trị hiệu quả nhất.
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            # 👉 Người KHÔNG có nguy cơ
            st.markdown(
                """
                <div style="
                    background-color: #f9f9f9;
                    padding: 15px;
                    border-left: 5px solid gray;
                    border-radius: 8px;
                    font-size: 16px;
                ">
                    - Bạn đang duy trì một lối sống lành mạnh, hãy tiếp tục vận động đều đặn và ăn uống cân bằng để giữ vững sức khỏe lâu dài.<br>
                    - Chỉ số của bạn đang trong ngưỡng an toàn, một dấu hiệu rất tích cực! Hãy tiếp tục chăm sóc cơ thể mỗi ngày với thói quen tốt hiện tại.
                </div>
                """,
                unsafe_allow_html=True
            )