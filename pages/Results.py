import streamlit as st
import os
import joblib
import matplotlib.pyplot as plt
import numpy as np

# ── Page config & hide defaults ────────────────────────────────────────────────
st.set_page_config(page_title="Results", layout="wide")
st.markdown("""
    <style>
      #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ── Navbar ─────────────────────────────────────────────────────────────────────
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

# ── Load the trained model ─────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    # model file sits one level up from this pages/ folder
    base = os.path.dirname(os.path.abspath(__file__))
    return joblib.load(os.path.join(os.path.dirname(base), "best_gb_model.pkl"))

model = load_model()

# ── Retrieve & display your risk % ─────────────────────────────────────────────
prob = st.session_state.get("prediction_prob", None)
if prob is None:
    st.error("No prediction found. Please complete the risk assessment first.")
    st.stop()

st.markdown(
    f"### Based on your input data, your risk of developing stroke is **{prob * 100:.2f}%**"
)

# ── Build & plot feature‐importance (%) ────────────────────────────────────────
feature_names = [
    "Heart Disease", "Hypertension", "Ever Married", "Smoking Status",
    "Work Type", "Gender", "Age", "Avg Glucose", "Age²", "Age×Glucose", "Glucose²"
]
# global importances from your gradient‐boost model
importances = model.feature_importances_
# convert to percentages
importances_pct = importances / importances.sum() * 100

fig, ax = plt.subplots()
bars = ax.bar(feature_names, importances_pct)
# give each bar its own color
colors = plt.cm.tab20.colors
for i, bar in enumerate(bars):
    bar.set_color(colors[i % len(colors)])
# annotate with “xx.xx%”
for i, v in enumerate(importances_pct):
    ax.text(i, v + 0.5, f"{v:.2f}%", ha="center", va="bottom")
ax.set_ylabel("Contribution to Risk (%)")
ax.set_title("Feature Contributions to Stroke Risk Prediction")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot(fig)

# ── Recommendations button ────────────────────────────────────────────────────
if st.button("Click for recommendations"):
    # must use the relative path from root
    st.switch_page("pages/Recommendations.py")
