import streamlit as st
import openai

def app(lang):
    st.markdown('<a name="chatbot"></a>', unsafe_allow_html=True)
    st.subheader("💬 " + ("Chatbot Support" if lang == "English" else "Assistance Chatbot"))
    prompt = st.text_input("Ask a question:")

    if st.button("Send") and prompt:
        openai.api_key = st.secrets["openai"]["api_key"]
        with st.spinner("Thinking..."):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            st.success(response.choices[0].message.content)