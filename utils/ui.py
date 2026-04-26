import streamlit as st


def global_header():
    st.markdown(
        """
        <div style="text-align:center; margin-bottom:20px;">
            <h1 style="color:#38bdf8; margin:0;">
                💧 Smart Water Monitoring System
            </h1>
            <p style="color:#94a3b8; margin-top:6px;">
                AI-Based Early Warning System
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def header(title, subtitle=""):
    st.markdown(f"## {title}")

    if subtitle:
        st.markdown(
            f"<p style='color:#94a3b8; font-size:13px; margin-top:-8px;'>{subtitle}</p>",
            unsafe_allow_html=True
        )