import streamlit as st
from utils.ui import global_header
from pages.database import init_db

init_db()

st.set_page_config(
    page_title="Water Monitoring",
    layout="wide"
)

st.markdown("""
<style>
.stApp { background-color: #020617; }
[data-testid="stSidebar"] { display: none; }

div[role="radiogroup"] {
    display: flex !important;
    justify-content: center !important;
    gap: 25px;
    margin: 15px 0 25px 0;
}

label[data-baseweb="radio"] {
    background: rgba(255,255,255,0.05);
    padding: 10px 16px;
    border-radius: 10px;
}

input[type="radio"]:checked + div {
    color: #38bdf8 !important;
    font-weight: 600;
}

h1, h2, h3 { color: #f8fafc !important; }
p { color: #94a3b8 !important; }
</style>
""", unsafe_allow_html=True)

global_header()

page = st.radio(
    "",
    ["📊 Dashboard", "🔮 Predict", "🗂 Records", "🏥 Health", "📰 Articles"],
    horizontal=True
)

if page == "📊 Dashboard":
    import pages.dashboard as d
    d.run()

elif page == "🔮 Predict":
    import pages.prediction as p
    p.run()

elif page == "🗂 Records":
    import pages.records as r
    r.run()

elif page == "🏥 Health":
    import pages.health as h
    h.run()

elif page == "📰 Articles":
    import pages.articles as a
    a.run()