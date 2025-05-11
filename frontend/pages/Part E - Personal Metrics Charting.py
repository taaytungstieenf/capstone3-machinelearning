import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Cấu hình Streamlit
st.set_page_config(page_title="Diabetes Visualization", layout="centered")
sns.set(style="whitegrid")

# Sidebar
st.sidebar.title("⚙️ Tuỳ chọn")

# Upload file CSV
uploaded_file = st.sidebar.file_uploader("📁 Tải lên file CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    # Load mặc định từ thư mục gốc dự án
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    df = pd.read_csv(os.path.join(BASE_DIR, "diabetes_dataset.csv"))

# Chuyển cột phù hợp sang dạng category
for col in ['gender', 'smoking_history', 'diabetes']:
    if col in df.columns:
        df[col] = df[col].astype('category')

# Header chính
st.title("🩺 Trực quan hóa dữ liệu bệnh tiểu đường")

# Sidebar: chọn loại biểu đồ
chart_type = st.sidebar.selectbox(
    "🧭 Chọn loại biểu đồ:",
    [
        "Phân bố biến liên tục",
        "Đếm biến phân loại",
        "Tỉ lệ tiểu đường theo nhóm",
        "Phân tán giữa các đặc trưng",
        "Ma trận tương quan (Heatmap)",
        "Violin Plot theo diabetes"
    ]
)

# Kích thước biểu đồ chuẩn nhỏ gọn
figsize = (6, 4)

# Render biểu đồ
if chart_type == "Phân bố biến liên tục":
    st.header("📈 Phân bố các biến liên tục")
    for col in ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']:
        if col in df.columns:
            st.subheader(f"{col}")
            fig, ax = plt.subplots(figsize=figsize)
            sns.histplot(df[col], kde=True, ax=ax)
            fig.tight_layout()
            st.pyplot(fig)

elif chart_type == "Đếm biến phân loại":
    st.header("📊 Số lượng từng nhóm")
    for col in ['gender', 'smoking_history', 'hypertension', 'heart_disease', 'diabetes']:
        if col in df.columns:
            st.subheader(f"{col}")
            fig, ax = plt.subplots(figsize=figsize)
            sns.countplot(x=col, data=df, ax=ax)
            fig.tight_layout()
            st.pyplot(fig)

elif chart_type == "Tỉ lệ tiểu đường theo nhóm":
    st.header("📋 Tỉ lệ tiểu đường theo nhóm")
    for col in ['gender', 'smoking_history']:
        if col in df.columns:
            st.subheader(f"Theo {col}")
            fig, ax = plt.subplots(figsize=figsize)
            sns.countplot(x=col, hue='diabetes', data=df, ax=ax)
            fig.tight_layout()
            st.pyplot(fig)

elif chart_type == "Phân tán giữa các đặc trưng":
    st.header("🧬 Mối quan hệ giữa các đặc trưng")
    pairs = [('bmi', 'blood_glucose_level'), ('HbA1c_level', 'blood_glucose_level')]
    for x, y in pairs:
        if x in df.columns and y in df.columns:
            st.subheader(f"{y} vs {x}")
            fig, ax = plt.subplots(figsize=figsize)
            sns.scatterplot(data=df, x=x, y=y, hue='diabetes', ax=ax)
            fig.tight_layout()
            st.pyplot(fig)

elif chart_type == "Ma trận tương quan (Heatmap)":
    st.header("🔥 Ma trận tương quan")
    numeric_cols = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']
    existing_cols = [col for col in numeric_cols if col in df.columns]
    if existing_cols:
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.heatmap(df[existing_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
        fig.tight_layout()
        st.pyplot(fig)

elif chart_type == "Violin Plot theo diabetes":
    st.header("🎻 Phân bố BMI theo nhóm tiểu đường")
    if 'bmi' in df.columns and 'diabetes' in df.columns:
        fig, ax = plt.subplots(figsize=figsize)
        sns.violinplot(x='diabetes', y='bmi', data=df, ax=ax)
        fig.tight_layout()
        st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("🧪 Capstone 3 – Machine Learning | Streamlit Visualization © 2025")
