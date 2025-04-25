import mysql.connector
from datetime import datetime
import os

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '246357',
    'database': 'diabetesDB',
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            dob DATE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT,
            gender INT,
            age FLOAT,
            hypertension INT,
            heart_disease INT,
            smoking_history INT,
            bmi FLOAT,
            HbA1c_level FLOAT,
            blood_glucose_level FLOAT,
            prediction INT,
            timestamp DATETIME,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    ''')

    conn.commit()
    conn.close()

def get_or_create_patient(name, dob):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM patients WHERE name = %s AND dob = %s", (name, dob))
    result = cursor.fetchone()
    if result:
        patient_id = result[0]
    else:
        cursor.execute("INSERT INTO patients (name, dob) VALUES (%s, %s)", (name, dob))
        conn.commit()
        patient_id = cursor.lastrowid
    conn.close()
    return patient_id

def save_prediction(data: dict, prediction: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    patient_id = get_or_create_patient(data["name"], data["dob"])

    cursor.execute('''
        INSERT INTO predictions (
            patient_id, gender, age, hypertension, heart_disease,
            smoking_history, bmi, HbA1c_level, blood_glucose_level,
            prediction, timestamp
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        patient_id, data["gender"], data["age"], data["hypertension"], data["heart_disease"],
        data["smoking_history"], data["bmi"], data["HbA1c_level"], data["blood_glucose_level"],
        prediction, datetime.now()
    ))
    conn.commit()
    conn.close()

init_db()