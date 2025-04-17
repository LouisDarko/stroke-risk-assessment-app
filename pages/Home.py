import streamlit as st
from gtts import gTTS
import base64
import os

# Hide sidebar, hamburger menu, and Streamlit branding
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Custom CSS for improving the UI
st.markdown("""
    <style>
    /* General page styles */
    body {
        font-family: 'Arial', sans-serif;
        background-color: #fafafa;
        color: #333;
    }

    /* Top Navigation Bar */
    .nav-menu {
        background-color: #4C9D70;
        padding: 12px 30px;
        border-radius: 15px;
        display: flex;
        justify-content: center;
        gap: 40px;
        font-size: 18px;
        font-weight: bold;
    }
    .nav-menu a {
        color: white;
        text-decoration: none;
        font-size: 18px;
    }
    .nav-menu a:hover {
        text-decoration: underline;
    }

    /* Section containers */
    .section-container {
        background-color: #ffffff;
        padding: 30px;
        margin-bottom: 40px;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    }
    
    .section-header {
        color: #4C9D70;
        font-size: 28px;
        margin-bottom: 15px;
        text-align: center;
    }

    .section-content {
        font-size: 18px;
        line-height: 1.6;
    }

    /* Text-to-Speech Button Styling */
    .tts-btn {
        background-color: #4C9D70;
        color: white;
        padding: 12px 24px;
        font-size: 16px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: block;
        margin: 20px auto;
    }

    .tts-btn:hover {
        background-color: #3e8e41;
        transform: scale(1.05);
    }

    /* Call to Action Section */
    .cta-section {
        background-color: #e6f2ff;
        padding: 40px;
        border-radius: 12px;
        text-align: center;
        margin-top: 30px;
    }

    .cta-section h4 {
        font-size: 26px;
        color: #333;
    }

    .cta-section p {
        font-size: 18px;
        color: #555;
        margin-bottom: 30px;
    }

    .cta-section button {
        background-color: #4C9D70;
        color: white;
        padding: 12px 24px;
        font-size: 18px;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .cta-section button:hover {
        background-color: #3e8e41;
        transform: scale(1.1);
    }
    </style>
""", unsafe_allow_html=True)

# Top navigation bar
st.markdown("""
    <div class="nav-menu">
        <a href="?page=home" target="_self">🏠 Home</a>
        <a href="?page=risk_assessment" target="_self">📝 Risk Assessment</a>
        <a href="?page=results" target="_self">📊 Results</a>
    </div>
""", unsafe_allow_html=True)

# Get the language from query params
query_params = st.query_params
language = query_params.get("language", ["English"])[0]  # Default to English if no language is provided

# Translations dictionary
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
    # More translations as necessary...
}

# Get content for the selected language
text = translations.get(language, translations["English"])

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
        st.warning("❌ Audio not available for this language.")

# Header and Description
st.markdown(f"""
    <div class="section-container">
        <h2 class="section-header">{text["title"]}</h2>
        <p class="section-content">{text["desc"]}</p>
        <button class="tts-btn" onclick="create_audio('{text["desc"]}', 'en')">🔊 Listen</button>
    </div>
""", unsafe_allow_html=True)

# Stroke Information Section
def info_section(header, content):
    st.markdown(f"""
        <div class="section-container">
            <h3 class="section-header">{header}</h3>
            <div class="section-content">
                {content}
            </div>
        </div>
    """, unsafe_allow_html=True)
    create_audio(content, "en")

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

# Final Call to Action Section
st.markdown(f"""
    <div class="cta-section">
        <h4>{text["risk_assessment"]}</h4>
        <p>Click the button below to assess your personal stroke risk using our intelligent tool.</p>
        <a href="?page=risk_assessment" target="_self">
            <button>📝 Go to Risk Assessment</button>
        </a>
    </div>
""", unsafe_allow_html=True)

