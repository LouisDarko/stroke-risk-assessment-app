import streamlit as st

def app(lang):
    st.title("🧠 " + ("Stroke Risk Assessment App" if lang == "English" else "Application d'Évaluation du Risque d'AVC"))
    st.image("https://www.cdc.gov/stroke/images/stroke-infographic-1185px.png", use_column_width=True)
    if lang == "English":
        st.markdown("""
        ## 🩺 What is a Stroke?
        A stroke happens when blood flow to the brain is blocked or a blood vessel bursts.

        ### 🧬 Types:
        - Ischemic
        - Hemorrhagic
        - TIA

        ### ⚠️ Risk Factors:
        - High BP, Diabetes, Smoking, Heart Disease
        """)
    else:
        st.markdown("""
        ## 🩺 Qu'est-ce qu'un AVC ?
        Un AVC se produit lorsque le flux sanguin vers le cerveau est bloqué ou qu’un vaisseau éclate.

        ### 🧬 Types:
        - Ischémique
        - Hémorragique
        - AIT

        ### ⚠️ Facteurs de Risque:
        - Hypertension, Diabète, Tabac, Maladie cardiaque
        """)