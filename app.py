import streamlit as st
import base64
import os
import openai
from top_nav import top_nav
from translations import get_translation

# Hide default Streamlit UI elements
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Page configuration
st.set_page_config(page_title="Stroke Risk Assessment App", layout="wide")

# Top navigation bar
top_nav()

# Language selection for translations
language = st.selectbox("🌍 Language", list(get_translation('').keys()))
lang_key = language.split()[0]
text = get_translation(lang_key)

# OpenAI API Key setup
openai.api_key = st.secrets.get("OPENAI_API_KEY")

# Home page content
st.title(text['title'])
st.write(text['desc'])

# Text-to-speech helper
def create_audio(text_str, lang_code):
    try:
        from gtts import gTTS
        tts = gTTS(text_str, lang=lang_code)
        file_path = f"tts_home_{lang_code}.mp3"
        tts.save(file_path)
        with open(file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.audio(f"data:audio/mp3;base64,{b64}", format="audio/mp3")
        os.remove(file_path)
    except Exception:
        st.warning("Audio not available for this language.")

create_audio(text['desc'], text.get('lang_code','en'))

# Warning signs section
st.markdown(f"""
<div style='background-color:#fff3cd; padding:20px; border-radius:10px;'>
  <h4>{text['warning']}</h4>
  <ul>
    {''.join(f'<li>{item}</li>' for item in text['warning_list'])}
  </ul>
</div>
""", unsafe_allow_html=True)

# Call-to-action button to Risk Assessment
st.markdown(f"""
<style>
.cta-btn {{
  display: block;
  width: fit-content;
  margin: 30px auto;
  background-color: #4C9D70;
  color: white;
  padding: 12px 24px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s ease, background-color 0.2s ease;
}}
.cta-btn:hover {{
  background-color: #3e8e41;
  transform: scale(1.05);
}}
</style>
<a href='Risk_Assessment' target='_self'>
  <button class='cta-btn'>{text['cta']}</button>
</a>
""", unsafe_allow_html=True)
