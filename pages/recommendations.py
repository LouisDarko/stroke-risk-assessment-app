import streamlit as st

def app(lang):
    st.header("💡 " + ("Health Recommendations" if lang == "English" else "Recommandations de Santé"))
    if lang == "English":
        st.markdown("- Exercise 🏃‍♂️\n- Eat healthy 🥦\n- Avoid smoking 🚭\n- Monitor blood pressure and sugar 🩸")
    else:
        st.markdown("- Faire de l'exercice 🏃‍♂️\n- Manger sainement 🥦\n- Éviter de fumer 🚭\n- Surveiller la tension et le sucre 🩸")