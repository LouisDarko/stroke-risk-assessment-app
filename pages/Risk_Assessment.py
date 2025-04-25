import streamlit as st
import joblib
import numpy as np
import os

# ── Page config & styling ─────────────────────────────────────────────────────
st.set_page_config(page_title="Stroke Risk Assessment", layout="wide")
st.markdown("""
<style>
  #MainMenu, footer, header {visibility: hidden;}
  [data-testid="stSidebar"], [data-testid="collapsedControl"] {display: none;}
</style>
""", unsafe_allow_html=True)

st.title("📝 Stroke Risk Assessment")

# ── Navbar ────────────────────────────────────────────────────────────────────
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
    root_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(root_dir, "best_gb_model.pkl")
    if not os.path.exists(model_path):
        st.error(f"⚠️ Cannot load model at {model_path}")
        st.stop()
    return joblib.load(model_path)

model = load_model()

# ── Personal Information ─────────────────────────────────────────────────────
with st.expander("👤 Personal Information", expanded=True):
    age = st.number_input("Age", min_value=18, max_value=100, step=1, key="age")
    gender = st.selectbox(
        "Gender", [None, "Male", "Female"], index=0,
        format_func=lambda x: "Select Gender" if x is None else x,
        key="gender"
    )
    ever_married = st.selectbox(
        "Ever Married?", [None, "Yes", "No"], index=0,
        format_func=lambda x: "Select Marital Status" if x is None else x,
        key="ever_married"
    )
    work_type = st.selectbox(
        "Work Type", [None, "Private", "Self-employed", "Govt_job", "Never_worked"], index=0,
        format_func=lambda x: "Select Work Type" if x is None else x,
        key="work_type"
    )

# ── Health Information ────────────────────────────────────────────────────────
with st.expander("🩺 Health Information", expanded=True):
    hypertension = st.radio(
        "Hypertension?", [None, "Yes", "No"], index=0,
        format_func=lambda x: "Select Hypertension Status" if x is None else x,
        key="hypertension"
    )
    heart_disease = st.radio(
        "Heart Disease?", [None, "Yes", "No"], index=0,
        format_func=lambda x: "Select Heart Disease Status" if x is None else x,
        key="heart_disease"
    )
    avg_glucose = st.number_input("Average Glucose Level (mg/dL)", min_value=55.0, step=0.1, key="avg_glucose_level")
    smoking_status = st.selectbox(
        "Smoking Status", [None, "never smoked", "formerly smoked", "smokes"], index=0,
        format_func=lambda x: "Select Smoking Status" if x is None else x,
        key="smoking_status"
    )

# ── Consent ───────────────────────────────────────────────────────────────────
st.markdown("### 📄 Consent and Disclaimer")
consent = st.checkbox("I agree to have my data used for stroke risk estimation.", key="consent")

# ── Calculate & Navigate ──────────────────────────────────────────────────────
if st.button("Calculate Stroke Risk 📈"):
    # Validation checks
    missing = []
    if not consent:
        st.error("You must agree to the terms before proceeding.")
        st.stop()
    for field, value in [
        ("Gender", gender), ("Marital Status", ever_married), ("Work Type", work_type),
        ("Hypertension", hypertension), ("Heart Disease", heart_disease), ("Smoking Status", smoking_status)
    ]:
        if value is None:
            missing.append(field)
    if missing or age < 18 or avg_glucose <= 0:
        st.error(f"Please complete all fields: {', '.join(missing)} and ensure age ≥ 18, glucose > 0.")
    else:
        # Feature engineering
        age_sq = age ** 2
        glu_sq = avg_glucose ** 2
        interaction = age * avg_glucose

        # Encodings
        gender_map  = {"Male":0, "Female":1}
        married_map = {"Yes":1, "No":0}
        work_map    = {"Private":0, "Self-employed":1, "Govt_job":2, "Never_worked":3}
        htn_map     = {"Yes":1, "No":0}
        heart_map   = {"Yes":1, "No":0}
        smoke_map   = {"never smoked":0, "formerly smoked":1, "smokes":2}

        features = np.array([
            heart_map[heart_disease], htn_map[hypertension], married_map[ever_married],
            smoke_map[smoking_status], work_map[work_type], gender_map[gender],
            age, avg_glucose, age_sq, interaction, glu_sq
        ], dtype=float).reshape(1, -1)

        prob = model.predict_proba(features)[0][1]

        # Persist to session
        st.session_state.user_data = {
            "age": age,
            "gender": gender,
            "ever_married": ever_married,
            "work_type": work_type,
            "hypertension": hypertension,
            "heart_disease": heart_disease,
            "avg_glucose_level": avg_glucose,
            "smoking_status": smoking_status
        }
        st.session_state.prediction_prob = prob

        # Navigate
        st.switch_page("pages/Results.py")

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
