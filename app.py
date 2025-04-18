import streamlit as st
from gtts import gTTS
import base64
import os

# Page config
st.set_page_config(page_title="Stroke Risk Prediction", layout="wide")

# Hide Streamlit default elements
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Navigation bar
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

# Header content
st.title("🧠 Learn About Stroke")

intro_text = """
A stroke happens when the blood supply to part of your brain is interrupted or reduced, 
preventing brain tissue from getting oxygen and nutrients. Early detection can save lives.
"""
st.markdown(f"<p style='font-size:18px;'>{intro_text}</p>", unsafe_allow_html=True)

# Full page text
full_page_text = """
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
- Control blood pressure & sugar
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
"""

# Generate audio file once
def generate_audio(text, filename="page_audio.mp3"):
    if not os.path.exists(filename):
        tts = gTTS(text, lang='en')
        tts.save(filename)
    with open(filename, "rb") as audio_file:
        audio_bytes = audio_file.read()
        b64_audio = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
        <audio controls style="width: 100%;">
            <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

# Audio player for full page
st.subheader("🔊 Listen to this page")
generate_audio(full_page_text)

# Content sections
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
