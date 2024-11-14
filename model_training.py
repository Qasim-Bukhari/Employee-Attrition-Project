# model_training.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
import joblib

# Load the dataset
df = pd.read_csv("C:/University Material/Data Mining/Employee Attrition Project/employee_attrition_dataset.csv")

# Select relevant columns
selected_columns = [
    "Age", "JobSatisfaction", "YearsAtCompany", "JobLevel", "MonthlyIncome",
    "TotalWorkingYears", "YearsSinceLastPromotion", "OverTime", "Attrition"
]
df = df[selected_columns]

# Encode categorical columns
le_overtime = LabelEncoder()
df['OverTime'] = le_overtime.fit_transform(df['OverTime'])

le_attrition = LabelEncoder()
df['Attrition'] = le_attrition.fit_transform(df['Attrition'])

# Split the data into features and target
X = df.drop("Attrition", axis=1)
y = df["Attrition"]

# Apply SMOTE to balance the classes
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Standardize the features
scaler = StandardScaler()
X_resampled = scaler.fit_transform(X_resampled)
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Try RandomForest for improved handling of imbalance
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=["No Attrition", "Attrition"]))

feature_importance = model.feature_importances_

# Save the model, scaler, encoders, and feature importance
joblib.dump(model, "model.joblib")
joblib.dump(scaler, "scaler.joblib")
joblib.dump(le_overtime, "le_overtime.joblib")
joblib.dump(le_attrition, "le_attrition.joblib")
joblib.dump(feature_importance, "feature_importance.joblib")

print("Model, scaler, and encoders saved successfully with SMOTE and balanced class weight.")
