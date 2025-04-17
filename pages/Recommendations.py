import streamlit as st




# Page configuration
st.set_page_config(page_title="Stroke Risk Recommendations", layout="wide")
st.title("💡 Stroke Prevention Recommendations")

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
        <a href='/' target='_self'>🏠 Home</a>
        <a href='/Risk_Assessment' target='_self'>📝 Risk Assessment</a>
        <a href='/Results' target='_self'>📊 Results</a>
        <a href='/Recommendations' target='_self'>🤝🏾 Recommendations</a>
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
