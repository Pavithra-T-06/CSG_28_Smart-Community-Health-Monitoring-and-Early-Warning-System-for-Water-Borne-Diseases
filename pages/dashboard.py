import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pages.database import fetch_data


def run():
    st.title("📊 Dashboard")
    st.caption("Overview of water quality data")

    data = fetch_data()

    if not data:
        st.warning("No data available")
        return

    # ---------------- DATAFRAME ----------------
    df = pd.DataFrame(data, columns=[
        "id","community","ph","turbidity","tds",
        "coliform","rainfall","temperature","risk","timestamp"
    ])

    # ---------------- METRICS ----------------
    st.subheader("Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Records", len(df))
    c2.metric("High Risk", len(df[df["risk"] == "High"]))
    c3.metric("Medium Risk", len(df[df["risk"] == "Medium"]))
    c4.metric("Low Risk", len(df[df["risk"] == "Low"]))

    st.divider()

    # ---------------- CHARTS ----------------
    col1, col2 = st.columns(2)

    # ========= RISK DISTRIBUTION =========
    with col1:
        st.subheader("Risk Distribution")

        risk_counts = df["risk"].value_counts().reset_index()
        risk_counts.columns = ["Risk", "Count"]

        color_map = {
            "Low": "#22c55e",     # green
            "Medium": "#f59e0b",  # yellow
            "High": "#ef4444"     # red
        }

        fig_bar = px.bar(
            risk_counts,
            x="Risk",
            y="Count",
            color="Risk",
            color_discrete_map=color_map
        )

        fig_bar.update_layout(
            height=260,
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            showlegend=False
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    # ========= WATER TRENDS =========
    with col2:
        st.subheader("Water Trends")

        fig = go.Figure()

        # pH
        fig.add_trace(go.Scatter(
            y=df["ph"],
            mode="lines",
            name="pH (0–14)",
            line=dict(color="#22d3ee", width=2)
        ))

        # TDS
        fig.add_trace(go.Scatter(
            y=df["tds"],
            mode="lines",
            name="TDS (mg/L)",
            line=dict(color="#f59e0b", width=2)
        ))

        # Turbidity
        fig.add_trace(go.Scatter(
            y=df["turbidity"],
            mode="lines",
            name="Turbidity (NTU)",
            line=dict(color="#10b981", width=2)
        ))

        fig.update_layout(
            height=260,
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            yaxis_title="Values",
            xaxis_title="Samples"
        )

        st.plotly_chart(fig, use_container_width=True)

    # ---------------- COMMUNITY SUMMARY ----------------
    st.subheader("📌 Community Risk Summary")

    summary = df.groupby(["community", "risk"]).size().unstack(fill_value=0)

    st.dataframe(summary, use_container_width=True)

    # ---------------- INSIGHT ----------------
    st.subheader("🔍 Insight")

    if not summary.empty:
        high_risk_area = summary["High"].idxmax()
        st.success(f"🚨 Highest risk community: {high_risk_area}")

    # ---------------- RECENT RECORDS ----------------
    st.subheader("⏱ Recent Records")

    st.dataframe(df.tail(10), use_container_width=True)