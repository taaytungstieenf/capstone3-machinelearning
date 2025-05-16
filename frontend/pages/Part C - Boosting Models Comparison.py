import streamlit as st
import pandas as pd
import os

# Đường dẫn đến thư mục metrics từ file hiện tại
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
metrics_dir = os.path.join(base_dir, 'boosting_models', 'metrics')

# Đường dẫn cụ thể tới các file CSV
metric_files = [
    os.path.join(metrics_dir, "catboost_metrics.csv"),
    os.path.join(metrics_dir, "xgboost_metrics.csv"),
    os.path.join(metrics_dir, "lightgbm_metrics.csv")
]

# Đọc dữ liệu
all_metrics = pd.concat([pd.read_csv(file) for file in metric_files], ignore_index=True)
all_metrics.set_index("model", inplace=True)

st.set_page_config(page_title="EDA", layout="wide", page_icon="⚕️",)
st.markdown("<h1 style='text-align: center; color: #21130d;'>So Sánh Các Mô Hình Boosting</h1>", unsafe_allow_html=True)

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

# --- Bố cục chia làm 2 cột ---
col1, col2 = st.columns([1, 1.5])  # tỉ lệ 2:1 giữa bảng và hình ảnh

# --- CỘT 1: Bảng và bar chart ---
with col1:
    st.markdown("<h3 style='text-align: center; color: #21130d;'>📋 Chỉ Số Của Các Mô Hình</h3>",unsafe_allow_html=True)
    st.dataframe(all_metrics.style.format("{:.4f}"))

    metrics_to_plot = ["accuracy", "auc", "precision", "recall", "f1_score", "training_time"]
    selected_metric = st.selectbox("📈 Chọn chỉ số để so sánh", metrics_to_plot, index=0)

    st.markdown(f"<h3 style='text-align: center;'>📊 Biểu đồ so sánh {selected_metric.capitalize()}</h3>", unsafe_allow_html=True)

    st.bar_chart(all_metrics[selected_metric])

# --- CỘT 2: Feature Importance ---
with col2:
    st.markdown("<h3 style='text-align: center; color: #21130d;'>🧠 Feature Importance</h3>", unsafe_allow_html=True)

    models = ["CatBoost", "XGBoost", "LightGBM"]
    model_to_filename = {
        "CatBoost": "catboost_feature_importance.png",
        "XGBoost": "xgboost_feature_importance.png",
        "LightGBM": "lightgbm_feature_importance.png"
    }

    selected_model = st.selectbox("Chọn mô hình", models, index=0)

    feature_plot_path = os.path.join(metrics_dir, model_to_filename[selected_model])
    if os.path.exists(feature_plot_path):
        st.image(feature_plot_path, caption=f"{selected_model} Feature Importance", use_container_width=True)
    else:
        st.warning(f"Không tìm thấy hình ảnh cho {selected_model}.")
