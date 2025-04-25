import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os
import joblib
import shap

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

# ── Load trained model ─────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    pages_dir  = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(pages_dir, "best_gb_model.pkl")
    if not os.path.exists(model_path):
        st.error(f"⚠️ Model file not found at:\n`{model_path}`")
        st.stop()
    return joblib.load(model_path)

model = load_model()

# ── Display results & local contributions ─────────────────────────────────────
if "user_data" in st.session_state and "prediction_prob" in st.session_state:
    prob = st.session_state.prediction_prob  # e.g. 0.02

    st.header("🧠 Stroke Risk Probability")
    st.write(f"Based on your input data, your risk of developing stroke is **{prob*100:.2f}%**")

    if prob > 0.5:
        st.warning("⚠️ Higher Risk of Stroke Detected")
    else:
        st.success("✔️ Lower Risk of Stroke Detected")

    # ── Compute SHAP for only the eight raw inputs ───────────────────────────────
    UD = st.session_state.user_data
    X = np.array([[
        {"Yes":1,"No":0}[UD["heart_disease"]],
        {"Yes":1,"No":0}[UD["hypertension"]],
        {"Yes":1,"No":0}[UD["ever_married"]],
        {"never smoked":0,"formerly smoked":1,"smokes":2}[UD["smoking_status"]],
        {"Private":0,"Self-employed":1,"Govt_job":2,"Never_worked":3}[UD["work_type"]],
        {"Male":0,"Female":1}[UD["gender"]],
        UD["age"],
        UD["avg_glucose_level"],

        # Note: We omit the engineered features here; we're only using indices 0–7
    ]])

    @st.cache_resource
    def get_explainer(mdl):
        return shap.TreeExplainer(mdl)

    explainer  = get_explainer(model)
    shap_vals  = explainer.shap_values(X)[1][0]  # class-1 contributions
    local8     = shap_vals[:8]
    abs8       = np.abs(local8)
    total_abs  = abs8.sum()
    contrib    = abs8 / total_abs * prob

    feature_names = [
        "Heart Disease", "Hypertension", "Ever Married",
        "Smoking Status", "Work Type", "Gender",
        "Age", "Avg Glucose"
    ]

    # ── Plot contributions summing to total risk ────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(feature_names, contrib * 100)
    ax.set_ylim(0, contrib.max() * 100 * 1.15)

    for i, bar in enumerate(bars):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + contrib.max() * 100 * 0.02,
            f"{contrib[i] * 100:.2f}%",
            ha="center", va="bottom"
        )

    ax.set_ylabel("Contribution to Risk (%)", fontsize=12, weight="bold")
    ax.set_title("Your Eight-Feature Contributions (sum to your total risk)", fontsize=14, weight="bold", pad=15)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)

    # ── Recommendations button & Back link ────────────────────────────────────
    st.markdown("### 📘 Personalized Recommendations:")
    if st.button("Go to Recommendations"):
        st.switch_page("Recommendations")

    st.markdown("[🔙 Back to Risk Assessment](/Risk_Assessment)")

else:
    st.warning("No user data found. Please complete the risk assessment first.")

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






# import streamlit as st
# import matplotlib.pyplot as plt
# import numpy as np
# import os
# import joblib

# # ── Page title & layout ───────────────────────────────────────────────────────
# st.set_page_config(page_title="Stroke Risk Results", layout="wide")
# st.markdown("""
#     <style>
#         #MainMenu, footer, header {visibility: hidden;}
#         [data-testid="stSidebar"], [data-testid="collapsedControl"] {display: none;}
#     </style>
# """, unsafe_allow_html=True)

# st.title("📊 Stroke Risk Results")

# # ── Navbar ─────────────────────────────────────────────────────────────────────
# st.markdown("""
#     <style>
#         .custom-nav {
#             background-color: #e8f5e9;
#             padding: 15px 0;
#             border-radius: 10px;
#             display: flex;
#             justify-content: center;
#             gap: 60px;
#             margin-bottom: 30px;
#             font-size: 18px;
#             font-weight: 600;
#         }
#         .custom-nav a {
#             text-decoration: none;
#             color: #4C9D70;
#         }
#         .custom-nav a:hover {
#             color: #388e3c;
#             text-decoration: underline;
#         }
#     </style>
#     <div class="custom-nav">
#         <a href='/Home'>Home</a>
#         <a href='/Risk_Assessment'>Risk Assessment</a>
#         <a href='/Results'>Results</a>
#         <a href='/Recommendations'>Recommendations</a>
#     </div>
# """, unsafe_allow_html=True)

