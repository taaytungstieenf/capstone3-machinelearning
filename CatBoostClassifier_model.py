import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score

# Load dataset
df = pd.read_csv("diabetes_prediction_dataset.csv")

# Xác định cột phân loại (CatBoost xử lý trực tiếp mà không cần encode tay)
categorical_cols = ['gender', 'smoking_history']

# Split features and target
X = df.drop(columns=['diabetes'])
y = df['diabetes']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train CatBoost model (ẩn log để không bị spam khi train)
model = CatBoostClassifier(verbose=0)
model.fit(X_train, y_train, cat_features=categorical_cols)

# Predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Evaluation
accuracy = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_pred_proba)
print(f'Accuracy: {accuracy:.4f}')
print(f'AUC: {auc:.4f}')

# Predict for a new person
new_person = pd.DataFrame([{
    'gender': 'Male',
    'age': 45,
    'hypertension': 1,
    'heart_disease': 0,
    'smoking_history': 'current',
    'bmi': 28.5,
    'HbA1c_level': 6.2,
    'blood_glucose_level': 130
}])

# Predict diabetes probability
prediction = model.predict(new_person)
probability = model.predict_proba(new_person)[:, 1]

print(f"Diabetes Prediction: {'Yes' if prediction[0] == 1 else 'No'}")
print(f"Probability: {probability[0]:.4f}")
