import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# ---------- FIX PATH ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "data", "water_quality.csv")

# ---------- LOAD DATA ----------
df = pd.read_csv(file_path)

# ---------- FEATURES ----------
X = df[["pH","Turbidity","TDS","Coliform","Rainfall","Temperature"]]
y = df["Risk"]

# ---------- ENCODE ----------
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# ---------- SPLIT ----------
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2)

# ---------- MODEL ----------
model = RandomForestClassifier()
model.fit(X_train, y_train)

# ---------- SAVE ----------
os.makedirs("model", exist_ok=True)

joblib.dump(model, os.path.join(BASE_DIR, "model", "rf_model.pkl"))
joblib.dump(le, os.path.join(BASE_DIR, "model", "label_encoder.pkl"))

print("✅ Model trained successfully!")