import streamlit as st
import pandas as pd

st.title("🧾 Stroke Risk Form")

with st.form("user_data_form"):
    age = st.number_input("Enter your Age", min_value=1, max_value=120, value=25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    hypertension = st.selectbox("Do you have hypertension?", ["Yes", "No"])
    heart_disease = st.selectbox("Do you have heart disease?", ["Yes", "No"])
    ever_married = st.selectbox("Have you ever been married?", ["Yes", "No"])
    work_type = st.selectbox("Work Type", ["Private", "Self-employed", "Govt Job", "Children", "Never worked"])
    smoking_status = st.selectbox("Smoking Status", ["Never smoked", "Formerly smoked", "Smokes"])
    bmi = st.number_input("Enter your BMI", min_value=10.0, max_value=60.0, value=22.0)

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.session_state.user_data = {
            "age": age, "gender": gender, "hypertension": hypertension,
            "heart_disease": heart_disease, "ever_married": ever_married,
            "work_type": work_type, "smoking_status": smoking_status, "bmi": bmi
        }
        st.success("Data submitted successfully. Proceed to Results.")
