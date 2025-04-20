import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score

# 1. Load dataset
df = pd.read_csv("xgb_dataset.csv")

# 2. Kiểm tra và xử lý dữ liệu thiếu (nếu có)
if df.isnull().sum().sum() > 0:
    print("Dữ liệu có giá trị thiếu, tiến hành loại bỏ các dòng chứa NaN.")
    df = df.dropna()  # hoặc bạn có thể điền giá trị trung bình/median tuỳ trường hợp

# 3. Encode biến phân loại (e.g., 'Male', 'Female' → 0,1)
label_encoders = {}
categorical_cols = ['gender', 'smoking_history']
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le  # lưu để sử dụng khi xử lý dữ liệu mới

# 4. Chuẩn hóa các biến số để mô hình học ổn định hơn
X = df.drop(columns=['diabetes'])
y = df['diabetes']

numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns
scaler = StandardScaler()
X[numerical_cols] = scaler.fit_transform(X[numerical_cols])

# 5. Chia tập dữ liệu thành train/test (80% - 20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 6. Huấn luyện mô hình XGBoost
model = xgb.XGBClassifier(eval_metric='logloss', use_label_encoder=False, random_state=42)
model.fit(X_train, y_train)

# 7. Dự đoán trên tập kiểm tra
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]  # xác suất dự đoán dương tính tiểu đường

# 8. Đánh giá mô hình
print("\n==== KẾT QUẢ ĐÁNH GIÁ ====")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("AUC Score:", roc_auc_score(y_test, y_pred_proba))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))


import joblib
joblib.dump(model, "xgb_diabetes_model.pkl")
