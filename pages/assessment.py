import streamlit as st

def app(lang):
    st.header("📝 " + ("Stroke Risk Assessment" if lang == "English" else "Évaluation du Risque d'AVC"))
    with st.form("form"):
        st.subheader("📋 " + ("Personal Info" if lang == "English" else "Infos Personnelles"))
        age = st.slider("Age", 1, 100)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        married = st.radio("Ever Married?", ["Yes", "No"])
        work_type = st.selectbox("Work Type", ["Self-employed", "Private", "Govt Job"])

        st.subheader("🩺 " + ("Health Info" if lang == "English" else "Infos Santé"))
        smoking = st.selectbox("Smoking Status", ["Formerly smoked", "Never smoked", "Smokes"])
        glucose = st.number_input("Average Glucose Level (mg/dL)")
        heart_disease = st.radio("Heart Disease?", ["Yes", "No"])
        hypertension = st.radio("High Blood Pressure?", ["Yes", "No"])
        consent = st.checkbox("✔️ " + ("I agree to the disclaimer" if lang == "English" else "J'accepte la clause de non-responsabilité"))

        if st.form_submit_button("Submit"):
            if consent:
                st.success("✅ " + ("Form submitted! Go to Results page." if lang == "English" else "Formulaire soumis ! Allez à la page Résultats."))
            else:
                st.error("❗" + ("Please agree to proceed." if lang == "English" else "Veuillez accepter pour continuer."))