import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, roc_auc_score
import matplotlib.pyplot as plt

# 1. Load dataset
df = pd.read_csv("diabetes_dataset.csv")

# 2. Encode categorical variables (e.g., 'Male', 'Female' → 0,1)
label_encoders = {}
categorical_cols = ['gender', 'smoking_history']
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# 3. Split features and target label
X = df.drop(columns=['diabetes'])
y = df['diabetes']

# 4. Split into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5. Train XGBoost model
model = xgb.XGBClassifier(eval_metric='logloss')  # Removed deprecated 'use_label_encoder'
model.fit(X_train, y_train)

# 6. Make predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]  # Probabilities for AUC
