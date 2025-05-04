import streamlit as st
import os, joblib, numpy as np, shap, plotly.graph_objects as go

# ───────────────────────── Page config & CSS ─────────────────────────
st.set_page_config(page_title="Stroke Risk Results", layout="wide")
st.markdown("""
  <style>
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid=\"stSidebar\"], [data-testid=\"collapsedControl\"] { display: none; }
  </style>
""", unsafe_allow_html=True)

# ───────────────────────── Title & Navbar ────────────────────────────
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

# ─────────────────── Load preprocessing and model ─────────────────────
@st.cache_resource
def load_preprocessor():
    import glob
    base = os.path.dirname(__file__)
    # Try full pipeline (dynamic search)
    pipeline_files = glob.glob(os.path.join(base, "*pipeline*.pkl"))
    for path in pipeline_files:
        try:
            pipeline = joblib.load(path)
            return pipeline, True
        except Exception:
            continue
    # Fallback: dynamic model and scaler
    scaler_files = glob.glob(os.path.join(base, "*scaler*.pkl"))
    model_files  = glob.glob(os.path.join(base, "*stacking*.pkl"))
    if scaler_files and model_files:
        scaler = joblib.load(scaler_files[0])
        model  = joblib.load(model_files[0])
        return (scaler, model), False
    st.error("⚠️ Could not find a preprocessing pipeline or scaler + model files in the app directory.
" \
             + "Please upload a pipeline (*.pkl containing scaler+model) or both scaler and stacking model pickle files.")
    st.stop()

preproc, is_pipeline = load_preprocessor()

# ─────────────────── SHAP Explainer Setup ─────────────────────
@st.cache_resource
def get_explainer(model_obj, background):
    return shap.KernelExplainer(model_obj.predict_proba, background)

# ─────────────────────────── Main ────────────────────────────
if "user_data" in st.session_state:
    ud = st.session_state.user_data
    # Raw feature vector in training order
    raw = np.array([[
        {"Yes":1, "No":0}[ud["heart_disease"]],
        {"Yes":1, "No":0}[ud["hypertension"]],
        {"Yes":1, "No":0}[ud["ever_married"]],
        {"never smoked":0, "formerly smoked":1, "smokes":2}[ud["smoking_status"]],
        {"Private":0, "Self-employed":1, "Govt_job":2, "Never_worked":3}[ud["work_type"]],
        {"Male":0, "Female":1}[ud["gender"]],
        ud["age"], ud["avg_glucose_level"],
        ud["age"]**2,
        ud["age"] * ud["avg_glucose_level"],
        ud["avg_glucose_level"]**2
    ]], dtype=float)

    # Apply preprocessing
    if is_pipeline:
        pipeline = preproc
        features = raw
        probs = pipeline.predict_proba(features)[0]
        prediction = pipeline.predict(features)[0]
        classes = pipeline.classes_
        background = raw
    else:
        scaler, model = preproc
        features = scaler.transform(raw)
        probs = model.predict_proba(features)[0]
        prediction = model.predict(features)[0]
        classes = model.classes_
        background = features

    # Extract positive-class probability
    pos_idx = list(classes).index(1)
    prob = probs[pos_idx]

    # Display risk message
    if prediction == 1:
        st.error(f"⚠️ High risk of stroke.\n\n**Probability:** {prob:.2%}")
    else:
        st.success(f"✅ Low risk of stroke.\n\n**Probability:** {prob:.2%}")

    # SHAP explanation
    explainer = get_explainer(preproc if is_pipeline else model, background)
    sv = explainer.shap_values(features if not is_pipeline else raw, nsamples=100)
    shap_vals = np.array(sv[1] if isinstance(sv, list) else sv).reshape(-1)

    # Relative contributions (sum to 100%)
    abs_vals = np.abs(shap_vals[:8])
    rel_pct = abs_vals / abs_vals.sum() * 100
    y_vals = rel_pct.tolist()

    # Plot feature contributions
    feature_names = [
        "Heart Disease","Hypertension","Ever Married",
        "Smoking Status","Work Type","Gender",
        "Age","Avg Glucose"
    ]
    colors = ["brown","gold","steelblue","purple"]
    fig_bar = go.Figure(go.Bar(
        x=feature_names, y=y_vals,
        marker=dict(color=[colors[i%4] for i in range(len(feature_names))]),
        text=[f"{v:.1f}%" for v in y_vals], textposition="auto",
        hovertemplate="<b>%{x}</b><br>Contribution: %{y:.1f}%<extra></extra>"
    ))
    fig_bar.update_layout(
        title="Relative Feature Contributions to Stroke Risk",
        yaxis_title="Contribution (%)",
        xaxis_tickangle=-45,
        margin=dict(t=60, b=120)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Gauge chart for overall risk
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number", value=prob*100,
        title={'text':"Overall Stroke Risk (%)"},
        gauge={
            'axis':{'range':[0,100]}, 'bar':{'color':'steelblue'},
            'steps':[{'range':[0,50],'color':'lightgreen'},{'range':[50,100],'color':'lightcoral'}],
            'threshold':{'line':{'color':'red','width':4},'value':50}
        }
    ))
    fig_gauge.update_layout(margin=dict(t=50, b=0, l=0, r=0))
    st.plotly_chart(fig_gauge, use_container_width=True)

    # Navigation
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔙 Back to Risk Assessment"): st.switch_page("pages/Risk_Assessment.py")
    with c2:
        if st.button("📘 Go to Recommendations"): st.switch_page("pages/Recommendations.py")
else:
    st.warning("Please complete the Risk Assessment first.")

# Footer
st.markdown("""
  <style>
    .custom-footer { background: rgba(76,157,112,0.6); color: white; padding: 30px 0;
                     border-radius: 12px; margin-top: 40px; text-align: center; font-size: 14px; }
    .custom-footer a { color: white; text-decoration: none; margin: 0 15px; }
    .custom-footer a:hover { text-decoration: underline; }
  </style>
  <div class='custom-footer'>
    <p>&copy; 2025 Stroke Risk Assessment Tool | All rights reserved</p>
    <p>
      <a href='/Home'>Home</a>
      <a href='/Risk_Assessment'>Risk Assessment</a>
      <a href='/Results'>Results</a>
      <a href='/Recommendations'>Recommendations</a>
    </p>
    <p style='font-size:12px; margin-top:10px;'>Developed by Victoria Mends</p>
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






