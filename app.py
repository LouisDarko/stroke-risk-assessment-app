import streamlit as st
from gtts import gTTS
import base64
import os

# Page configuration
st.set_page_config(page_title="Stroke Risk Prediction", layout="wide")

# Hide Streamlit default elements
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Navigation Bar
st.markdown("""
    <style>
        .nav-menu {
            background-color: #4C9D70;
            padding: 15px;
            border-radius: 12px;
            display: flex;
            justify-content: center;
            gap: 40px;
            font-size: 18px;
            margin-bottom: 40px;
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
        <a href='/Recommendations' target='_self'>🤝🏾 Recommendations</a>
    </div>
""", unsafe_allow_html=True)

# Header and introduction
st.title("🧠 Learn About Stroke")
intro_text = """
A stroke happens when the blood supply to part of your brain is interrupted or reduced, 
preventing brain tissue from getting oxygen and nutrients. Early detection can save lives.
"""
st.markdown(f"<p style='font-size:18px;'>{intro_text}</p>", unsafe_allow_html=True)

# Text-to-speech
def create_audio(text):
    try:
        tts = gTTS(text, lang='en')
        file_path = f"tts_intro.mp3"
        tts.save(file_path)
        with open(file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.audio(f"data:audio/mp3;base64,{b64}", format="audio/mp3")
        os.remove(file_path)
    except Exception:
        st.warning("❌ Audio not available.")

create_audio(intro_text)

# Stroke Information Sections
def info_card(icon, title, content):
    st.markdown(f"""
        <div style='background-color:#f0f8ff; padding:25px; border-radius:15px; margin-bottom:20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);'>
            <h4 style='font-size:22px;'>{icon} {title}</h4>
            <div style='font-size:16px;'>{content}</div>
        </div>
    """, unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    info_card("🧩", "Types of Stroke", """
    <ul>
        <li><strong>Ischemic:</strong> Blockage in brain arteries.</li>
        <li><strong>Hemorrhagic:</strong> Burst blood vessels in the brain.</li>
        <li><strong>TIA:</strong> Temporary blockage (mini-stroke).</li>
    </ul>
    """)

    info_card("❗", "Common Causes", """
    <ul>
        <li>High blood pressure</li>
        <li>Heart disease</li>
        <li>Diabetes</li>
        <li>Smoking</li>
        <li>Obesity and cholesterol</li>
    </ul>
    """)

    info_card("🩺", "Prevention", """
    <ul>
        <li>Control blood pressure & sugar</li>
        <li>Exercise regularly</li>
        <li>Eat a healthy diet</li>
        <li>Stop smoking</li>
    </ul>
    """)

with col2:
    info_card("⚠️", "Symptoms", """
    <ul>
        <li>Sudden numbness or weakness (face, arm, leg)</li>
        <li>Confusion, speech trouble</li>
        <li>Vision problems</li>
        <li>Dizziness or balance issues</li>
    </ul>
    """)

    info_card("⏱️", "Recognize a Stroke (FAST)", """
    <strong>Use the FAST test:</strong>
    <ul>
        <li><strong>F:</strong> Face drooping</li>
        <li><strong>A:</strong> Arm weakness</li>
        <li><strong>S:</strong> Speech difficulty</li>
        <li><strong>T:</strong> Time to call emergency</li>
    </ul>
    """)

    info_card("📊", "Stroke Statistics", """
    <ul>
        <li>2nd leading cause of death globally</li>
        <li>12.2 million cases in 2020</li>
        <li>5.5 million deaths annually</li>
    </ul>
    """)

# Call to Action
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
        background-color: #3e8e41;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)
