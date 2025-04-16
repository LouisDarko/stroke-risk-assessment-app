import streamlit as st
from pages import home, assessment, results, recommendations, chatbot

# Set page config
st.set_page_config(page_title="Stroke Risk Assessment", layout="wide")

# Sidebar menu
menu = st.sidebar.selectbox("Menu", ["Home", "Risk Assessment", "Understanding Your Results", "Recommendations", "Chatbot Support"])

# Routing
if menu == "Home":
    home.app()
elif menu == "Risk Assessment":
    assessment.app()
elif menu == "Understanding Your Results":
    results.app()
elif menu == "Recommendations":
    recommendations.app()
elif menu == "Chatbot Support":
    chatbot.app()