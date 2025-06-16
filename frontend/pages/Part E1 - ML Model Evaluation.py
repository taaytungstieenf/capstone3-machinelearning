import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Đường dẫn tới thư mục project root từ vị trí file hiện tại
project_root = Path(__file__).resolve().parents[2]
metrics_dir = project_root / 'boosting_models' / 'metrics'

# Đường dẫn cụ thể tới các file CSV
metric_files = [
    metrics_dir / "catboost_metrics.csv",
    metrics_dir / "xgboost_metrics.csv",
    metrics_dir / "lightgbm_metrics.csv"
]

# Đọc dữ liệu
all_metrics = pd.concat([pd.read_csv(file) for file in metric_files], ignore_index=True)
all_metrics.set_index("model", inplace=True)

st.set_page_config(page_title="Comparison", layout="wide", page_icon="⚕️")
st.markdown(
    """
    <h1 style='text-align: center;
               color: #2c3e50;
               font-size: 40px;
               font-family: "Trebuchet MS", sans-serif;
               text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);'>
        ⚖️ So Sánh Các Mô Hình Boosting
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

# --- Bố cục chia làm 2 cột ---
col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown("<h3 style='text-align: center; color: #21130d;'>📋 Chỉ Số Của Các Mô Hình</h3>", unsafe_allow_html=True)
    st.dataframe(all_metrics.style.format("{:.4f}"))

    metrics_to_plot = ["test_accuracy", "test_auc", "precision", "recall", "f1_score", "training_time"]
    selected_metric = st.selectbox("Chọn chỉ số để so sánh", metrics_to_plot, index=0)

    st.markdown(f"<h3 style='text-align: center;'>📊 Biểu đồ so sánh {selected_metric}</h3>", unsafe_allow_html=True)
    st.bar_chart(all_metrics[selected_metric])

with col2:
    chart_choice = st.sidebar.radio("",
        (
            "Chart 1 – Feature Importance",
            "Chart 2 – Confusion Matrix",
            "Chart 3 – Precision-Recall Curve",
            "Chart 4 – ROC Curve"
        )
    )

    if chart_choice == "Chart 1 – Feature Importance":
        st.markdown("<h3 style='text-align: center; color: #21130d;'>💡 Thuộc Tính Đặc Trưng</h3>", unsafe_allow_html=True)

        models = ["CatBoost", "XGBoost", "LightGBM"]
        model_to_filename = {
            "CatBoost": "catboost_feature_importance.png",
            "XGBoost": "xgboost_feature_importance.png",
            "LightGBM": "lightgbm_feature_importance.png"
        }

        selected_model = st.selectbox("Chọn mô hình", models, index=0)

        feature_plot_path = metrics_dir / model_to_filename[selected_model]
        if feature_plot_path.exists():
            st.image(str(feature_plot_path), caption=f"{selected_model} Feature Importance", use_container_width=True)
        else:
            st.warning(f"Không tìm thấy hình ảnh cho {selected_model}.")

    elif chart_choice == "Chart 2 – Confusion Matrix":
        st.markdown("<h3 style='text-align: center; color: #21130d;'>🔡 Ma Trận Nhầm Lẫn</h3>", unsafe_allow_html=True)

        models = ["CatBoost", "XGBoost", "LightGBM"]
        confusion_matrix_filenames = {
            "CatBoost": "catboost_confusion_matrix.png",
            "XGBoost": "xgboost_confusion_matrix.png",
            "LightGBM": "lightgbm_confusion_matrix.png"
        }

        selected_model_cm = st.selectbox("Chọn mô hình", models, index=0)
        cm_plot_path = metrics_dir / confusion_matrix_filenames[selected_model_cm]

        if cm_plot_path.exists():
            col1, col2 = st.columns([1, 15])
            with col2:
                st.image(str(cm_plot_path), caption=f"{selected_model_cm} Confusion Matrix", width=700)
        else:
            st.warning(f"Không tìm thấy confusion matrix cho {selected_model_cm}.")

    elif chart_choice == "Chart 3 – Precision-Recall Curve":
        st.markdown("<h3 style='text-align: center; color: #21130d;'>📉 Đường Cong Precision-Recall</h3>", unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(5.5, 4.0))

        model_files = {
            "CatBoost": "catboost_pr.npz",
            "XGBoost": "xgboost_pr.npz",
            "LightGBM": "lightgbm_pr.npz"
        }

        for model, file in model_files.items():
            path = metrics_dir / file
            if path.exists():
                data = np.load(path)
                precision = data['precision']
                recall = data['recall']
                auc_val = data['auc']
                ax.plot(recall, precision, label=f"{model} (Pre-Recall = {auc_val:.3f})", linewidth=1.4)

        ax.set_xlabel("Recall", fontsize=10)
        ax.set_ylabel("Precision", fontsize=10)
        for spine in ax.spines.values():
            spine.set_linewidth(0.8)
        ax.grid(True, linestyle="--", alpha=0.3)
        ax.legend(loc="lower left", fontsize=7, framealpha=1.0)

        plt.tight_layout()
        st.pyplot(fig)

    elif chart_choice == "Chart 4 – ROC Curve":
        st.markdown("<h3 style='text-align: center; color: #21130d;'>📈 Đường Cong ROC</h3>", unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(5.5, 4.0))

        model_files = {
            "CatBoost": "catboost_roc.npz",
            "XGBoost": "xgboost_roc.npz",
            "LightGBM": "lightgbm_roc.npz"
        }

        for model, file in model_files.items():
            path = metrics_dir / file
            if path.exists():
                data = np.load(path)
                fpr = data['fpr']
                tpr = data['tpr']
                auc_val = data['auc']
                ax.plot(fpr, tpr, label=f"{model} (AUC = {auc_val:.3f})", linewidth=1.4)

        ax.plot([0, 1], [0, 1], 'k--', linewidth=1.2, label='Random Guess')
        ax.set_xlabel("False Positive Rate", fontsize=10)
        ax.set_ylabel("True Positive Rate", fontsize=10)
        for spine in ax.spines.values():
            spine.set_linewidth(0.8)
        ax.grid(True, linestyle="--", alpha=0.3)
        ax.legend(loc="lower right", fontsize=7, framealpha=1.0)

        plt.tight_layout()
        st.pyplot(fig)
