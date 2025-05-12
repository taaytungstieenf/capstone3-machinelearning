import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Diabetes EDA", layout="wide")
st.title("Mô Tả Thống Kê Tập Dữ Liệu")

# Đưa uploader vào thanh bên
st.sidebar.markdown("### 📂 Tải lên tệp CSV")
uploaded_file = st.sidebar.file_uploader("", type="csv")

# Khởi tạo session_state nếu chưa có
if "df" not in st.session_state:
    st.session_state.df = None

# Lưu trữ file đã tải lên vào session_state
if uploaded_file is not None:
    st.session_state.df = pd.read_csv(uploaded_file)
    st.session_state.uploaded_file = uploaded_file
    st.success("📄 Dataset loaded successfully!")
else:
    if st.session_state.df is None:
        st.stop()

df = st.session_state.df

# Tạo menu chọn sơ đồ trong sidebar
chart_choice = st.sidebar.radio(
    "Chọn loại sơ đồ bạn muốn xem:",
    ("Histogram - Distribution", "Boxplot - Outliers by Category", "Countplot - Categorical Frequency",
     "Correlation Heatmap", "Diabetes Rate by Group (Barplot)", "Pairplot - Feature Relationships")
)

# Tạo layout 2 cột
col1, col2 = st.columns(2)

# Hiển thị sơ đồ dựa trên lựa chọn của người dùng
if chart_choice == "Histogram - Distribution":
    with col1:
        st.subheader("1️⃣ Histogram - Distribution")
        num_col1 = st.selectbox("Select numerical column (Histogram)", df.select_dtypes(include=['float64', 'int64']).columns, key="hist")
        fig1, ax1 = plt.subplots()
        sns.histplot(df[num_col1], kde=True, bins=30, ax=ax1)
        st.pyplot(fig1)

elif chart_choice == "Boxplot - Outliers by Category":
    with col1:
        st.subheader("2️⃣ Boxplot - Outliers by Category")
        cat_col1 = st.selectbox("Select category column (Boxplot)", df.select_dtypes(include='object').columns, key="box_cat")
        num_col2 = st.selectbox("Select numerical column (Boxplot)", df.select_dtypes(include=['float64', 'int64']).columns, key="box_num")
        fig2, ax2 = plt.subplots()
        sns.boxplot(data=df, x=cat_col1, y=num_col2, ax=ax2)
        plt.xticks(rotation=45)
        st.pyplot(fig2)

elif chart_choice == "Countplot - Categorical Frequency":
    with col1:
        st.subheader("3️⃣ Countplot - Categorical Frequency")
        cat_col2 = st.selectbox("Select column (Countplot)", df.select_dtypes(include='object').columns, key="countplot")
        fig3, ax3 = plt.subplots()
        sns.countplot(data=df, x=cat_col2, order=df[cat_col2].value_counts().index, ax=ax3)
        plt.xticks(rotation=45)
        st.pyplot(fig3)

elif chart_choice == "Correlation Heatmap":
    with col2:
        st.subheader("4️⃣ Correlation Heatmap")
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        sns.heatmap(df.select_dtypes(include=['float64', 'int64']).corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax4)
        st.pyplot(fig4)

elif chart_choice == "Diabetes Rate by Group (Barplot)":
    with col2:
        st.subheader("5️⃣ Diabetes Rate by Group (Barplot)")
        group_col = st.selectbox("Group by column (Barplot)", ['gender', 'smoking_history', 'hypertension', 'heart_disease'], key="group")
        diabetes_rate = df.groupby(group_col)['diabetes'].mean().reset_index()
        fig5, ax5 = plt.subplots()
        sns.barplot(data=diabetes_rate, x=group_col, y='diabetes', ax=ax5)
        plt.ylabel("Diabetes Rate")
        plt.xticks(rotation=45)
        st.pyplot(fig5)

elif chart_choice == "Pairplot - Feature Relationships":
    with col2:
        st.subheader("6️⃣ Pairplot - Feature Relationships")
        pair_cols = st.multiselect("Select 2-4 columns (Pairplot)", df.select_dtypes(include=['float64', 'int64']).columns, max_selections=4, key="pair")
        if len(pair_cols) >= 2:
            fig6 = sns.pairplot(df[pair_cols + ['diabetes']], hue="diabetes", diag_kind='kde')
            st.pyplot(fig6)
        else:
            st.info("ℹ️ Select at least 2 columns.")
