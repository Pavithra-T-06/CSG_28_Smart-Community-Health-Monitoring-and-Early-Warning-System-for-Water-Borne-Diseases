import streamlit as st


# ---------------- CARD COMPONENT ----------------
def resource_card(title, desc, points, link):
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.05);
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    ">
        <div>
            <h4 style="margin:0;color:#f8fafc;">{title}</h4>
            <p style="margin:4px 0;color:#94a3b8;">{desc}</p>
            <ul style="margin:4px 0;color:#cbd5f5;">
                {''.join([f"<li>{p}</li>" for p in points])}
            </ul>
        </div>
        <a href="{link}" target="_blank" style="
            color:#38bdf8;
            font-weight:600;
            text-decoration:none;
        ">Open →</a>
    </div>
    """, unsafe_allow_html=True)


# ---------------- MAIN ----------------
def run():
    st.title("📰 Resources")
    st.caption("Trusted water & health information")

    # Get last prediction risk
    risk = st.session_state.get("last_risk", "Low")

    # ---------------- RECOMMENDED ----------------
    st.subheader("🧠 Recommended for You")

    if risk == "High":
        st.warning("Based on recent high-risk detection")

        resource_card(
            "🌍 WHO Water Safety",
            "Global contamination & safety standards",
            ["Water quality limits", "Contamination control", "Safe consumption practices"],
            "https://www.who.int"
        )

        resource_card(
            "🧫 CDC Water Diseases",
            "Prevent waterborne diseases",
            ["Bacterial infection prevention", "Symptoms awareness", "Sanitation practices"],
            "https://www.cdc.gov"
        )

    elif risk == "Medium":
        st.info("Moderate risk – precautionary resources")

        resource_card(
            "💧 UNICEF Water Safety",
            "Hygiene & sanitation practices",
            ["Safe storage methods", "Basic filtration", "Clean handling"],
            "https://www.unicef.org"
        )

    else:
        st.success("Low risk – maintain safe practices")

        resource_card(
            "🇮🇳 India Water Portal",
            "Local water awareness",
            ["Water conservation", "Safe usage", "Community solutions"],
            "https://www.indiawaterportal.org"
        )

    st.divider()

    # ---------------- QUICK ACTIONS ----------------
    st.subheader("⚡ Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### 🚰 Boiling Guide
        - Boil for 5–10 minutes  
        - Cool in clean container  
        - Store covered  
        """)

    with col2:
        st.markdown("""
        ### 🧴 Filtration Tips
        - Use certified filters  
        - Clean regularly  
        - Replace cartridges  
        """)

    with col3:
        st.markdown("""
        ### 🧼 Hygiene Tips
        - Wash hands before handling water  
        - Keep containers clean  
        - Avoid open storage  
        """)

    st.divider()

    # ---------------- ALL RESOURCES ----------------
    st.subheader("📚 All Resources")

    resource_card(
        "🌍 WHO Guidelines",
        "Global drinking water standards",
        ["Safe pH levels", "Contaminant limits", "Health safety norms"],
        "https://www.who.int"
    )

    resource_card(
        "💧 UNICEF Water",
        "Sanitation and hygiene insights",
        ["Clean water access", "Child health", "Safe practices"],
        "https://www.unicef.org"
    )

    resource_card(
        "🧫 CDC Water Diseases",
        "Waterborne disease prevention",
        ["Disease control", "Symptoms awareness", "Prevention methods"],
        "https://www.cdc.gov"
    )

    resource_card(
        "🏦 World Bank Water",
        "Water policies and research",
        ["Infrastructure", "Global water issues", "Development programs"],
        "https://www.worldbank.org"
    )

    resource_card(
        "🇮🇳 India Water Portal",
        "Local water issues and solutions",
        ["Indian water data", "Community insights", "Solutions"],
        "https://www.indiawaterportal.org"
    )