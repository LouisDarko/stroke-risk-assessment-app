import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from gtts import gTTS
import base64
import os



# Page title and layout
st.set_page_config(page_title="Stroke Risk Results", layout="wide")

# Hide Streamlit default elements and sidebar
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        [data-testid="stSidebar"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}
    </style>
""", unsafe_allow_html=True)

st.title("📊 Stroke Risk Results")



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


# Check if user data and prediction probability exist in session state
if 'user_data' in st.session_state and 'prediction_prob' in st.session_state:
    user_data = st.session_state.user_data
    prediction_prob = st.session_state.prediction_prob

    # Stroke risk result header
    st.header("🧠 Stroke Risk Probability")
    st.write(f"Based on your input data, your stroke risk probability is: **{prediction_prob * 100:.2f}%**")

    if prediction_prob > 0.5:
        st.warning("⚠️ Higher Risk of Stroke Detected")
    else:
        st.success("✔️ Lower Risk of Stroke Detected")

    # Understanding your results
    st.subheader("Understanding Your Results")
    st.write("The graph below shows how different health factors may contribute to your overall risk:")

    # Create bar chart based on user's inputs
    risk_data = {
        'Age': user_data['age'],
        'Hypertension': 1 if user_data['hypertension'] == "Yes" else 0,
        'Heart Disease': 1 if user_data['heart_disease'] == "Yes" else 0,
        'Average Glucose': user_data['avg_glucose'],
        'Smoking Status': 1 if user_data['smoking_status'] == "Smokes" else (2 if user_data['smoking_status'] == "Formerly smoked" else 0)
    }

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=list(risk_data.keys()), y=list(risk_data.values()), palette='pastel', ax=ax)
    ax.set_ylabel("Relative Contribution Score")
    ax.set_title("Your Health Factors")
    st.pyplot(fig)

    # Generate audio description (optional)
    # def create_audio(text, lang="en"):
    #     try:
    #         tts = gTTS(text, lang=lang)
    #         file_path = "tts_output.mp3"
    #         tts.save(file_path)
    #         with open(file_path, "rb") as f:
    #             data = f.read()
    #             b64 = base64.b64encode(data).decode()
    #             st.audio(f"data:audio/mp3;base64,{b64}", format="audio/mp3")
    #         os.remove(file_path)
    #     except Exception as e:
    #         st.warning("Audio playback is unavailable.")

    # create_audio(f"Your stroke risk probability is {prediction_prob * 100:.1f} percent.")

    # Recommendations button
    st.markdown("### 📘 Click below to get personalized recommendations based on your results:")
    if st.button("Click for Recommendations"):
        st.switch_page("pages/Recommendations.py")

else:
    st.warning("No user data found. Please complete the risk assessment first.")


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

col1, col2 = st.columns([1, 1])
with col1:
    st.page_link("pages/Risk_Assessment.py", label="Go back to Risk Assessment", icon="🔙")


# Reset the flag so the user cannot directly access the Results page without calculating the risk
st.session_state.risk_calculated = False




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
