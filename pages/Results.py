import streamlit as st
import os, joblib, numpy as np, shap, plotly.graph_objects as go

# ───────────────────────── Page config & CSS ─────────────────────────
st.set_page_config(page_title="Stroke Risk Results", layout="wide")
st.markdown("""
  <style>
    #MainMenu, footer, header{visibility:hidden;}
    [data-testid="stSidebar"],[data-testid="collapsedControl"]{display:none;}
  </style>
""", unsafe_allow_html=True)

# ───────────────────────── Title & Navbar ────────────────────────────
st.title("📊 Stroke Risk Results")
st.markdown("""
  <style>
    .custom-nav{background:#e8f5e9;padding:15px 0;border-radius:10px;
                display:flex;justify-content:center;gap:60px;margin-bottom:30px;
                font-size:18px;font-weight:600;}
    .custom-nav a{text-decoration:none;color:#4C9D70;}
    .custom-nav a:hover{color:#388e3c;text-decoration:underline;}
  </style>
  <div class="custom-nav">
    <a href='/Home'>Home</a>
    <a href='/Risk_Assessment'>Risk Assessment</a>
    <a href='/Results'>Results</a>
    <a href='/Recommendations'>Recommendations</a>
  </div>
""", unsafe_allow_html=True)

# ──────────────────────── Load model ────────────────────────────────
@st.cache_resource
def load_model():
    path = os.path.join(os.path.dirname(__file__), "best_stacking_model.pkl")
    if not os.path.exists(path):
        st.error(f"⚠️ Model file not found at `{path}`")
        st.stop()
    return joblib.load(path)

model = load_model()

# ─────────────────────── SHAP KernelExplainer ───────────────────────
@st.cache_resource
def get_explainer(_model, n_features):
    background = np.zeros((1, n_features))
    return shap.KernelExplainer(_model.predict_proba, background)

