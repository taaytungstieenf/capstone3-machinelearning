"""
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score
import os

# 1. Load dataset
data_path = os.path.join("data", "diabetes_dataset.csv")
df = pd.read_csv(data_path)

# 2. Handle missing data
if df.isnull().sum().sum() > 0:
    print("Dữ liệu có giá trị thiếu, loại bỏ các dòng chứa NaN.")
    df = df.dropna()

# 3. Encode categorical features
label_encoders = {}
for col in ['gender', 'smoking_history']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# 4. Normalize numerical features
X = df.drop(columns=['diabetes'])
y = df['diabetes']

scaler = StandardScaler()
X[X.columns] = scaler.fit_transform(X)

# 5. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 6. Train XGBoost
model = xgb.XGBClassifier(eval_metric='logloss', use_label_encoder=False, random_state=42)
model.fit(X_train, y_train)

# 7. Evaluate
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("\n==== KẾT QUẢ ĐÁNH GIÁ ====")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("AUC Score:", roc_auc_score(y_test, y_proba))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# 8. Save models
model_output_path = os.path.join("models", "xgb_model.pkl")
joblib.dump(model, model_output_path)
"""
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, roc_auc_score
import matplotlib.pyplot as plt
import joblib
import os  # NEW: to create path

# 1. Load dataset
df = pd.read_csv("../data/diabetes_dataset.csv")

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

# 5. Train model
model = xgb.XGBClassifier(eval_metric='logloss')
model.fit(X_train, y_train)

# 6. Evaluation
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_pred_proba)

print(f'Accuracy: {accuracy:.4f}')
print(f'AUC: {auc:.4f}')

# 7. Feature importance plot
xgb.plot_importance(model)
plt.title("Feature Importance")
plt.tight_layout()
plt.show()

# 8. Save model and encoders (one level up to /models)
os.makedirs(os.path.join("..", "models"), exist_ok=True)

model_output_path = os.path.join("..", "models", "xgb_model.pkl")
encoders_output_path = os.path.join("..", "models", "label_encoders.pkl")

joblib.dump(model, model_output_path)
joblib.dump(label_encoders, encoders_output_path)

print(f"Model saved to: {model_output_path}")
print(f"Label encoders saved to: {encoders_output_path}")

