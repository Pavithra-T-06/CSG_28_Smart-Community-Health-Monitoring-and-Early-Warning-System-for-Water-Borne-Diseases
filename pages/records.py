import streamlit as st
import pandas as pd
from pages.database import (
    fetch_data,
    clear_data,
    delete_record,
    delete_by_community,
    delete_filtered
)


def run():
    st.title("📊 Records")

    data = fetch_data()

    if not data:
        st.warning("No records available")
        return

    df = pd.DataFrame(data, columns=[
        "id", "community", "ph", "turbidity", "tds",
        "coliform", "rainfall", "temperature", "risk", "timestamp"
    ])

    # =========================================================
    # FILTERS
    # =========================================================
    st.markdown("### 🔍 Filters")

    col1, col2 = st.columns(2)

    with col1:
        community_filter = st.selectbox(
            "Community",
            ["All"] + sorted(df["community"].unique())
        )

    with col2:
        risk_filter = st.selectbox(
            "Risk",
            ["All"] + sorted(df["risk"].unique())
        )

    filtered_df = df.copy()

    if community_filter != "All":
        filtered_df = filtered_df[filtered_df["community"] == community_filter]

    if risk_filter != "All":
        filtered_df = filtered_df[filtered_df["risk"] == risk_filter]

    st.dataframe(filtered_df, use_container_width=True)

    # =========================================================
    # ADVANCED DELETE
    # =========================================================
    st.markdown("### 🗑 Delete Controls")

    delete_mode = st.selectbox(
        "Choose delete option",
        [
            "Delete Single Record",
            "Delete by Community",
            "Delete Filtered Data",
            "Delete All Data"
        ]
    )

    # ---------------- SINGLE DELETE ----------------
    if delete_mode == "Delete Single Record":

        options = {
            f"{row['community']} | {row['risk']} | {row['timestamp']}": row["id"]
            for _, row in filtered_df.iterrows()
        }

        if options:
            selected = st.selectbox("Select record", list(options.keys()))

            if st.button("❌ Delete Selected"):
                delete_record(options[selected])
                st.success("Deleted")
                st.rerun()

    # ---------------- COMMUNITY DELETE ----------------
    elif delete_mode == "Delete by Community":

        communities = df["community"].unique()

        selected = st.selectbox("Select community", communities)

        if st.button("⚠ Delete Community Data"):
            delete_by_community(selected)
            st.success(f"Deleted all records for {selected}")
            st.rerun()

    # ---------------- FILTER DELETE ----------------
    elif delete_mode == "Delete Filtered Data":

        if st.button("⚠ Delete Filtered Records"):
            ids = filtered_df["id"].tolist()
            delete_filtered(ids)
            st.success("Filtered records deleted")
            st.rerun()

    # ---------------- DELETE ALL ----------------
    elif delete_mode == "Delete All Data":

        confirm = st.checkbox("I confirm deletion of ALL data")

        if confirm and st.button("🔥 Delete Everything"):
            clear_data()
            st.success("All data deleted")
            st.rerun()

    # =========================================================
    # DOWNLOAD
    # =========================================================
    st.markdown("### ⬇ Download")

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Filtered Data",
        csv,
        "records.csv",
        "text/csv"
    )