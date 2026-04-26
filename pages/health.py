import streamlit as st
import pandas as pd
from pages.database import fetch_data


def run():
    st.title("🏥 Health Analysis")

    # ================= LOAD WATER DATA =================
    data = fetch_data()

    if not data:
        st.warning("No water data available")
        return

    # Proper mapping from DB
    water_df = pd.DataFrame(data, columns=[
        "id", "community", "ph", "turbidity", "tds",
        "coliform", "rainfall", "temperature", "risk", "timestamp"
    ])

    water_df.columns = water_df.columns.str.lower().str.strip()
    water_df["community"] = water_df["community"].astype(str).str.lower().str.strip()

    # ================= CSV UPLOAD =================
    st.subheader("📂 Upload Health CSV")

    file = st.file_uploader("Upload health data CSV", type=["csv"])

    if file:
        health_df = pd.read_csv(file)
        health_df.columns = health_df.columns.str.lower().str.strip()

        # Required columns
        required = ["community", "disease_cases", "hospital_visits"]

        if not all(col in health_df.columns for col in required):
            st.error("CSV must contain: community, disease_cases, hospital_visits")
            st.write("Found:", list(health_df.columns))
            return

        health_df["community"] = health_df["community"].astype(str).str.lower().str.strip()

        st.success("✅ Using uploaded health data")

    else:
        st.warning("using simulated health data")

        # Generate health data from risk
        risk_cases = {"Low": 5, "Medium": 25, "High": 80}

        health_df = water_df[["community", "risk"]].copy()
        health_df["disease_cases"] = health_df["risk"].map(risk_cases)
        health_df["hospital_visits"] = health_df["disease_cases"] * 2

    # ================= MERGE =================
    df = pd.merge(
        water_df,
        health_df,
        on="community",
        how="inner"
    )

    if df.empty:
        st.error("❌ No matching communities between water and health data")
        return

    # ================= SAFE RISK =================
    if "risk" not in df.columns:
        # handle renamed columns
        for col in df.columns:
            if "risk" in col:
                df["risk"] = df[col]
                break

    # ================= FINAL COMPUTATION =================
    df["cases"] = df["disease_cases"] + df["hospital_visits"]

    # ================= INSIGHTS =================
    st.markdown("### 🧠 Key Insights")

    st.write(f"Average disease cases: {round(df['cases'].mean(), 2)}")
    st.write(f"Highest affected community: {df.loc[df['cases'].idxmax(), 'community']}")
    st.write(f"Highest recorded cases: {df['cases'].max()}")

    if "tds" in df.columns:
        corr = df["tds"].corr(df["cases"])
    else:
        corr = 0

    st.write(f"Correlation score: {round(corr, 2)}")

    if corr < 0.3:
        st.info("Weak correlation → water quality alone not sufficient")
    else:
        st.success("Strong correlation → water quality impacts health")

    st.divider()

    # ================= CLEAN TABLE =================
    st.markdown("### 🔗 Combined Data")

    # remove duplicate columns
    cols_to_show = [col for col in df.columns if not col.endswith("_y")]
    st.dataframe(df[cols_to_show], use_container_width=True)

    st.divider()

    # ================= CHART =================
    st.markdown("### 📊 Disease vs Water Risk")

    chart_df = df.groupby("community")["cases"].sum().reset_index()
    st.bar_chart(chart_df.set_index("community"))

    st.divider()

    # ================= ALERTS =================
    st.markdown("### 🚨 Health Alerts")

    for _, row in chart_df.iterrows():
        if row["cases"] > 100:
            st.error(f"🚨 Outbreak risk in {row['community']}")
        elif row["cases"] > 50:
            st.warning(f"⚠ High risk water in {row['community']}")
        else:
            st.success(f"✅ Stable in {row['community']}")