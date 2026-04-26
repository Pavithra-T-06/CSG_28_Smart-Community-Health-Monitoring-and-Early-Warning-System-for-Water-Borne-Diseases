import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix


# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/Indian_water_data.csv")
df.columns = df.columns.str.strip().str.lower()

print("\n📊 Columns:", df.columns)


# ---------------- FEATURE ENGINEERING ----------------

# pH (average)
df["ph"] = (
    pd.to_numeric(df["ph - min"], errors="coerce") +
    pd.to_numeric(df["ph - max"], errors="coerce")
) / 2

# Temperature
df["temperature"] = (
    pd.to_numeric(df["temperature (c) - min"], errors="coerce") +
    pd.to_numeric(df["temperature (c) - max"], errors="coerce")
) / 2

# Coliform
df["coliform"] = (
    pd.to_numeric(df["total coliform (mpn/100ml) - min"], errors="coerce") +
    pd.to_numeric(df["total coliform (mpn/100ml) - max"], errors="coerce")
) / 2


# ---------------- HANDLE MISSING FEATURES ----------------
df["turbidity"] = 5
df["tds"] = 400
df["rainfall"] = 50


# ---------------- CLEAN ----------------
df = df.dropna(subset=["ph", "temperature", "coliform"])
print("\n✅ Cleaned rows:", len(df))


# ---------------- IMPROVED LABEL ----------------
def assign_risk(row):
    if row["coliform"] > 100 or row["ph"] < 5.5 or row["ph"] > 9.5:
        return "High"
    elif row["coliform"] > 20 or row["ph"] < 6.5 or row["ph"] > 8.5:
        return "Medium"
    else:
        return "Low"


df["risk"] = df.apply(assign_risk, axis=1)

print("\n📊 Class Distribution:")
print(df["risk"].value_counts())


# ---------------- FEATURES ----------------
features = ["ph", "turbidity", "tds", "coliform", "rainfall", "temperature"]

X = df[features]
y = df["risk"]


# ---------------- TRAIN (STRATIFIED + BALANCED) ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=150,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)


# ---------------- EVALUATE ----------------
y_pred = model.predict(X_test)

print("\n🔥 MODEL RESULTS")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))


# ---------------- CONFUSION MATRIX (SAVE IMAGE) ----------------
cm = confusion_matrix(y_test, y_pred)

plt.figure()
plt.imshow(cm)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

for i in range(len(cm)):
    for j in range(len(cm)):
        plt.text(j, i, cm[i, j], ha='center', va='center')

plt.savefig("confusion_matrix.png")
plt.close()

print("📊 Confusion matrix saved as image")


# ---------------- SAVE MODEL ----------------
joblib.dump(model, "model/rf_model.pkl")

print("\n✅ Model trained on real dataset and saved!")