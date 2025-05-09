import pandas as pd
import numpy as np
import lightgbm as lgb  # THAY ĐỔI: Dùng LightGBM thay vì XGBoost
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, roc_auc_score
import matplotlib.pyplot as plt
import joblib
import os

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

# 5. Train model using LightGBM
model = lgb.LGBMClassifier()
model.fit(X_train, y_train)

# 6. Evaluation
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_pred_proba)

print(f'Accuracy: {accuracy:.4f}')
print(f'AUC: {auc:.4f}')

# 7. Feature importance plot
lgb.plot_importance(model, max_num_features=10)
plt.title("Feature Importance")
plt.tight_layout()
plt.show()

# 8. Save model and encoders
os.makedirs(os.path.join("..", "models"), exist_ok=True)

model_output_path = os.path.join("models", "lightgbm_model.pkl")
encoders_output_path = os.path.join("models", "lightgbm_label_encoders.pkl")

joblib.dump(model, model_output_path)
joblib.dump(label_encoders, encoders_output_path)

print(f"Model saved to: {model_output_path}")
print(f"Label encoders saved to: {encoders_output_path}")
