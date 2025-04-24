import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os

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

# ── Display results ────────────────────────────────────────────────────────────
if 'user_data' in st.session_state and 'prediction_prob' in st.session_state:
    user_data       = st.session_state.user_data
    prediction_prob = st.session_state.prediction_prob

    st.header("🧠 Stroke Risk Probability")
    st.write(f"Based on your input data, your stroke risk probability is: **{prediction_prob*100:.2f}%**")
    if prediction_prob > 0.5:
        st.warning("⚠️ Higher Risk of Stroke Detected")
    else:
        st.success("✔️ Lower Risk of Stroke Detected")

    # ── Beautiful Bar Chart ────────────────────────────────────────────────────
    st.subheader("Understanding Your Results")
    st.write("How each factor contributes to your overall risk:")

    # build risk_data dict
    smoke_map = {"never smoked":0, "formerly smoked":1, "smokes":2, "Unknown":3}
    risk_data = {
        'Age': user_data['age'],
        'Hypertension': 1 if user_data['hypertension']=="Yes" else 0,
        'Heart Disease': 1 if user_data['heart_disease']=="Yes" else 0,
        'Average Glucose': user_data['avg_glucose_level'],
        'Smoking Status': smoke_map.get(user_data['smoking_status'], 0)
    }

    labels = list(risk_data.keys())
    values = list(risk_data.values())

    # pastel colormap
    cmap = plt.get_cmap("Pastel1")
    colors = cmap(np.linspace(0, 1, len(labels)))

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#f9f9f9")
    ax.set_facecolor("#f9f9f9")

    bars = ax.bar(labels, values, color=colors, edgecolor="white", linewidth=0.8)
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    ax.set_ylabel("Score", fontsize=12, weight="bold")
    ax.set_title("Your Health Factor Scores", fontsize=14, weight="bold", pad=15)
    plt.xticks(rotation=30, ha="right", fontsize=11)

    # annotate bar values
    for bar in bars:
        y = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            y + max(values)*0.02,
            f"{y:.1f}",
            ha="center",
            va="bottom",
            fontsize=11
        )

    st.pyplot(fig)

    # ── Recommendations button ────────────────────────────────────────────────
    st.markdown("### 📘 Get personalized recommendations based on your results:")
    if st.button("Click for Recommendations"):
        st.query_params = {"page": "Recommendations"}

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
