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

# ── Load trained model for feature-importances ─────────────────────────────────
@st.cache_resource
def load_model():
    # __file__ is pages/Results.py
    pages_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(pages_dir, "best_gb_model.pkl")
    if not os.path.exists(model_path):
        st.error(f"⚠️ Model file not found at:\n`{model_path}`")
        st.stop()
    return joblib.load(model_path)

model = load_model()

# ── Display results ────────────────────────────────────────────────────────────
if 'user_data' in st.session_state and 'prediction_prob' in st.session_state:
    prediction_prob = st.session_state.prediction_prob

    # Updated risk message
    st.header("🧠 Stroke Risk Probability")
    st.write(f"Based on your input data, your risk of developing stroke is **{prediction_prob*100:.2f}%**")

    if prediction_prob > 0.5:
        st.warning("⚠️ Higher Risk of Stroke Detected")
    else:
        st.success("✔️ Lower Risk of Stroke Detected")

    # ── Feature contributions chart ─────────────────────────────────────────────
    st.subheader("Understanding Your Results")
    st.write("How each factor contributes to your overall risk:")

    feature_names = [
        "Heart Disease", "Hypertension", "Ever Married",
        "Smoking Status", "Work Type", "Gender",
        "Age", "Avg Glucose", "Age²", "Age×Glucose", "Glucose²"
    ]
    importances = model.feature_importances_
    importances_pct = importances / importances.sum() * 100

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = plt.cm.tab20.colors
    bars = ax.bar(feature_names,
                  importances_pct,
                  color=[colors[i % len(colors)] for i in range(len(feature_names))])

    # annotate percentages
    for i, bar in enumerate(bars):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"{importances_pct[i]:.2f}%",
            ha="center",
            va="bottom",
            fontsize=11
        )

    ax.set_ylabel("Contribution to Risk (%)", fontsize=12, weight="bold")
    ax.set_title("Feature Contributions to Stroke Risk Prediction", fontsize=14, weight="bold", pad=15)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)

    # ── Recommendations button ────────────────────────────────────────────────
    st.markdown("### 📘 Get personalized recommendations based on your results:")
    if st.button("Click for Recommendations"):
        st.switch_page("pages/Recommendations.py")

    # ── Back link ─────────────────────────────────────────────────────────────
    st.markdown("[🔙 Go back to Risk Assessment](/Risk_Assessment)")

else:
    st.warning("No user data found. Please complete the risk assessment first.")

# ── Footer ────────────────────────────────────────────────────────────────────
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
        }
        .custom-footer a {
            color: white;
            text-decoration: none;
            margin: 0 15px;
        }
        .custom-footer a:hover {
            text-decoration: underline;
        }
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
