import streamlit as st
from translations.lang import get_text
import streamlit.components.v1 as components

# Custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Language selector in header
lang = st.selectbox("🌍 Select Language", ["English", "French", "Spanish", "Swahili", "Arabic"])
_ = lambda x: get_text(x, lang)

# Navigation menu
menu = st.columns(4)
with menu[0]:
    if st.button(_("Home")):
        st.switch_page("app.py")
with menu[1]:
    if st.button(_("Risk Form")):
        st.switch_page("pages/1_🧾_Risk_Form.py")
with menu[2]:
    if st.button(_("Results")):
        st.switch_page("pages/2📊_Results.py")
with menu[3]:
    if st.button(_("Recommendations")):
        st.switch_page("pages/3💡_Recommendations.py")

# Home Page Content
st.markdown(f"<h1>{_('Welcome to Stroke Risk Assessment App')}</h1>", unsafe_allow_html=True)
st.markdown(f"""
<p>{_('This app helps you assess your risk of having a stroke based on key health factors.')}</p>
<ul>
  <li>{_('Learn about stroke and how to prevent it.')}</li>
  <li>{_('Enter your health data securely.')}</li>
  <li>{_('Get visual insights and expert recommendations.')}</li>
</ul>
""", unsafe_allow_html=True)

components.html(\"\"\"
<!-- Floating Chatbot Button -->
<div id="chatbot-button" onclick="alert('Chatbot coming soon!')">
  💬
</div>
\"\"\", height=100)
