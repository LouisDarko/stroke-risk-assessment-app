import streamlit as st

# Page configuration
st.set_page_config(page_title="Stroke Risk Recommendations", layout="wide")

# Hide Streamlit default elements and sidebar
st.markdown("""
    <style>
        #MainMenu, header {visibility: hidden;}
        [data-testid="stSidebar"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}
    </style>
""", unsafe_allow_html=True)

st.title("💡 Stroke Prevention Recommendations")

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

# Retrieve risk score and inputs from session state
risk_score = st.session_state.get("risk_score")
input_data = st.session_state.get("input_data")

if risk_score is None or input_data is None:
    st.warning("⚠️ No stroke risk score found. Please complete the assessment first.")
    st.page_link("pages/Results.py", label="Go to Results Page")
    st.stop()

st.markdown(f"### 🧠 Your estimated stroke risk is **{risk_score:.2f}%**.")

# Personalized suggestions
st.subheader("🔎 Personalized Recommendations")

if risk_score < 30:
    st.success("✅ You have a low risk. Keep up the good work!")
    st.markdown("""
    - Keep up with regular health checkups.
    - Maintain a balanced diet and exercise.
    - Avoid smoking and manage stress effectively.
    """)
elif 30 <= risk_score < 70:
    st.warning("⚠️ You are at moderate risk. Take proactive steps to lower it.")
    st.markdown("""
    - Monitor and manage blood pressure and glucose levels.
    - Limit alcohol intake and avoid smoking.
    - Consider lifestyle modifications like increasing physical activity.
    """)
else:
    st.error("🚨 You are at high risk. Please take immediate action.")
    st.markdown("""
    - Seek medical advice for detailed cardiovascular assessment.
    - Take prescribed medications if necessary (e.g., antihypertensives).
    - Adopt a strict healthy diet and consistent physical activity routine.
    - Completely avoid tobacco products and excessive alcohol.
    """)

# General recommendations
st.subheader("📌 General Stroke Prevention Tips")
st.markdown("""
- Discuss these results with your healthcare provider.
- Develop a personalised prevention plan.
- Schedule regular monitoring of risk factors.
- Learn the warning signs of stroke (**F.A.S.T**) and what to do in case of an emergency.
- Eat more fruits and vegetables, reduce salt and processed foods.
- Maintain a healthy weight and sleep schedule.
- Monitor chronic conditions like diabetes or hypertension.
""")

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
    st.page_link("pages/Risk_Assessment.py", label="Reassess Risk", icon="🔁")
with col2:
    st.page_link("app.py", label="Back to Home", icon="🏠")

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

# Ensure the footer stays at the bottom when the page content is small
st.markdown("""
    <style>
        .stApp {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .stApp > .main {
            flex: 1;
        }
    </style>
""", unsafe_allow_html=True)
