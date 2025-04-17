import streamlit as st
from gtts import gTTS
import base64
import os

# Page configuration
st.set_page_config(page_title="Stroke Risk Recommendations", layout="wide")
st.title("💡 Stroke Prevention Recommendations")



# Retrieve risk score and inputs from session state
risk_score = st.session_state.get("risk_score")
input_data = st.session_state.get("input_data")

if risk_score is None or input_data is None:
    st.warning("⚠️ " + text["no_score"])
    st.page_link("pages/2_🧠_Results.py", label=text["goto_results"])
    st.stop()

st.markdown(f"### 🧠 {text['based_on_score']} **{risk_score:.2f}%**.")

# Personalized suggestions
st.subheader("🔎 " + text["suggestions"])

if risk_score < 30:
    st.success("✅ " + text["low"])
    st.markdown("""
    - Keep up with regular health checkups.
    - Maintain a balanced diet and exercise.
    - Avoid smoking and manage stress effectively.
    """)
elif 30 <= risk_score < 70:
    st.warning("⚠️ " + text["moderate"])
    st.markdown("""
    - Monitor and manage blood pressure and glucose levels.
    - Limit alcohol intake and avoid smoking.
    - Consider lifestyle modifications like increasing physical activity.
    """)
else:
    st.error("🚨 " + text["high"])
    st.markdown("""
    - Seek medical advice for detailed cardiovascular assessment.
    - Take prescribed medications if necessary (e.g., antihypertensives).
    - Adopt a strict healthy diet and consistent physical activity routine.
    - Completely avoid tobacco products and excessive alcohol.
    """)

# General recommendations
st.subheader("📌 " + text["general"])
st.markdown("""
- Discuss these results with your healthcare provider.
- Develop a personalised prevention plan.
- Schedule regular monitoring of risk factors.
- Learn the warning signs of stroke (**F.A.S.T**) and what to do in case of an emergency.
- Eat more fruits and vegetables, reduce salt and processed foods.
- Maintain a healthy weight and sleep schedule.
- Monitor chronic conditions like diabetes or hypertension.
""")

# Audio output
def create_audio(text, lang_key):
    lang_codes = {
        "English": "en", "French": "fr", "Spanish": "es", "Japanese": "ja",
        "Chinese": "zh-CN", "Akan": "en", "Ga": "en", "Hausa": "en", "Ewe": "en"
    }
    lang_code = lang_codes.get(lang_key, "en")
    try:
        tts = gTTS(text, lang=lang_code)
        file_path = f"tts_{lang_code}.mp3"
        tts.save(file_path)
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            st.audio(f"data:audio/mp3;base64,{b64}", format="audio/mp3")
        os.remove(file_path)
    except Exception:
        st.warning("TTS not available for this language yet.")

create_audio(f"{text['based_on_score']} {risk_score:.2f} percent. {text['general']}", lang_key)

# Styled navigation buttons
st.markdown("""
    <style>
    .button-container {
        display: flex;
        gap: 20px;
        margin-top: 30px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 24px;
        font-size: 16px;
        border-radius: 10px;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.page_link("pages/1_📝_Risk_Assessment.py", label=text["button_assess"], icon="🔁")
with col2:
    st.page_link("Home.py", label=text["button_home"], icon="🏠")


# import openai  # If not already imported

# # --- Chatbot widget (floating button) ---
# st.markdown("""
# <style>
# #floating-chat {
#   position: fixed;
#   bottom: 25px;
#   right: 30px;
#   z-index: 9999;
# }
# .chat-popup {
#   background: white;
#   padding: 20px;
#   border-radius: 10px;
#   width: 320px;
#   box-shadow: 0 4px 8px rgba(0,0,0,0.1);
# }
# </style>
# <div id="floating-chat">
#   <details>
#     <summary style="cursor:pointer;
#                     font-size:16px;
#                     background:#4C9D70;
#                     color:white;
#                     padding:10px 20px;
#                     border-radius:20px;">
#       💬 Chat
#     </summary>
#     <div class="chat-popup">
# """, unsafe_allow_html=True)

# chat_input = st.text_input("💡 Ask about stroke:", key="global_chat")
# if chat_input:
#     resp = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=chat_input,
#         max_tokens=100
#     )
#     reply = resp.choices[0].text.strip()
#     st.markdown(f"<div style='margin-top:10px;'><strong>🤖:</strong> {reply}</div>",
#                 unsafe_allow_html=True)

st.markdown("</div></details></div>", unsafe_allow_html=True)
