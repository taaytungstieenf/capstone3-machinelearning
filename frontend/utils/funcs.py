import mysql.connector
from datetime import date

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '246357',
    'database': 'diabetesDB',
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_predictions_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.id, pt.name, pt.dob, p.age, p.gender, p.bmi, p.blood_glucose_level,
               p.HbA1c_level, p.prediction, p.timestamp
        FROM predictions p
        JOIN patients pt ON p.patient_id = pt.id
        ORDER BY p.timestamp DESC
        LIMIT 10
    ''')
    predictions = cursor.fetchall()
    conn.close()
    return predictions

def delete_all_predictions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions")
    cursor.execute("DELETE FROM patients")
    conn.commit()
    conn.close()

def display_predictions(predictions, st):
    st.subheader("🧾 Lịch sử dự đoán gần đây")

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
