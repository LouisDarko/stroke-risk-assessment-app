import streamlit as st
from gtts import gTTS
import base64
import os
import openai

# Hide sidebar, hamburger menu, and Streamlit branding
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Top navigation bar
st.markdown("""
    <style>
    .nav-menu {
        background-color: #4C9D70;
        padding: 15px;
        border-radius: 10px;
        display: flex;
        justify-content: center;
        gap: 40px;
        font-size: 18px;
        margin-bottom: 30px;
    }
    .nav-menu a {
        color: white;
        text-decoration: none;
        font-weight: bold;
    }
    .nav-menu a:hover {
        text-decoration: underline;
    }
    </style>

    <div class='nav-menu'>
        <a href='/Home' target='_self'>🏠 Home</a>
        <a href='/Risk_Assessment' target='_self'>📝 Risk Assessment</a>
        <a href='/Results' target='_self'>📊 Results</a>
    </div>
""", unsafe_allow_html=True)

# Set OpenAI API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Secure storage

# Page config
st.set_page_config(page_title="Stroke Info | AlzEye", layout="wide")

# Text-to-speech function
def create_audio(text, lang_code):
    try:
        tts = gTTS(text, lang=lang_code)
        file_path = f"tts_{lang_code}.mp3"
        tts.save(file_path)
        with open(file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.audio(f"data:audio/mp3;base64,{b64}", format="audio/mp3")
        os.remove(file_path)
    except Exception:
        st.warning("❌ Text-to-speech not available for this language.")

# Language selector
language = st.selectbox("🌍 Language", ["English 🇬🇧", "French 🇫🇷", "Spanish 🇪🇸", "Japanese 🇯🇵", "Chinese 🇨🇳", "Akan 🇬🇭", "Ga 🇬🇭", "Hausa 🇬🇭", "Ewe 🇬🇭"])
lang_key = language.split()[0]

# Translations
translations = {
    "English": {
        "title": "🧠 Learn About Stroke",
        "desc": "A stroke happens when the blood supply to part of your brain is interrupted or reduced, preventing brain tissue from getting oxygen and nutrients.",
        "types": "Types of Stroke",
        "common_causes": "Common Causes",
        "symptoms": "Symptoms",
        "prevention": "Prevention",
        "recognize": "Recognize a Stroke (FAST)",
        "treatment": "Treatment Options",
        "stats": "Stroke Statistics",
        "risk_assessment": "Assess Your Stroke Risk"
    },
    "French": {
        "title": "🧠 Apprenez à propos des AVC",
        "desc": "Un AVC se produit lorsque l'approvisionnement en sang d'une partie de votre cerveau est interrompu ou réduit.",
        "types": "Types d'AVC",
        "common_causes": "Causes courantes",
        "symptoms": "Symptômes",
        "prevention": "Prévention",
        "recognize": "Reconnaître un AVC (FAST)",
        "treatment": "Traitements disponibles",
        "stats": "Statistiques sur les AVC",
        "risk_assessment": "Évaluez votre risque d'AVC"
    },
    # Add more as needed
}

lang_codes = {
    "English": "en", "French": "fr", "Spanish": "es", "Japanese": "ja",
    "Chinese": "zh-CN", "Akan": "en", "Ga": "en", "Hausa": "en", "Ewe": "en"
}

text = translations.get(lang_key, translations["English"])

# Header
st.title(text["title"])
st.write(text["desc"])
create_audio(text["desc"], lang_codes[lang_key])

# Info section builder
def info_section(header, content):
    st.markdown(f"""
        <div style='background-color:#f0f8ff; padding:20px; border-radius:10px; margin-bottom:20px;'>
            <h4>{header}</h4>
            {content}
        </div>
    """, unsafe_allow_html=True)

# Stroke information sections
info_section(text["types"], """
<ul>
    <li><strong>Ischemic:</strong> Blockage in brain arteries.</li>
    <li><strong>Hemorrhagic:</strong> Burst blood vessels in the brain.</li>
    <li><strong>TIA:</strong> Temporary blockage (mini-stroke).</li>
</ul>
""")

info_section(text["common_causes"], """
<ul>
    <li>High blood pressure</li>
    <li>Heart disease</li>
    <li>Diabetes</li>
    <li>Smoking</li>
    <li>Obesity and cholesterol</li>
</ul>
""")

info_section(text["symptoms"], """
<ul>
    <li>Sudden numbness or weakness (face, arm, leg)</li>
    <li>Confusion, speech trouble</li>
    <li>Vision problems</li>
    <li>Dizziness or balance issues</li>
</ul>
""")

info_section(text["prevention"], """
<ul>
    <li>Control blood pressure & sugar</li>
    <li>Exercise regularly</li>
    <li>Eat a healthy diet</li>
    <li>Stop smoking</li>
</ul>
""")

info_section(text["recognize"], """
<strong>Use the FAST test:</strong>
<ul>
    <li><strong>F:</strong> Face drooping</li>
    <li><strong>A:</strong> Arm weakness</li>
    <li><strong>S:</strong> Speech difficulty</li>
    <li><strong>T:</strong> Time to call emergency</li>
</ul>
""")

info_section(text["treatment"], """
<ul>
    <li>Clot-busting medication</li>
    <li>Rehabilitation therapy</li>
    <li>Surgical intervention</li>
</ul>
""")

info_section(text["stats"], """
<ul>
    <li>2nd leading cause of death globally</li>
    <li>12.2 million cases in 2020</li>
    <li>5.5 million deaths annually</li>
</ul>
""")

# Final call to action: Responsive button with hover animation
st.markdown(f"""
    <div style='background-color:#e6f2ff; padding:20px; border-radius:10px; text-align:center; margin-top:30px;'>
        <h4>{text["risk_assessment"]}</h4>
        <p>Click the button below to assess your personal stroke risk using our intelligent tool.</p>
        <a href='/Risk_Assessment' target='_self'>
            <button style='background-color:#4C9D70; color:white; padding:10px 20px; font-size:16px; border:none; border-radius:8px; cursor:pointer; transition:all 0.3s ease;'>
                📝 Go to Risk Assessment
            </button>
        </a>
    </div>
    <style>
    button:hover {{
        background-color: #3e8e41;
        transform: scale(1.1);
    }}
    </style>
""", unsafe_allow_html=True)

import openai  # If not already imported

# --- Chatbot widget (floating button) ---
st.markdown("""
<style>
#floating-chat {
  position: fixed;
  bottom: 25px;
  right: 30px;
  z-index: 9999;
}
.chat-popup {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 320px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
</style>
<div id="floating-chat">
  <details>
    <summary style="cursor:pointer;
                    font-size:16px;
                    background:#4C9D70;
                    color:white;
                    padding:10px 20px;
                    border-radius:20px;">
      💬 Chat
    </summary>
    <div class="chat-popup">
""", unsafe_allow_html=True)

chat_input = st.text_input("💡 Ask about stroke:", key="global_chat")
if chat_input:
    resp = openai.Completion.create(
        engine="text-davinci-003",
        prompt=chat_input,
        max_tokens=100
    )
    reply = resp.choices[0].text.strip()
    st.markdown(f"<div style='margin-top:10px;'><strong>🤖:</strong> {reply}</div>",
                unsafe_allow_html=True)

st.markdown("</div></details></div>", unsafe_allow_html=True)
