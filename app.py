import streamlit as st
import base64

st.set_page_config(page_title="Stroke Predictor", layout="wide")

# Background Image
with open("stroke_bg.jpg", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

st.markdown(
    f"""
    <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        footer {{visibility: visible;}}
        footer:after {{
            content:'© 2024 Stroke Prevention AI. All rights reserved.';
            display: block;
            position: relative;
            color: white;
            padding: 10px;
            text-align: center;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Centered Wide Text
st.markdown("""
    <div style='text-align: center; padding: 40px 0; width: 100%;'>
        <h1 style='font-size: 48px; margin-bottom: 10px;'>Early Detection Saves Lives</h1>
        <p style='font-size: 20px; color: #f0f0f0;'>Explore stroke prevention strategies with our intelligent tool</p>
    </div>
""", unsafe_allow_html=True)

# Navigation Buttons
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.page_link("pages/1_🧠_Predict_Stroke.py", label="🧠 Predict Stroke", icon="🧠")
with col2:
    st.page_link("pages/2_📊_Visualization.py", label="📊 Visualization", icon="📊")
with col3:
    st.page_link("pages/3_📁_Upload_Data.py", label="📁 Upload Data", icon="📁")
