import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="EDA", layout="wide", page_icon="⚕️",)
st.markdown(
    """
    <h1 style='text-align: center;
               color: #2c3e50;
               font-size: 40px;
               font-family: "Trebuchet MS", sans-serif;
               text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);'>
        🔍 Mô Tả Thống Kê Tập Dữ Liệu
    </h1>
    """,
    unsafe_allow_html=True
)

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

uploaded_file = st.sidebar.file_uploader("", type="csv")

if uploaded_file is not None:
    st.session_state.uploaded_file = uploaded_file

    df = pd.read_csv(uploaded_file)

    # Ép kiểu dữ liệu cho một số cột
    df['gender'] = df['gender'].astype('category')
    df['hypertension'] = df['hypertension'].astype('category')
    df['diabetes'] = df['diabetes'].astype('category')
    df['smoking_history'] = df['smoking_history'].astype('category')
    df['heart_disease'] = df['heart_disease'].astype('category')

    df['age'] = df['age'].astype('int64')
    df['blood_glucose_level'] = df['blood_glucose_level'].astype('int64')

    st.session_state.df = df
else:
    if "df" not in st.session_state or st.session_state.df is None:
        st.info("⏳ Vui lòng tải lên tệp CSV.")
        st.stop()

df = st.session_state.df

# Tạo menu chọn sơ đồ trong sidebar
chart_choice = st.sidebar.radio("",
    (
        "Chart 1 – Category Histogram",
        "Chart 2 – Numerical Histogram",
        "Chart 3 – Numerical Outliers Boxplot",
        "Chart 4 – Cat vs Num Boxplot",
        "Chart 5 – Significances Scatterplot",
        "Chart 6 – Correlation Heatmap"
    )
)

col1, col2, col3, col4 = st.columns([1, 0.15, 1.75, 0.15])

with col1:
    st.markdown("<h3 style='text-align: center; color: #21130d;'>📋 Kiểu dữ liệu</h3>",unsafe_allow_html=True)
    st.dataframe(df.dtypes.reset_index().rename(columns={"index": "Tên cột", 0: "Kiểu dữ liệu"}))

# Hiển thị sơ đồ dựa trên lựa chọn của người dùng
if chart_choice == "Chart 1 – Category Histogram":
    with col3:
        cat_columns = df.select_dtypes(include=['category']).columns.tolist()

        selected_col = st.selectbox("", cat_columns)

        st.write(f"### Thống kê biến `{selected_col}`")

        # Biểu đồ đếm và bảng tần suất
        fig, ax = plt.subplots()
        sns.countplot(x=selected_col, data=df, ax=ax)
        plt.xticks(rotation=0)
        st.pyplot(fig)

    with col1:
        st.markdown("<h3 style='text-align: center; color: #21130d;'>📋 Thống Kê Trên Từng Thuộc Tính</h3>",unsafe_allow_html=True)
        st.write(df[selected_col].value_counts())

elif chart_choice == "Chart 2 – Numerical Histogram":
    with col3:
        num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

        selected_num_col = st.selectbox("", num_cols)

        st.write(f"### Phân bố của `{selected_num_col}`")

        fig, ax = plt.subplots()
        sns.histplot(df[selected_num_col], kde=True, ax=ax)
        st.pyplot(fig)

        with col1:
            st.markdown("<h3 style='text-align: center; color: #21130d;'>📋 Thống Kê Trên Từng Thuộc Tính</h3>", unsafe_allow_html=True)
            st.write(df[selected_num_col].describe())

elif chart_choice == "Chart 3 – Numerical Outliers Boxplot":
    with col3:
        num_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

        selected_num_col = st.selectbox("", num_cols)

        st.write(f"### Boxplot của `{selected_num_col}`")

        fig, ax = plt.subplots()
        sns.boxplot(x=df[selected_num_col], ax=ax)
        st.pyplot(fig)

        with col1:
            st.markdown("<h3 style='text-align: center; color: #21130d;'>📋 Thống Kê Trên Từng Thuộc Tính</h3>", unsafe_allow_html=True)
            st.write(df[selected_num_col].describe())

elif chart_choice == "Chart 4 – Cat vs Num Boxplot":
    with col1:
        num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        cat_cols = df.select_dtypes(include='category').columns.tolist()

        # Chọn biến số (y) và biến phân loại (x)
        selected_y = st.selectbox("Chọn thuộc tính", num_cols)
        selected_x = st.selectbox("Chọn thuộc tính", cat_cols)
    with col3:
        st.write(f"### Boxplot: `{selected_y}` theo nhóm `{selected_x}`")

        fig, ax = plt.subplots()
        sns.boxplot(x=selected_x, y=selected_y, data=df, ax=ax)
        plt.xticks(rotation=00)
        st.pyplot(fig)

elif chart_choice == "Chart 5 – Significances Scatterplot":
    with col1:
        cat_cols = df.select_dtypes(include='category').columns.tolist()
        hue_col = st.selectbox("Chọn thuộc tính phân loại để tô màu", ["(Click chọn)"] + cat_cols)

        # Combobox 2: Chọn biến số để làm trục Y
        num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        y_col = st.selectbox("Chọn thuộc tính số", [col for col in num_cols if col != 'age'])

    with col3:
        # Vẽ scatter plot
        fig, ax = plt.subplots()
        if hue_col != "(Click chọn)":
            sns.scatterplot(data=df, x="age", y=y_col, hue=hue_col, ax=ax)
            st.write(f"### Scatter: `age` vs `{y_col}` theo `{hue_col}`")
        else:
            sns.scatterplot(data=df, x="age", y=y_col, ax=ax)
            st.write(f"### Scatter: `age` vs `{y_col}`")

        st.pyplot(fig)

elif chart_choice == "Chart 6 – Correlation Heatmap":
    with col3:
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        sns.heatmap(
            df.select_dtypes(include=['float64', 'int64']).corr(),
            annot=True,
            cmap='coolwarm',
            fmt=".2f",
            ax=ax4
        )

        # Làm nghiêng nhãn trục Y 30 độ
        ax4.set_yticklabels(ax4.get_yticklabels(), rotation=360)

        st.pyplot(fig4)

    st.markdown("### 🔎 Nhận xét:")
    st.markdown("- `bmi` có tương quan cao nhất với `age` vì khi về già con người có su hướng tăng cân.")
    st.markdown("- `HbA1c_level` có tương quan cao thứ nhì với `blood_glucose_level` bởi vì số đo đường huyết liên quan trực tiếp đến mức đường huyết đang có trong máu")