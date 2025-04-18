import streamlit as st
from gtts import gTTS
import base64
import os

# Set page configuration
st.set_page_config(page_title="Stroke Risk Prediction", layout="wide")

# Hide Streamlit default elements and sidebar
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        [data-testid="stSidebar"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# Custom Header
st.markdown("""
    <div style="background-color: #4C9D70; padding: 20px; border-radius: 12px; margin-bottom: 20px;">
        <h1 style="color: white; text-align: center; margin: 0;">🧠 Stroke Risk Assessment Tool</h1>
        <p style="color: white; text-align: center; font-size: 18px;">Empowering you to take control of your brain health</p>
    </div>
""", unsafe_allow_html=True)

# Custom Navbar
st.markdown("""
    <style>
        .custom-nav {
            background-color: #e8f5e9;
            padding: 15px 0;
            border-radius: 10px;
            display: flex;
            justify-content: center;
            gap: 60px;
            margin-bottom: 30px;
            font-size: 18px;
            font-weight: 600;
        }
        .custom-nav a {
            text-decoration: none;
            color: #4C9D70;
        }
        .custom-nav a:hover {
            color: #388e3c;
            text-decoration: underline;
        }
    </style>
    <div class="custom-nav">
        <a href='/Home' target='_self'>Home</a>
        <a href='/Risk_Assessment' target='_self'>Risk Assessment</a>
        <a href='/Results' target='_self'>Results</a>
        <a href='/Recommendations' target='_self'>Recommendations</a>
    </div>
""", unsafe_allow_html=True)

# Header and Intro
st.title("🧠 Learn About Stroke")
intro_text = """
A stroke happens when the blood supply to part of your brain is interrupted or reduced, 
preventing brain tissue from getting oxygen and nutrients. Early detection can save lives.
"""
st.markdown(f"<p style='font-size:18px;'>{intro_text}</p>", unsafe_allow_html=True)

# All content for audio narration (combine all section texts)
full_page_text = """
Learn About Stroke

A stroke happens when the blood supply to part of your brain is interrupted or reduced, 
preventing brain tissue from getting oxygen and nutrients. Early detection can save lives.

Types of Stroke:
- Ischemic: Blockage in brain arteries.
- Hemorrhagic: Burst blood vessels in the brain.
- TIA: Temporary blockage (mini-stroke).

Common Causes:
- High blood pressure
- Heart disease
- Diabetes
- Smoking
- Obesity and cholesterol

Prevention:
- Control blood pressure and sugar
- Exercise regularly
- Eat a healthy diet
- Stop smoking

Symptoms:
- Sudden numbness or weakness (face, arm, leg)
- Confusion, speech trouble
- Vision problems
- Dizziness or balance issues

Recognize a Stroke (FAST):
- F: Face drooping
- A: Arm weakness
- S: Speech difficulty
- T: Time to call emergency

Stroke Statistics:
- 2nd leading cause of death globally
- 12.2 million cases in 2020
- 5.5 million deaths annually

- Assess Your Stroke Risk
- Click below to use our intelligent tool and evaluate your risk level
"""

# Generate full-page audio with controls
def generate_audio(text, filename="full_page.mp3"):
    tts = gTTS(text, lang='en')
    tts.save(filename)
    with open(filename, "rb") as f:
        audio_data = f.read()
        b64_audio = base64.b64encode(audio_data).decode()
        audio_html = f"""
            <audio controls style="width: 100%; margin-top: 20px;">
                <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
        """
        st.markdown("### 🔊 Listen to this page")
        st.markdown(audio_html, unsafe_allow_html=True)

generate_audio(full_page_text)

# Section cards with consistent size using Flexbox
st.markdown("""
    <style>
        .info-cards-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            gap: 30px;
            margin-top: 30px;
        }
        .info-card {
            background-color: #f0f8ff;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            width: 48%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 300px;
            box-sizing: border-box; /* Fix issue where padding increases card height */
        }
        .info-card h4 {
            font-size: 22px;
            margin-bottom: 15px;
        }
        .info-card ul {
            font-size: 16px;
            margin-top: 10px;
        }
        .info-card a {
            color: #4C9D70;
            font-weight: bold;
            text-decoration: none;
        }
        .info-card a:hover {
            color: #388e3c;
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# Info Card content
def info_card(icon, title, content):
    return f"""
        <div class="info-card">
            <h4>{icon} {title}</h4>
            <div>{content}</div>
        </div>
    """

# Cards in columns
cards_content = [
    ("🧩", "Types of Stroke", """
        <ul>
            <li><strong>Ischemic:</strong> Blockage in brain arteries.</li>
            <li><strong>Hemorrhagic:</strong> Burst blood vessels in the brain.</li>
            <li><strong>TIA:</strong> Temporary blockage (mini-stroke).</li>
        </ul>
    """),
    ("❗", "Common Causes", """
        <ul>
            <li>High blood pressure</li>
            <li>Heart disease</li>
            <li>Diabetes</li>
            <li>Smoking</li>
            <li>Obesity and cholesterol</li>
        </ul>
    """),
    ("🩺", "Prevention", """
        <ul>
            <li>Control blood pressure & sugar</li>
            <li>Exercise regularly</li>
            <li>Eat a healthy diet</li>
            <li>Stop smoking</li>
        </ul>
    """),
    ("⚠️", "Symptoms", """
        <ul>
            <li>Sudden numbness or weakness (face, arm, leg)</li>
            <li>Confusion, speech trouble</li>
            <li>Vision problems</li>
            <li>Dizziness or balance issues</li>
        </ul>
    """),
    ("⏱️", "Recognize a Stroke (FAST)", """
        <strong>Use the FAST test:</strong>
        <ul>
            <li><strong>F:</strong> Face drooping</li>
            <li><strong>A:</strong> Arm weakness</li>
            <li><strong>S:</strong> Speech difficulty</li>
            <li><strong>T:</strong> Time to call emergency</li>
        </ul>
    """),
    ("📊", "Stroke Statistics", """
        <ul>
            <li>2nd leading cause of death globally</li>
            <li>12.2 million cases in 2020</li>
            <li>5.5 million deaths annually</li>
        </ul>
    """)
]

# Render all cards in the container
card_elements = "".join([info_card(card[0], card[1], card[2]) for card in cards_content])

st.markdown(f"<div class='info-cards-container'>{card_elements}</div>", unsafe_allow_html=True)

# Call to Action (CTA)
st.markdown("""
    <div style='background-color:#e6f2ff; padding:30px; border-radius:12px; text-align:center; margin-top:30px;'>
        <h4>📝 Assess Your Stroke Risk</h4>
        <p>Click below to use our intelligent tool and evaluate your risk level.</p>
        <a href='/Risk_Assessment' target='_self'>
            <button style='background-color:#4C9D70; color:white; padding:12px 24px; font-size:16px; border:none; border-radius:8px; cursor:pointer; transition:all 0.3s ease;'>
                ➡️ Start Risk Assessment
            </button>
        </a>
    </div>
    <style>
    button:hover {
        background-color: #3e8e3c;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# Custom Footer with Developer Credit and Transparent Background
st.markdown("""
    <style>
        .custom-footer {
            background-color: rgba(76, 157, 112, 0.6);
            color: white;
            padding: 30px 0;
            border-radius: 12px;
            margin-top: 40px;
            text-align: center;
            font-size: 14px;
            width: 100%;
            position: relative;
        }
        .custom-footer a {
            color: white;
            text-decoration: none;
            margin: 0 15px;
        }
        .custom-footer a:hover {
            text-decoration: underline;
        }
        .footer-text {
            width: 80%;
            margin: 0 auto;
        }
    </style>
    <div class="custom-footer">
        <div class="footer-text">
            <p>&copy; 2025 Stroke Risk Assessment Tool | All rights reserved</p>
            <p>
                <a href='/Home' target='_self'>Home</a>
                <a href='/Risk_Assessment' target='_self'>Risk Assessment</a>
                <a href='/Results' target='_self'>Results</a>
                <a href='/Recommendations' target='_self'>Recommendations</a>
            </p>
            <p style="font-size: 12px; margin-top: 10px;">Developed by Victoria Mends</p>
        </div>
    </div>
""", unsafe_allow_html=True)
