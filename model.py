import os
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight

MODEL_PATH = "model/rf_model.pkl"


# ---------------- LOAD OR TRAIN ----------------
def load_or_train_model():
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        return model, None
    else:
        return train_model()


# ---------------- TRAIN MODEL ----------------
def train_model():
    np.random.seed(42)
    size = 1000

    # -------- Synthetic realistic data --------
    data = pd.DataFrame({
        "ph": np.random.uniform(4, 9, size),
        "turbidity": np.random.uniform(0, 20, size),
        "tds": np.random.uniform(100, 1000, size),
        "coliform": np.random.uniform(0, 100, size),
        "rainfall": np.random.uniform(0, 200, size),
        "temperature": np.random.uniform(10, 40, size)
    })

    # -------- Improved risk logic --------
    def assign_risk(row):
        score = 0

        if row["coliform"] > 50:
            score += 3
        elif row["coliform"] > 10:
            score += 2

        if row["ph"] < 6 or row["ph"] > 9:
            score += 2

        if row["turbidity"] > 10:
            score += 2

        if row["tds"] > 500:
            score += 1

        if score >= 4:
            return "High"
        elif score >= 2:
            return "Medium"
        else:
            return "Low"

    data["risk"] = data.apply(assign_risk, axis=1)

    features = ["ph", "turbidity", "tds", "coliform", "rainfall", "temperature"]
    X = data[features]
    y = data["risk"]

    # -------- Class balancing --------
    classes = np.unique(y)
    weights = compute_class_weight("balanced", classes=classes, y=y)
    class_weights = dict(zip(classes, weights))

    # -------- Train/Test --------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # -------- Tuned model --------
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        class_weight=class_weights,
        random_state=42
    )

    model.fit(X_train, y_train)

    joblib.dump(model, MODEL_PATH)

    return model, None


# ---------------- PREDICT ----------------
def predict(model, data):
    features = np.array(data).reshape(1, -1)

    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]

    confidence = max(probabilities)

    return prediction, confidence