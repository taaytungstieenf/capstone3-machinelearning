import numpy as np
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="EDA", layout="wide", page_icon="⚕️",)
st.markdown("<h1 style='text-align: center; color: #21130d;'>Mô Tả Thống Kê Tập Dữ Liệu</h1>", unsafe_allow_html=True)

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
    }
    </style>
    <div class="footer">
        © 2025 Nguyễn Đức Tây | All rights reserved.
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader("", type="csv")

# Kiểm tra tình trạng file đã được tải lên chưa
if uploaded_file is not None:
    st.session_state.uploaded_file = uploaded_file # Rồi thì lưu trữ file
    st.session_state.df = pd.read_csv(uploaded_file)
else:
    if "df" not in st.session_state or st.session_state.df is None:
        st.info("⏳ Vui lòng tải lên tệp CSV.") # Chưa thì gởi message
        st.stop()

df = st.session_state.df # Lấy DataFrame từ session_state để vẽ các sơ đồ bên dưới

# Tạo menu chọn sơ đồ trong sidebar
chart_choice = st.sidebar.radio("",
    (
        "Histogram - Distribution",
        "Boxplot - Outliers by Category",
        "Countplot - Categorical Frequency",
        "Correlation Heatmap",
        "Diabetes Rate by Group (Barplot)",
        "Pairplot - Feature Relationships"
    )
)

col1, col2, col3 = st.columns([1.5, 2.75, 1.5])

# Hiển thị sơ đồ dựa trên lựa chọn của người dùng
if chart_choice == "Histogram - Distribution":
    with col2:
        num_col1 = st.selectbox(
            "Thống Kê Trên Từng Thuộc Tính",
            df.select_dtypes(include=['float64', 'int64', 'object']).columns,
            key="hist"
        )

        fig1, ax1 = plt.subplots()

        # Nếu là cột số
        if pd.api.types.is_numeric_dtype(df[num_col1]):
            data = df[num_col1].dropna()
            min_val, max_val = data.min(), data.max()

            # Vẽ histogram
            bins = 50
            sns.histplot(data, kde=True, bins=bins, ax=ax1)

            # Trục X chi tiết
            tick_interval_x = (max_val - min_val) / 10
            ax1.set_xticks(np.arange(min_val, max_val + tick_interval_x, tick_interval_x))

            # Trục Y chi tiết với số chẵn
            y_max = ax1.get_ylim()[1]
            raw_interval = y_max / 10
            tick_interval_y = max(1, round(raw_interval))
            if tick_interval_y % 2 != 0:
                tick_interval_y += 1
            ax1.set_yticks(np.arange(0, y_max + tick_interval_y, tick_interval_y))

            # Thiết lập tiêu đề và nhãn
            ax1.set_xlabel(num_col1)
            ax1.set_ylabel("Số lượng")
            ax1.set_title(f"Phân phối: {num_col1}")
            ax1.tick_params(axis='x', rotation=45)

        # Nếu là cột phân loại
        else:
            sns.countplot(x=num_col1, data=df, ax=ax1, order=df[num_col1].value_counts().index)

            # Trục Y chi tiết với số chẵn
            y_max = df[num_col1].value_counts().max()
            raw_interval = y_max / 10
            tick_interval_y = max(1, round(raw_interval))
            if tick_interval_y % 2 != 0:
                tick_interval_y += 1
            ax1.set_yticks(np.arange(0, y_max + tick_interval_y, tick_interval_y))

            # Thiết lập tiêu đề và nhãn

            #ax1.set_title(f"Tần suất phân loại: {num_col1}")
            ax1.tick_params(axis='x', rotation=30)

        # Hiển thị biểu đồ
        st.pyplot(fig1)

elif chart_choice == "Boxplot - Outliers by Category":
    with col2:
        cat_col1 = st.selectbox("Chọn cột phân loại (Boxplot)", df.select_dtypes(include='object').columns,
                                key="box_cat")
        num_col2 = st.selectbox("Chọn cột số (Boxplot)", df.select_dtypes(include=['float64', 'int64']).columns,
                                key="box_num")

        # Loại bỏ giá trị thiếu để tránh lỗi
        plot_df = df[[cat_col1, num_col2]].dropna()

        # Tạo biểu đồ
        fig2, ax2 = plt.subplots(figsize=(10, 6))  # Có thể tăng kích thước nếu nhiều nhãn

        sns.boxplot(data=plot_df, x=cat_col1, y=num_col2, ax=ax2)

        # Xoay nhãn trục X để dễ đọc
        ax2.tick_params(axis='x', rotation=45)

        # Thiết lập chia trục Y theo số chẵn
        y_min, y_max = plot_df[num_col2].min(), plot_df[num_col2].max()
        tick_interval_y = max(1, round((y_max - y_min) / 10))
        if tick_interval_y % 2 != 0:
            tick_interval_y += 1
        ax2.set_yticks(np.arange(y_min, y_max + tick_interval_y, tick_interval_y))

        # Thiết lập nhãn và tiêu đề
        ax2.set_xlabel(cat_col1)
        ax2.set_ylabel(num_col2)
        ax2.set_title(f"Boxplot: {num_col2} theo nhóm {cat_col1}")

        # Hiển thị
        st.pyplot(fig2)

elif chart_choice == "Countplot - Categorical Frequency":
    with col2:
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
