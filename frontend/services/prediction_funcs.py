# Hàm hiển thị kết quả dự đoán
def display_predictions(predictions, st):

    if not predictions:
        st.write("Không có dữ liệu dự đoán.")
    else:
        for pred in predictions:
            col1, col2, col3, col4 = st.columns([2, 1, 2, 2])
            with col1:
                st.write(f"👤 **Tên:** {pred[1]}")
                st.write(f"🎂 **Ngày sinh:** {pred[2]}")
            with col2:
                st.write(f"🧓 **Tuổi:** {pred[3]}")
                st.write(f"⚧️ **Giới tính:** {'Nam' if pred[4] == 1 else 'Nữ'}")
            with col3:
                st.write(f"⚖️ **BMI:** {pred[5]}")
                st.write(f"🩸 **Glucose:** {pred[6]}")
            with col4:
                st.write(f"🧪 **HbA1c:** {pred[7]}")
                result = '🚨 Có nguy cơ' if pred[8] == 1 else '✅ Không có nguy cơ'
                st.write(f"📊 **Kết quả:** {result}")
            st.write(f"🕒 **Thời gian:** {pred[9]}")
            st.markdown("---")
