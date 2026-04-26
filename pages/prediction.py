import streamlit as st
import pandas as pd
import joblib
import os
from pages.database import insert_data
from utils.alert import check_and_alert
from utils.ui import header


# ---------------- EXPLANATION ----------------
def generate_explanation(data, final_risk):
    ph, turbidity, tds, coliform, rainfall, temperature = data

    issues = []

    if coliform > 50:
        issues.append(f"Bacterial contamination ({coliform:.2f} CFU)")
    elif coliform > 10:
        issues.append(f"Moderate bacterial presence ({coliform:.2f} CFU)")

    if ph < 6.5 or ph > 8.5:
        issues.append(f"Unsafe pH ({ph:.2f})")

    if turbidity > 10:
        issues.append(f"High turbidity ({turbidity:.2f} NTU)")

    if tds > 500:
        issues.append(f"High TDS ({tds:.2f} mg/L)")

    if not issues:
        issues.append("All parameters within acceptable limits")

    if final_risk == "High":
        actions = ["Do NOT consume water", "Immediate treatment required"]
    elif final_risk == "Medium":
        actions = ["Boil or filter water", "Monitor regularly"]
    else:
        actions = ["Safe for drinking"]

    return f"""
### 💧 Water Quality: **{final_risk}**

#### 🔍 Observations:
- """ + "\n- ".join(issues) + """

#### 📌 Actions:
- """ + "\n- ".join(actions)


# ---------------- MAIN ----------------
def run():
    header("🔮 Prediction")

    if not os.path.exists("model/rf_model.pkl"):
        st.error("Model not found")
        return

    model = joblib.load("model/rf_model.pkl")

    # ================= MANUAL =================
    st.subheader("🧪 Manual Input")

    community = st.text_input("Community Name", "Area_1")

    col1, col2 = st.columns(2)

    with col1:
        ph = st.slider("pH", 0.0, 14.0, 7.0)
        turbidity = st.slider("Turbidity", 0.0, 50.0, 2.0)
        tds = st.slider("TDS", 0.0, 1500.0, 200.0)

    with col2:
        coliform = st.slider("Coliform", 0.0, 200.0, 2.0)
        rainfall = st.slider("Rainfall", 0.0, 300.0, 40.0)
        temperature = st.slider("Temperature", 0.0, 50.0, 25.0)

    c1, c2 = st.columns(2)

    with c1:
        if st.button("🚀 Predict"):
            data = [ph, turbidity, tds, coliform, rainfall, temperature]

            # ---------- STRONG RULE SYSTEM ----------
            if coliform > 40 or turbidity > 15 or ph < 5 or ph > 9.5:
                final_risk = "High"

            elif (
                coliform <= 10 and
                turbidity <= 5 and
                6.5 <= ph <= 8.5 and
                tds <= 500
            ):
                final_risk = "Low"

            else:
                final_risk = "Medium"

            # ---------- OUTPUT ----------
            if final_risk == "High":
                st.error("🚨 High Risk")
            elif final_risk == "Medium":
                st.warning("⚠ Medium Risk")
            else:
                st.success("✅ Low Risk")

            st.markdown(generate_explanation(data, final_risk))

            insert_data(community, *data, final_risk)

            if final_risk == "High":
                check_and_alert(community, final_risk, data)

    with c2:
        if st.button("🔄 Reset Manual"):
            st.rerun()

    st.divider()

    # ================= CSV =================
    st.subheader("📂 Bulk CSV Prediction")

    file = st.file_uploader("Upload CSV", type=["csv"], key="csv")

    if file:
        df = pd.read_csv(file)

        required = ["pH", "Turbidity", "TDS", "Coliform", "Rainfall", "Temperature"]

        if not all(col in df.columns for col in required):
            st.error(f"CSV must contain: {required}")
            return

        st.dataframe(df)

        c3, c4 = st.columns(2)

        with c3:
            if st.button("⚡ Predict CSV"):

                results = []

                for _, row in df.iterrows():
                    data = [
                        row["pH"], row["Turbidity"], row["TDS"],
                        row["Coliform"], row["Rainfall"], row["Temperature"]
                    ]

                    if data[3] > 40 or data[1] > 15 or data[0] < 5 or data[0] > 9.5:
                        final_risk = "High"
                    elif (
                        data[3] <= 10 and data[1] <= 5 and
                        6.5 <= data[0] <= 8.5 and data[2] <= 500
                    ):
                        final_risk = "Low"
                    else:
                        final_risk = "Medium"

                    results.append(final_risk)

                    insert_data("CSV Upload", *data, final_risk)

                    if final_risk == "High":
                        check_and_alert("CSV Upload", final_risk, data)

                df["Predicted Risk"] = results

                st.success("✅ CSV Prediction Complete")
                st.dataframe(df)

                csv = df.to_csv(index=False).encode("utf-8")

                st.download_button(
                    "⬇ Download Results",
                    csv,
                    "predicted_results.csv",
                    "text/csv"
                )

        with c4:
            if st.button("🔄 Reset CSV"):
                st.session_state["csv"] = None
                st.rerun()