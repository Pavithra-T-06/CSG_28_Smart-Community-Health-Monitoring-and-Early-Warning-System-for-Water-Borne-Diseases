import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import joblib
import pandas as pd
import os

from sklearn.metrics import (
    confusion_matrix,
    roc_curve,
    auc,
    classification_report
)
from sklearn.preprocessing import label_binarize
from sklearn.model_selection import train_test_split, cross_val_score


# ---------------- DEBUG: SHOW SAVE LOCATION ----------------
print("📂 Files will be saved in:", os.getcwd())


# ---------------- LOAD MODEL ----------------
model = joblib.load("model/rf_model.pkl")


# ---------------- GENERATE REALISTIC DATA ----------------
np.random.seed(42)
size = 1000

data = pd.DataFrame({
    "ph": np.clip(np.random.normal(7, 1, size), 3, 10),
    "turbidity": np.clip(np.random.exponential(3, size), 0, 30),
    "tds": np.clip(np.random.normal(300, 150, size), 50, 1200),
    "coliform": np.clip(np.random.exponential(20, size), 0, 150),
    "rainfall": np.random.uniform(10, 200, size),
    "temperature": np.random.uniform(20, 35, size)
})


# ---------------- RISK LABEL FUNCTION ----------------
def assign_risk(row):
    if (
        row["coliform"] > 40 or
        row["turbidity"] > 15 or
        row["ph"] < 5 or row["ph"] > 9.5
    ):
        return "High"
    elif (
        row["coliform"] > 10 or
        row["turbidity"] > 5 or
        row["ph"] < 6.5 or row["ph"] > 8.5 or
        row["tds"] > 500
    ):
        return "Medium"
    else:
        return "Low"


data["risk"] = data.apply(assign_risk, axis=1)

features = ["ph", "turbidity", "tds", "coliform", "rainfall", "temperature"]

X = data[features]
y = data["risk"]


# ---------------- TRAIN TEST SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


# ---------------- PREDICTIONS ----------------
y_pred = model.predict(X_test)


# =========================================================
# 📊 CONFUSION MATRIX
# =========================================================
cm = confusion_matrix(y_test, y_pred, labels=model.classes_)

plt.figure()
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    xticklabels=model.classes_,
    yticklabels=model.classes_
)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.savefig("confusion_matrix.png")
plt.close()


# =========================================================
# 📉 ROC CURVE
# =========================================================
classes = model.classes_

y_test_bin = label_binarize(y_test, classes=classes)
y_score = model.predict_proba(X_test)

plt.figure()

for i, class_name in enumerate(classes):
    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_score[:, i])
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f"{class_name} (AUC={roc_auc:.2f})")

plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.savefig("roc_curve.png")
plt.close()


# =========================================================
# 📊 FEATURE IMPORTANCE
# =========================================================
importances = model.feature_importances_

plt.figure()
plt.bar(features, importances)
plt.title("Feature Importance")
plt.xticks(rotation=45)
plt.savefig("feature_importance.png")
plt.close()


# =========================================================
# 📈 CROSS VALIDATION
# =========================================================
scores = cross_val_score(model, X, y, cv=5)

plt.figure()
plt.plot(scores, marker="o")
plt.title("Cross Validation Scores")
plt.xlabel("Fold")
plt.ylabel("Accuracy")
plt.savefig("cross_validation.png")
plt.close()


# =========================================================
# 📋 CLASSIFICATION REPORT (FIXED)
# =========================================================
report = classification_report(y_test, y_pred)

# PRINT (so you SEE it)
print("\n📊 Classification Report:\n")
print(report)

# SAVE TXT
with open("classification_report.txt", "w") as f:
    f.write(report)

# SAVE CSV (better for report)
report_dict = classification_report(y_test, y_pred, output_dict=True)
report_df = pd.DataFrame(report_dict).transpose()
report_df.to_csv("classification_report.csv")

print("\n✅ classification_report.txt saved")
print("✅ classification_report.csv saved")


# =========================================================
print("\n🎯 ALL METRICS GENERATED SUCCESSFULLY")