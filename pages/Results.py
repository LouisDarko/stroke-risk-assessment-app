import streamlit as st
import joblib
import sklearn
import os
import numpy as np

# ── Page config & hide defaults ────────────────────────────────────────────────
st.set_page_config(page_title="Stroke Risk Assessment", layout="wide")
st.markdown("""
    <style>
      #MainMenu, footer, header {visibility: hidden;}
      [data-testid="stSidebar"], [data-testid="collapsedControl"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# ── Title & Navbar ─────────────────────────────────────────────────────────────
st.title("📝 Stroke Risk Assessment")
st.markdown("""
  <style>
    .custom-nav {
      background: #e8f5e9; padding: 15px 0; border-radius: 10px;
      display: flex; justify-content: center; gap: 60px; margin-bottom: 30px;
      font-size: 18px; font-weight: 600;
    }
    .custom-nav a { text-decoration: none; color: #4C9D70; }
    .custom-nav a:hover { color: #388e3c; text-decoration: underline; }
  </style>
  <div class="custom-nav">
    <a href='/Home'>Home</a>
    <a href='/Risk_Assessment'>Risk Assessment</a>
    <a href='/Results'>Results</a>
    <a href='/Recommendations'>Recommendations</a>
  </div>
""", unsafe_allow_html=True)

# ── Load model ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    base = os.path.dirname(os.path.abspath(__file__))
    return joblib.load(os.path.join(base, "best_gb_model.pkl"))

model = load_model()

# ── Input Sections ─────────────────────────────────────────────────────────────
with st.expander("👤 Personal Information", expanded=True):
    age = st.number_input(
        "Age",
        min_value=18, max_value=100,
        value=, step=1, format="%d",
        help="Enter your age (years)",
        key="age"
    )
    gender = st.selectbox(
        "Gender",
        options=["Select…", "Male", "Female"],
        index=0,
        key="gender"
    )
    ever_married = st.selectbox(
        "Ever Married?",
        options=["Select…", "Yes", "No"],
        index=0,
        key="ever_married"
    )
    work_type = st.selectbox(
        "Work Type",
        options=["Select…", "Private", "Self-employed", "Govt_job", "Never_worked"],
        index=0,
        key="work_type"
    )

with st.expander("🩺 Health Information", expanded=True):
    hypertension = st.radio(
        "Do you have hypertension?",
        options=["Select…", "Yes", "No"],
        index=0,
        key="hypertension"
    )
    heart_disease = st.radio(
        "Do you have heart disease?",
        options=["Select…", "Yes", "No"],
        index=0,
        key="heart_disease"
    )
    avg_glucose_level = st.number_input(
        "Average Glucose Level (mg/dL)",
        min_value=0.0, value=0.0, step=0.1,
        help="Enter your average blood glucose",
        key="avg_glucose_level"
    )
    smoking_status = st.selectbox(
        "Smoking Status",
        options=["Select…", "never smoked", "formerly smoked", "smokes"],
        index=0,
        key="smoking_status"
    )

# ── Consent & Disclaimer ───────────────────────────────────────────────────────
st.markdown("### 📄 Consent and Disclaimer")
st.write(
    "This tool provides an estimate of stroke risk based on the information you provide. "
    "It is not a diagnostic tool and should not replace professional medical advice. "
    "By submitting, you agree to allow us to estimate your stroke risk."
)
st.checkbox(
    "✅ I agree to the terms and allow risk estimation",
    key="consent"
)

# ── Calculate & Redirect ────────────────────────────────────────────────────────
if st.button("Calculate Stroke Risk 📈"):
    # validation
    if not st.session_state.consent:
        st.error("You must agree to the terms before proceeding!")
    elif (
        st.session_state.age < 1
        or st.session_state.avg_glucose_level <= 0
        or st.session_state.gender == "Select…"
        or st.session_state.ever_married == "Select…"
        or st.session_state.work_type == "Select…"
        or st.session_state.hypertension == "Select…"
        or st.session_state.heart_disease == "Select…"
        or st.session_state.smoking_status == "Select…"
    ):
        st.error("Please complete all fields with valid values before submitting.")
    else:
        # polynomial features
        age    = st.session_state.age
        gluc   = st.session_state.avg_glucose_level
        age_sq = age ** 2
        glu_sq = gluc ** 2
        interact = age * gluc

        # encoding maps
        gender_map       = {"Male":0, "Female":1}
        married_map      = {"Yes":1, "No":0}
        work_map         = {"Private":0, "Self-employed":1, "Govt_job":2, "Never_worked":3}
        hypertension_map = {"Yes":1, "No":0}
        heart_map        = {"Yes":1, "No":0}
        smoke_map        = {"never smoked":0, "formerly smoked":1, "smokes":2}

        # build feature vector
        features = np.array([
            heart_map       [st.session_state.heart_disease],
            hypertension_map[st.session_state.hypertension],
            married_map     [st.session_state.ever_married],
            smoke_map       [st.session_state.smoking_status],
            work_map        [st.session_state.work_type],
            gender_map      [st.session_state.gender],
            age,
            gluc,
            age_sq,
            interact,
            glu_sq
        ], dtype=float).reshape(1, -1)

        # compute probability
        prob = model.predict_proba(features)[0][1]

        # save for Results.py
        st.session_state.user_data       = {
            "age": age,
            "gender": st.session_state.gender,
            "ever_married": st.session_state.ever_married,
            "work_type": st.session_state.work_type,
            "hypertension": st.session_state.hypertension,
            "heart_disease": st.session_state.heart_disease,
            "avg_glucose_level": gluc,
            "smoking_status": st.session_state.smoking_status
        }
        st.session_state.prediction_prob = prob

        # navigate to Results.py
        st.query_params = {"page": "Results"}

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
  <style>
    .custom-footer {
      background-color: rgba(76,157,112,0.6); color: white;
      padding: 30px 0; border-radius: 12px; margin-top: 40px;
      text-align: center; font-size: 14px; width: 100%;
    }
    .custom-footer a { color: white; text-decoration: none; margin: 0 15px; }
    .custom-footer a:hover { text-decoration: underline; }
  </style>
  <div class="custom-footer">
    <p>&copy; 2025 Stroke Risk Assessment Tool | All rights reserved</p>
    <p>
      <a href='/Home'>Home</a>
      <a href='/Risk_Assessment'>Risk Assessment</a>
      <a href='/Results'>Results</a>
      <a href='/Recommendations'>Recommendations</a>
    </p>
    <p style="font-size:12px; margin-top:10px;">Developed by Victoria Mends</p>
  </div>
""", unsafe_allow_html=True)