# # ── Load trained model for feature-importances ─────────────────────────────────
# @st.cache_resource
# def load_model():
#     pages_dir = os.path.dirname(os.path.abspath(__file__))
#     model_path = os.path.join(pages_dir, "best_gb_model.pkl")
#     if not os.path.exists(model_path):
#         st.error(f"⚠️ Model file not found at:\n`{model_path}`")
#         st.stop()
#     return joblib.load(model_path)

# model = load_model()

# # ── Display results ────────────────────────────────────────────────────────────
# if 'user_data' in st.session_state and 'prediction_prob' in st.session_state:
#     prediction_prob = st.session_state.prediction_prob

#     st.header("🧠 Stroke Risk Probability")
#     st.write(f"Based on your input data, your risk of developing stroke is **{prediction_prob*100:.2f}%**")

#     if prediction_prob > 0.5:
#         st.warning("⚠️ Higher Risk of Stroke Detected")
#     else:
#         st.success("✔️ Lower Risk of Stroke Detected")

#     # ── Feature contributions chart ─────────────────────────────────────────────
#     st.subheader("Understanding Your Results")
#     st.write("How each factor contributes to your overall risk:")

#     # All features and importances
#     all_features = [
#         "Heart Disease", "Hypertension", "Ever Married",
#         "Smoking Status", "Work Type", "Gender",
#         "Age", "Avg Glucose", "Age²", "Age×Glucose", "Glucose²"
#     ]
#     importances = model.feature_importances_
#     pct = importances / importances.sum() * 100

#     # Reorder to match input sequence
#     order_indices = [6, 5, 2, 4, 1, 0, 7, 3]
#     feature_names = [all_features[i] for i in order_indices]
#     importances_pct = pct[order_indices]

#     fig, ax = plt.subplots(figsize=(10, 5))
#     base_colors = plt.cm.tab20.colors
#     max_index = int(np.argmax(importances_pct))
#     bar_colors = ["red" if i == max_index else base_colors[i % len(base_colors)] for i in range(len(feature_names))]
#     bars = ax.bar(
#         feature_names,
#         importances_pct,
#         color=bar_colors
#     )

#     # Expand y-axis to fit the highest label
#     max_val = importances_pct.max()
#     ax.set_ylim(0, max_val * 1.15)

#     # Annotate each bar with percentage
#     for i, bar in enumerate(bars):
#         ax.text(
#             bar.get_x() + bar.get_width() / 2,
#             bar.get_height() + max_val * 0.02,
#             f"{importances_pct[i]:.2f}%",
#             ha="center",
#             va="bottom",
#             fontsize=11
#         )

#     ax.set_ylabel("Contribution to Risk (%)", fontsize=12, weight="bold")
#     ax.set_title("Feature Contributions to Stroke Risk Prediction", fontsize=14, weight="bold", pad=15)
#     plt.xticks(rotation=45, ha="right")
#     plt.tight_layout()
#     st.pyplot(fig)

#     # ── Recommendations button ────────────────────────────────────────────────
#     st.markdown("### 📘 Get personalized recommendations based on your results:")
#     if st.button("Click for Recommendations"):
#         st.switch_page("pages/Recommendations.py")

#     # ── Back link ─────────────────────────────────────────────────────────────
#     st.markdown("[🔙 Go back to Risk Assessment](/Risk_Assessment)")

# else:
#     st.warning("No user data found. Please complete the risk assessment first.")

# # ── Footer ────────────────────────────────────────────────────────────────────
# st.markdown("""
#     <style>
#         .custom-footer {
#             background-color: rgba(76, 157, 112, 0.6);
#             color: white;
#             padding: 30px 0;
#             border-radius: 12px;
#             margin-top: 40px;
#             text-align: center;
#             font-size: 14px;
#             width: 100%;
#         }
#         .custom-footer a {
#             color: white;
#             text-decoration: none;
#             margin: 0 15px;
#         }
#         .custom-footer a:hover {
#             text-decoration: underline;
#         }
#     </style>
#     <div class="custom-footer">
#         <p>&copy; 2025 Stroke Risk Assessment Tool | All rights reserved</p>
#         <p>
#             <a href='/Home'>Home</a>
#             <a href='/Risk_Assessment'>Risk Assessment</a>
#             <a href='/Results'>Results</a>
#             <a href='/Recommendations'>Recommendations</a>
#         </p>
#         <p style="font-size:12px; margin-top:10px;">Developed by Victoria Mends</p>
#     </div>
# """, unsafe_allow_html=True)
