import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os
import joblib

# ── Page title & layout ───────────────────────────────────────────────────────
st.set_page_config(page_title="Stroke Risk Results", layout="wide")
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        [data-testid="stSidebar"], [data-testid="collapsedControl"] {display: none;}
    </style>
""", unsafe_allow_html=True)

st.title("📊 Stroke Risk Results")

# ── Navbar ─────────────────────────────────────────────────────────────────────
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
        <a href='/Home'>Home</a>
        <a href='/Risk_Assessment'>Risk Assessment</a>
        <a href='/Results'>Results</a>
        <a href='/Recommendations'>Recommendations</a>
    </div>
""", unsafe_allow_html=True)

# ── Load trained model ────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    pages_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(pages_dir, "best_gb_model.pkl")
    if not os.path.exists(model_path):
        st.error(f"⚠️ Model file not found at: {model_path}")
        st.stop()
    return joblib.load(model_path)

model = load_model()

# ── Retrieve prediction ───────────────────────────────────────────────────────
if 'prediction_prob' not in st.session_state:
    st.error("⚠️ No stroke risk score found. Please complete the assessment first.")
    st.page_link("pages/Risk_Assessment.py", label="Go to Risk Assessment")
    st.stop()

prob = st.session_state.prediction_prob
risk_score = prob * 100

st.header("🧠 Stroke Risk Probability")
st.write(f"Based on your input data, your risk of developing stroke is **{risk_score:.2f}%**")
if prob > 0.5:
    st.warning("⚠️ Higher Risk of Stroke Detected")
else:
    st.success("✔️ Lower Risk of Stroke Detected")

# ── Feature contributions ─────────────────────────────────────────────────────
st.subheader("Understanding Your Results")
st.write("How much each factor contributed to your overall risk (bars sum to your risk):")

# Base features and importances
# Indices correspond to: [0:Heart Disease,1:Hypertension,2:Ever Married,3:Smoking Status,4:Work Type,5:Gender,6:Age,7:Avg Glucose]
importances = model.feature_importances_
# Absolute contribution: importance × risk probability × 100
abs_contrib = importances[:8] * prob * 100

# Order to match input sequence: Age, Gender, Ever Married, Work Type, Hypertension, Heart Disease, Avg Glucose, Smoking Status
order = [6,5,2,4,1,0,7,3]
feature_names = ["Age","Gender","Ever Married","Work Type","Hypertension","Heart Disease","Avg Glucose","Smoking Status"]
contrib_values = abs_contrib[order]

# Plot
fig, ax = plt.subplots(figsize=(10,5))
# Highlight the highest contributor in red
max_idx = int(np.argmax(contrib_values))
base_colors = plt.cm.tab20.colors
bar_colors = ["red" if i==max_idx else base_colors[i % len(base_colors)] for i in range(len(feature_names))]
bars = ax.bar(feature_names, contrib_values, color=bar_colors)

# Expand y-axis so labels fit
top = contrib_values.max() * 1.15
ax.set_ylim(0, top)

# Annotate each bar with its contribution
for i, bar in enumerate(bars):
    ax.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height() + top*0.01,
        f"{contrib_values[i]:.2f}%",
        ha="center", va="bottom",
        fontsize=11
    )

ax.set_ylabel("Contribution to Risk (%)", fontsize=12, weight="bold")
ax.set_title("Feature Contributions to Stroke Risk Prediction", fontsize=14, weight="bold")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot(fig)

# ── Recommendations button ───────────────────────────────────────────────────
st.markdown("### 🎯 Personalized Recommendations")
if st.button("Click for Recommendations"):
    st.switch_page("pages/Recommendations.py")

# ── Back link ─────────────────────────────────────────────────────────────────
st.markdown("[🔙 Go back to Risk Assessment](/Risk_Assessment)")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
    <style>
        .custom-footer {
            background-color: rgba(76,157,112,0.6);
            color: white;
            padding: 30px 0;
            border-radius: 12px;
            margin-top: 40px;
            text-align: center;
            font-size: 14px;
            width: 100%;
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
