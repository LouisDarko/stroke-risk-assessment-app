import streamlit as st
import os
import joblib
import numpy as np
import shap
import plotly.graph_objects as go

# ── Page config & hide defaults ────────────────────────────────────────────────
st.set_page_config(page_title="Stroke Risk Results", layout="wide")
st.markdown("""
    <style>
      #MainMenu, footer, header {visibility: hidden;}
      [data-testid="stSidebar"], [data-testid="collapsedControl"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# ── Title & Navbar ─────────────────────────────────────────────────────────────
st.title("📊 Stroke Risk Results")
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

# ── Load trained model ─────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    base = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base, "best_gb_model.pkl")
    if not os.path.exists(model_path):
        st.error(f"⚠️ Model file not found at:\n`{model_path}`")
        st.stop()
    return joblib.load(model_path)

model = load_model()

# ── Compute SHAP explainer once ────────────────────────────────────────────────
@st.cache_resource
def get_explainer(_mdl):
    return shap.TreeExplainer(_mdl)

explainer = get_explainer(model)

# ── Display results & SHAP-based contributions ─────────────────────────────────
if "user_data" in st.session_state and "prediction_prob" in st.session_state:
    prob = st.session_state.prediction_prob

    st.header("🧠 Stroke Percentage Risk")
    st.write(f"Based on your inputs, your estimated risk is **{prob*100:.2f}%**")

    if prob > 0.5:
        st.warning("⚠️ Higher Risk of Stroke Detected")
    else:
        st.success("✔️ Lower Risk of Stroke Detected")

    # Only plot contributions when risk > 0
    if prob == 0:
        st.info("Your predicted risk is 0%; there are no feature contributions to display.")
    else:
        # Reconstruct the full 11-feature input
        UD = st.session_state.user_data
        age = UD["age"]
        glu = UD["avg_glucose_level"]
        age_sq = age ** 2
        interaction = age * glu
        glu_sq = glu ** 2

        full_X = np.array([[
            {"Yes":1,"No":0}[UD["heart_disease"]],
            {"Yes":1,"No":0}[UD["hypertension"]],
            {"Yes":1,"No":0}[UD["ever_married"]],
            {"never smoked":0,"formerly smoked":1,"smokes":2}[UD["smoking_status"]],
            {"Private":0,"Self-employed":1,"Govt_job":2,"Never_worked":3}[UD["work_type"]],
            {"Male":0,"Female":1}[UD["gender"]],
            age, glu, age_sq, interaction, glu_sq
        ]])

        sv = explainer.shap_values(full_X)
        if isinstance(sv, list):
            shap_vals_full = sv[1][0]
        else:
            shap_vals_full = sv[0]

        raw8 = shap_vals_full[:8]
        abs8 = np.abs(raw8)
        contrib = abs8 / abs8.sum() * prob

        feature_names = [
            "Heart Disease", "Hypertension", "Ever Married",
            "Smoking Status", "Work Type", "Gender",
            "Age", "Avg Glucose"
        ]

        # Determine colors: tallest bar red, others from default palette
        default_colors = [
            "#636EFA", "#00CC96", "#AB63FA", "#FFA15A",
            "#19D3F3", "#FF6692", "#B6E880", "#FF97FF"
        ]
        top_idx = int(np.argmax(contrib))
        colors = ["red" if i == top_idx else default_colors[i % len(default_colors)]
                  for i in range(len(feature_names))]

        # Interactive Plotly bar chart
        fig = go.Figure(
            go.Bar(
                x=feature_names,
                y=contrib * 100,
                marker=dict(color=colors),
                text=[f"{v*100:.2f}%" for v in contrib],
                textposition="auto",
                hovertemplate="<b>%{x}</b><br>Contribution: %{y:.2f}%<extra></extra>"
            )
        )
        fig.update_layout(
            title="How Each Input Contributed to Your Total Risk",
            yaxis=dict(title="Contribution to Risk (%)"),
            xaxis=dict(tickangle=-45),
            margin=dict(t=60, b=120)
        )
        st.plotly_chart(fig, use_container_width=True)

    # Navigation Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔙 Back to Risk Assessment"):
            st.switch_page("pages/Risk_Assessment.py")
    with col2:
        if st.button("📘 Go to Recommendations"):
            st.switch_page("pages/Recommendations.py")

else:
    st.warning("No input data found. Please complete the Risk Assessment first.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
  <style>
    .custom-footer { background-color: rgba(76,157,112,0.6); color: white;
      padding: 30px 0; border-radius: 12px; margin-top: 40px;
      text-align: center; font-size: 14px; width: 100%; }
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
