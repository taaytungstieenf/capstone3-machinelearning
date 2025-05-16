import pandas as pd
import numpy as np
from catboost import CatBoostClassifier, Pool  # THAY ĐỔI: Dùng CatBoost
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import joblib
import os
import time

# 1. Load dataset
df = pd.read_csv("../diabetes_dataset.csv")

# 2. Encode categorical variables
label_encoders = {}
categorical_cols = ['gender', 'smoking_history']

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# 3. Split features and target
X = df.drop(columns=['diabetes'])
y = df['diabetes']

# 4. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5. Train model using CatBoost
model = CatBoostClassifier(verbose=0)  # silent training

start_time = time.time()
model.fit(X_train, y_train)
end_time = time.time()

training_time = end_time - start_time
print(f'Training Time: {training_time:.4f}')

# 6. Evaluation
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_pred_proba)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f'Accuracy: {accuracy:.4f}')
print(f'AUC: {auc:.4f}')
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-score:  {f1:.4f}")

# 7. Feature importance plot
feature_importances = model.get_feature_importance()
feature_names = X.columns

plt.figure(figsize=(10, 6))
plt.barh(feature_names, feature_importances)
plt.xlabel("Importance")
plt.title("Feature Importance")
plt.tight_layout()
#plt.show()

# Lưu biểu đồ
feature_plot_path = os.path.join("metrics", "catboost_feature_importance.png")
plt.savefig(feature_plot_path)
plt.close()

print(f"Feature importance plot saved to: {feature_plot_path}")

# 8. Save model and encoders
os.makedirs(os.path.join("..", "models"), exist_ok=True)

model_output_path = os.path.join("models", "catboost_model.cbm")
encoders_output_path = os.path.join("models", "catboost_label_encoders.pkl")

model.save_model(model_output_path)
joblib.dump(label_encoders, encoders_output_path)

print(f"Model saved to: {model_output_path}")
print(f"Label encoders saved to: {encoders_output_path}")

# 9. Save evaluation metrics to CSV
metrics_df = pd.DataFrame([{
    "model": "CatBoost",
    "accuracy": accuracy,
    "auc": auc,
    "precision": precision,
    "recall": recall,
    "f1_score": f1,
    "training_time": training_time
}])

metrics_output_path = os.path.join("metrics", "catboost_metrics.csv")
metrics_df.to_csv(metrics_output_path, index=False)

print(f"Evaluation metrics saved to: {metrics_output_path}")