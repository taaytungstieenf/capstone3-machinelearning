import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.linear_model import LogisticRegression

# Load dataset
df = pd.read_csv("diabetes_prediction_dataset.csv")

# Encode categorical variables
label_encoders = {}
categorical_cols = ['gender', 'smoking_history']
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Split features and target
X = df.drop(columns=['diabetes'])
y = df['diabetes']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Logistic Regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Evaluation
accuracy = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_pred_proba)
print(f'Accuracy: {accuracy:.4f}')
print(f'AUC: {auc:.4f}')

# Define a new person's data (replace values accordingly)
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

# Apply the same encoding as training data
for col in categorical_cols:
    new_person[col] = label_encoders[col].transform(new_person[col])

# Predict diabetes probability
prediction = model.predict(new_person)
probability = model.predict_proba(new_person)[:, 1]

print(f"Diabetes Prediction: {'Yes' if prediction[0] == 1 else 'No'}")
print(f"Probability: {probability[0]:.4f}")
