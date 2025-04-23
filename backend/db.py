# database.py
import mysql.connector
from datetime import datetime
import os

# Cấu hình kết nối MySQL
DB_CONFIG = {
    'host': 'localhost',  # Địa chỉ máy chủ MySQL
    'user': 'root',  # Tên người dùng MySQL
    'password': '246357',  # Mật khẩu MySQL
    'database': 'diabetesDB',  # Tên cơ sở dữ liệu
}

# Hàm tạo kết nối tới MySQL
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Tạo bảng nếu chưa có
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            gender INT,
            age FLOAT,
            hypertension INT,
            heart_disease INT,
            smoking_history INT,
            bmi FLOAT,
            HbA1c_level FLOAT,
            blood_glucose_level FLOAT,
            prediction INT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

# Lưu bản ghi dự đoán
def save_prediction(data: dict, prediction: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO predictions (
            gender, age, hypertension, heart_disease,
            smoking_history, bmi, HbA1c_level, blood_glucose_level,
            prediction, timestamp
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        data["gender"], data["age"], data["hypertension"], data["heart_disease"],
        data["smoking_history"], data["bmi"], data["HbA1c_level"], data["blood_glucose_level"],
        prediction, datetime.now()
    ))
    conn.commit()
    conn.close()

# Gọi 1 lần khi khởi chạy để đảm bảo bảng được tạo
init_db()
