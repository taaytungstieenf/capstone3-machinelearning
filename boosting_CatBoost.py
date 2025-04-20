import pandas as pd
import numpy as np
from catboost import CatBoostClassifier, Pool
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, roc_auc_score
import matplotlib.pyplot as plt

# 1. Load dataset
df = pd.read_csv("xgb_diabetes_dataset.csv")

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

# 4. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5. Create Pool object for CatBoost (optional but helps with categorical features)
train_pool = Pool(X_train, y_train)
test_pool = Pool(X_test, y_test)

# 6. Train CatBoost model (silent=True to suppress verbose output)
model = CatBoostClassifier(verbose=0, random_state=42)
model.fit(train_pool)

# 7. Make predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# 8. Evaluation
accuracy = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_pred_proba)

print(f'Accuracy: {accuracy:.4f}')
print(f'AUC: {auc:.4f}')

# 9. Plot feature importance
feature_importance = model.get_feature_importance()
feature_names = X.columns

plt.figure(figsize=(10, 6))
plt.barh(feature_names, feature_importance)
plt.title("Feature Importance (CatBoost)")
plt.xlabel("Importance Score")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# 10. Predict for a new individual
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

# Encode new person's categorical data same as training
for col in categorical_cols:
    new_person[col] = label_encoders[col].transform(new_person[col])

# 11. Prediction for the new person
prediction = model.predict(new_person)
probability = model.predict_proba(new_person)[:, 1]

print(f"Diabetes Prediction: {'Yes' if prediction[0] == 1 else 'No'}")
print(f"Probability: {probability[0]:.4f}")

# 12. Show top features in order
sorted_idx = np.argsort(feature_importance)[::-1]
print("\nTop features influencing prediction:")
for idx in sorted_idx:
    print(f"{feature_names[idx]}: {feature_importance[idx]:.4f}")
