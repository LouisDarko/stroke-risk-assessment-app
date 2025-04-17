import streamlit as st
from streamlit_option_menu import option_menu
from pages import home, assessment, results, recommendations, chatbot

st.set_page_config(page_title="Stroke Risk App", layout="wide")

# Custom CSS
st.markdown("""
<style>
body {
    background-color: #f9f9fb;
}
header {
    visibility: hidden;
}
.main {
    padding-top: 10px;
}
.chat-button {
    position: fixed;
    bottom: 30px;
    right: 30px;
    background-color: #4CAF50;
    color: white;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    text-align: center;
    line-height: 60px;
    font-size: 30px;
    cursor: pointer;
    z-index: 1000;
}
</style>
""", unsafe_allow_html=True)

# Language selection
lang = st.selectbox("🌐 Select Language", ["English", "Français"])

# Horizontal menu
selected = option_menu(
    menu_title=None,
    options=["Home", "Assessment", "Results", "Recommendations"],
    icons=["house", "clipboard-check", "bar-chart", "lightbulb"],
    orientation="horizontal"
)

# Page navigation
if selected == "Home":
    home.app(lang)
elif selected == "Assessment":
    assessment.app(lang)
elif selected == "Results":
    results.app(lang)
elif selected == "Recommendations":
    recommendations.app(lang)

# Floating Chatbot on Home page only
if selected == "Home":
    st.markdown('<a href="#chatbot"><div class="chat-button">💬</div></a>', unsafe_allow_html=True)
    chatbot.app(lang)