# ─────────────────────────── Main section ────────────────────────────
required_keys = {"user_data", "prediction_prob"}
if required_keys <= st.session_state.keys():
    ud       = st.session_state.user_data
    prob_raw = float(st.session_state.prediction_prob)
    pct_disp = round(prob_raw * 100, 2)

    st.header("🧠 Stroke Percentage Risk")
    st.write(f"Based on your inputs, your estimated risk is **{pct_disp:.2f}%**")
    if prob_raw > 0.5:
        st.warning("⚠️ Higher Risk of Stroke Detected")
    else:
        st.success("✔️ Lower Risk of Stroke Detected")

    # ── Build feature vector ───────────────────────────────────────────
    age, glu = ud["age"], ud["avg_glucose_level"]
    X = np.array([[
        {"Yes": 1, "No": 0}[ud["heart_disease"]],
        {"Yes": 1, "No": 0}[ud["hypertension"]],
        {"Yes": 1, "No": 0}[ud["ever_married"]],
        {"never smoked": 0, "formerly smoked": 1, "smokes": 2}[ud["smoking_status"]],
        {"Private": 0, "Self-employed": 1, "Govt_job": 2, "Never_worked": 3}[ud["work_type"]],
        {"Male": 0, "Female": 1}[ud["gender"]],
        age, glu, age**2, age * glu, glu**2
    ]])

    # ── SHAP contributions via KernelExplainer ─────────────────────────
    feature_names = ["Heart Disease", "Hypertension", "Ever Married",
                     "Smoking Status", "Work Type", "Gender", "Age", "Avg Glucose"]
    palette = ["#A52A2A", "#FFD700", "#4682B4", "#800080"]
    colors  = [palette[i % 4] for i in range(len(feature_names))]

    if pct_disp == 0.00:
        contrib = np.zeros(len(feature_names))
    else:
        explainer = get_explainer(model, X.shape[1])
        # compute SHAP values (nsamples can be tuned)
        sv = explainer.shap_values(X, nsamples=100)

        # handle both list-of-arrays and single-array outputs:
        if isinstance(sv, list) and len(sv) > 1:
            # multi-output → pick the 'stroke' class explanation
            shap_vals = sv[1][0]
        else:
            # single ndarray: first (and only) row is our sample
            shap_vals = sv[0]

        # only take the first 8 original features
        abs8    = np.abs(shap_vals[:8])
        contrib = abs8 / abs8.sum() * prob_raw

    # ── Plotly bar chart ───────────────────────────────────────────────
    fig = go.Figure(go.Bar(
        x=feature_names,
        y=contrib * 100,
        marker=dict(color=colors),
        text=[f"{v*100:.2f}%" for v in contrib],
        textposition="auto",
        hovertemplate="<b>%{x}</b><br>Contribution: %{y:.2f}%<extra></extra>"
    ))
    fig.update_layout(
        title="How Each Input Contributed to Your Total Risk",
        yaxis=dict(title="Contribution to Risk (%)", rangemode="tozero"),
        xaxis=dict(tickangle=-45),
        margin=dict(t=60, b=120)
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Navigation buttons ──────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔙 Back to Risk Assessment"):
            st.switch_page("pages/Risk_Assessment.py")
    with col2:
        if st.button("📘 Go to Recommendations"):
            st.switch_page("pages/Recommendations.py")

else:
    st.warning("No input data found. Please complete the Risk Assessment first.")

# ─────────────────────────── Footer ─────────────────────────────────
st.markdown("""
  <style>
    .custom-footer{background:rgba(76,157,112,0.6);color:white;padding:30px 0;
                   border-radius:12px;margin-top:40px;text-align:center;font-size:14px;}
    .custom-footer a{color:white;text-decoration:none;margin:0 15px;}
    .custom-footer a:hover{text-decoration:underline;}
  </style>
  <div class='custom-footer'>
    <p>&copy; 2025 Stroke Risk Assessment Tool | All rights reserved</p>
    <p>
      <a href='/Home'>Home</a><a href='/Risk_Assessment'>Risk Assessment</a>
      <a href='/Results'>Results</a><a href='/Recommendations'>Recommendations</a>
    </p>
    <p style='font-size:12px;margin-top:10px;'>Developed by Victoria Mends</p>
  </div>
""", unsafe_allow_html=True)











# import streamlit as st
# import os, joblib, shap, plotly.graph_objects as go, pandas as pd, numpy as np
# # ensures engineer_feats is importable

# # ----- place these THREE lines at the *very top* of the page -------------
# import feutils, __main__
# if not hasattr(__main__, "engineer_feats"):
#     setattr(__main__, "engineer_feats", feutils.engineer_feats)
# # -------------------------------------------------------------------------


# # ───────────────────────── Page config & CSS ─────────────────────────
# st.set_page_config(page_title="Stroke Risk Results", layout="wide")
# st.markdown("""
#   <style>
#     #MainMenu, footer, header{visibility:hidden;}
#     [data-testid="stSidebar"],[data-testid="collapsedControl"]{display:none;}
#   </style>""", unsafe_allow_html=True)

# # ───────────────────────── Title & Navbar ────────────────────────────
# st.title("📊 Stroke Risk Results")
# st.markdown("""
#   <style>
#     .custom-nav{background:#e8f5e9;padding:15px 0;border-radius:10px;
#                 display:flex;justify-content:center;gap:60px;margin-bottom:30px;
#                 font-size:18px;font-weight:600;}
#     .custom-nav a{text-decoration:none;color:#4C9D70;}
#     .custom-nav a:hover{color:#388e3c;text-decoration:underline;}
#   </style>
#   <div class="custom-nav">
#     <a href='/Home'>Home</a><a href='/Risk_Assessment'>Risk Assessment</a>
#     <a href='/Results'>Results</a><a href='/Recommendations'>Recommendations</a>
#   </div>""", unsafe_allow_html=True)

# # ─────────────────────── Load pipeline & explainer ──────────────────
# @st.cache_resource
# def load_pipeline():
#     import feutils, __main__
#     setattr(__main__, "engineer_feats", feutils.engineer_feats)

#     path = os.path.join(os.path.dirname(__file__), "stroke_stacking_pipeline.pkl")
#     return joblib.load(path)


# model = load_pipeline()

# @st.cache_resource
# def get_explainer(_m):
#     """Use TreeExplainer if possible; else fall back to permutation."""
#     try:
#         return shap.TreeExplainer(_m)
#     except shap.utils._exceptions.InvalidModelError:
#         return shap.Explainer(_m, algorithm="permutation")

# explainer = get_explainer(model)

# # ─────────────────────────── Main section ───────────────────────────
# if {"user_data", "prediction_prob"} <= st.session_state.keys():
#     ud        = st.session_state.user_data
#     prob_raw  = float(st.session_state.prediction_prob)
#     pct_disp  = round(prob_raw * 100, 2)

#     st.header("🧠 Stroke Percentage Risk")
#     st.write(f"Based on your inputs, your estimated risk is **{pct_disp:.2f}%**")
#     st.warning("⚠️ Higher Risk of Stroke Detected") if prob_raw > 0.5 else \
#         st.success("✔️ Lower Risk of Stroke Detected")

#     X_df = pd.DataFrame([ud])

#     # ── SHAP contributions ─────────────────────────────────────────
#     shap_vals  = explainer(X_df)
#     base_names = list(ud.keys())          # 8 original fields
#     palette    = ["#A52A2A","#FFD700","#4682B4","#800080"]
#     colors     = [palette[i % 4] for i in range(len(base_names))]

#     if pct_disp == 0:
#         contrib = np.zeros(len(base_names))
#     else:
#         raw     = shap_vals.values[0][:len(base_names)]
#         contrib = np.abs(raw) / np.abs(raw).sum() * prob_raw

#     fig = go.Figure(go.Bar(
#         x=base_names,
#         y=contrib * 100,
#         marker=dict(color=colors),
#         text=[f"{v*100:.2f}%" for v in contrib],
#         textposition="auto",
#         hovertemplate="<b>%{x}</b><br>Contribution: %{y:.2f}%<extra></extra>"
#     ))
#     fig.update_layout(
#         title="How Each Input Contributed to Your Total Risk",
#         yaxis=dict(title="Contribution to Risk (%)", rangemode="tozero"),
#         xaxis=dict(tickangle=-45),
#         margin=dict(t=60, b=120)
#     )
#     st.plotly_chart(fig, use_container_width=True)

#     # Navigation buttons
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("🔙 Back to Risk Assessment"):
#             st.switch_page("pages/Risk_Assessment.py")
#     with col2:
#         if st.button("📘 Go to Recommendations"):
#             st.switch_page("pages/Recommendations.py")
# else:
#     st.warning("No input data found. Please complete the Risk Assessment first.")

# # ─────────────────────────── Footer ────────────────────────────────
# st.markdown("""
#   <style>
#     .custom-footer{background:rgba(76,157,112,0.6);color:white;padding:30px 0;
#                    border-radius:12px;margin-top:40px;text-align:center;font-size:14px;}
#     .custom-footer a{color:white;text-decoration:none;margin:0 15px;}
#     .custom-footer a:hover{text-decoration:underline;}
#   </style>
#   <div class='custom-footer'>
#     <p>&copy; 2025 Stroke Risk Assessment Tool | All rights reserved</p>
#     <p>
#       <a href='/Home'>Home</a><a href='/Risk_Assessment'>Risk Assessment</a>
#       <a href='/Results'>Results</a><a href='/Recommendations'>Recommendations</a>
#     </p>
#     <p style='font-size:12px;margin-top:10px;'>Developed by Victoria Mends</p>
#   </div>""", unsafe_allow_html=True)





# import streamlit as st
# import os, joblib, numpy as np, shap, plotly.graph_objects as go

# # ───────────────────────── Page config & CSS ─────────────────────────
# _ = st.set_page_config(page_title="Stroke Risk Results", layout="wide")
# _ = st.markdown("""
#   <style>
#     #MainMenu, footer, header{visibility:hidden;}
#     [data-testid="stSidebar"],[data-testid="collapsedControl"]{display:none;}
#   </style>
# """, unsafe_allow_html=True)

# # ───────────────────────── Title & Navbar ────────────────────────────
# _ = st.title("📊 Stroke Risk Results")
# _ = st.markdown("""
#   <style>
#     .custom-nav{background:#e8f5e9;padding:15px 0;border-radius:10px;
#                 display:flex;justify-content:center;gap:60px;margin-bottom:30px;
#                 font-size:18px;font-weight:600;}
#     .custom-nav a{text-decoration:none;color:#4C9D70;}
#     .custom-nav a:hover{color:#388e3c;text-decoration:underline;}
#   </style>
#   <div class="custom-nav">
#     <a href='/Home'>Home</a>
#     <a href='/Risk_Assessment'>Risk Assessment</a>
#     <a href='/Results'>Results</a>
#     <a href='/Recommendations'>Recommendations</a>
#   </div>
# """, unsafe_allow_html=True)

# # ──────────────────────── Load model & SHAP explainer ─────────────────────
# @st.cache_resource
# def load_model():
#     path = os.path.join(os.path.dirname(__file__), "best_stacking_model.pkl")
#     if not os.path.exists(path):
#         st.error(f"⚠️ Model file not found at `{path}`"); st.stop()
#     return joblib.load(path)

# model = load_model()

# @st.cache_resource
# def get_explainer(_model):     # leading underscore → skip hashing
#     return shap.TreeExplainer(_model)

# explainer = get_explainer(model)

# # ─────────────────────────── Main section ────────────────────────────
# required_keys = {"user_data", "prediction_prob"}
# if required_keys <= st.session_state.keys():
#     ud        = st.session_state.user_data
#     prob_raw  = float(st.session_state.prediction_prob)     # already computed in previous page
#     pct_disp  = round(prob_raw * 100, 2)                    # two-decimal %

#     _ = st.header("🧠 Stroke Percentage Risk")
#     _ = st.write(f"Based on your inputs, your estimated risk is **{pct_disp:.2f}%**")
#     _ = st.warning("⚠️ Higher Risk of Stroke Detected") if prob_raw > 0.5 else \
#         st.success("✔️ Lower Risk of Stroke Detected")

#     # ── Build feature vector for SHAP (same order as training) ────────────
#     age, glu = ud["age"], ud["avg_glucose_level"]
#     X = np.array([[
#         {"Yes": 1, "No": 0}[ud["heart_disease"]],
#         {"Yes": 1, "No": 0}[ud["hypertension"]],
#         {"Yes": 1, "No": 0}[ud["ever_married"]],
#         {"never smoked": 0, "formerly smoked": 1, "smokes": 2}[ud["smoking_status"]],
#         {"Private": 0, "Self-employed": 1, "Govt_job": 2, "Never_worked": 3}[ud["work_type"]],
#         {"Male": 0, "Female": 1}[ud["gender"]],
#         age, glu, age**2, age * glu, glu**2
#     ]])

#     # ── SHAP contributions ───────────────────────────────────────────────
#     feature_names = ["Heart Disease", "Hypertension", "Ever Married",
#                      "Smoking Status", "Work Type", "Gender", "Age", "Avg Glucose"]
#     palette = ["#A52A2A", "#FFD700", "#4682B4", "#800080"]   # brown, gold, steel-blue, purple
#     colors  = [palette[i % 4] for i in range(8)]

#     if pct_disp == 0.00:                                    # flatten bars if rounded 0 %
#         contrib = np.zeros(len(feature_names))
#     else:
#         sv         = explainer.shap_values(X)
#         shap_vals  = sv[1][0] if isinstance(sv, list) else sv[0]
#         abs8       = np.abs(shap_vals[:8])
#         contrib    = abs8 / abs8.sum() * prob_raw

#     # ── Plotly bar chart ─────────────────────────────────────────────────
#     fig = go.Figure(go.Bar(
#         x=feature_names,
#         y=contrib * 100,
#         marker=dict(color=colors),
#         text=[f"{v*100:.2f}%" for v in contrib],
#         textposition="auto",
#         hovertemplate="<b>%{x}</b><br>Contribution: %{y:.2f}%<extra></extra>"
#     ))
#     fig.update_layout(
#         title="How Each Input Contributed to Your Total Risk",
#         yaxis=dict(title="Contribution to Risk (%)", rangemode="tozero"),
#         xaxis=dict(tickangle=-45),
#         margin=dict(t=60, b=120)
#     )
#     _ = st.plotly_chart(fig, use_container_width=True)

#     # ── Navigation buttons ──────────────────────────────────────────────
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("🔙 Back to Risk Assessment"):
#             st.switch_page("pages/Risk_Assessment.py")
#     with col2:
#         if st.button("📘 Go to Recommendations"):
#             st.switch_page("pages/Recommendations.py")
# else:
#     _ = st.warning("No input data found. Please complete the Risk Assessment first.")

# # ─────────────────────────── Footer ────────────────────────────────
# _ = st.markdown("""
#   <style>
#     .custom-footer{background:rgba(76,157,112,0.6);color:white;padding:30px 0;
#                    border-radius:12px;margin-top:40px;text-align:center;font-size:14px;}
#     .custom-footer a{color:white;text-decoration:none;margin:0 15px;}
#     .custom-footer a:hover{text-decoration:underline;}
#   </style>
#   <div class='custom-footer'>
#     <p>&copy; 2025 Stroke Risk Assessment Tool | All rights reserved</p>
#     <p>
#       <a href='/Home'>Home</a><a href='/Risk_Assessment'>Risk Assessment</a>
#       <a href='/Results'>Results</a><a href='/Recommendations'>Recommendations</a>
#     </p>
#     <p style='font-size:12px;margin-top:10px;'>Developed by Victoria Mends</p>
#   </div>
# """, unsafe_allow_html=True)






