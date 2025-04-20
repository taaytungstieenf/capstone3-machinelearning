import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, roc_auc_score
import matplotlib.pyplot as plt

# 1. Load dataset
df = pd.read_csv("xgb_dataset.csv")

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

# 7. Evaluate performance
accuracy = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_pred_proba)

print(f'Accuracy: {accuracy:.4f}')
print(f'AUC: {auc:.4f}')

# 8. Plot feature importance
xgb.plot_importance(model)
plt.title("Feature Importance")
plt.tight_layout()
plt.show()

# 9. Predict for a new individual
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

# Encode categorical columns for new input
for col in categorical_cols:
    new_person[col] = label_encoders[col].transform(new_person[col])

# 10. Predict diabetes status for new person
prediction = model.predict(new_person)
probability = model.predict_proba(new_person)[:, 1]

print(f"Diabetes Prediction: {'Yes' if prediction[0] == 1 else 'No'}")
print(f"Probability: {probability[0]:.4f}")

# 11. Optional: show sorted feature importance scores
importances = model.feature_importances_
feature_names = X.columns
indices = np.argsort(importances)[::-1]

print("\nTop features influencing prediction:")
for i in indices:
    print(f"{feature_names[i]}: {importances[i]:.4f}")
