import streamlit as st
from top_nav import top_nav
from translations import get_translation

# Hide Streamlit default UI elements
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Top navigation bar
top_nav()

# Language selection for translations
language = st.selectbox("🌍 Language", list(get_translation('').keys()))
lang_key = language.split()[0]
text = get_translation(lang_key)

# Set the current page from query parameters, default to "home"
page = st.experimental_get_query_params().get("page", ["home"])[0]

# Render the page based on the current query parameter
if page == "home":
    # Home Page content
    st.title(text['title'])
    st.write(text['desc'])

    # Text-to-speech helper
    def create_audio(text_str, lang_code):
        try:
            from gtts import gTTS
            tts = gTTS(text_str, lang=lang_code)
            file_path = f"tts_home_{lang_code}.mp3"
            tts.save(file_path)
            with open(file_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                st.audio(f"data:audio/mp3;base64,{b64}", format="audio/mp3")
            os.remove(file_path)
        except Exception:
            st.warning("Audio not available for this language.")

    create_audio(text['desc'], text.get('lang_code', 'en'))

    # Warning signs section
    st.markdown(f"""
    <div style='background-color:#fff3cd; padding:20px; border-radius:10px;'>
      <h4>{text['warning']}</h4>
      <ul>
        {''.join(f'<li>{item}</li>' for item in text['warning_list'])}
      </ul>
    </div>
    """, unsafe_allow_html=True)

    # Button to go to Risk Assessment
    st.markdown(f"""
    <a href="?page=risk_assessment">
        <button style="padding:12px 24px; background-color:#4CAF50; color:white; border:none; border-radius:8px;">
            {text['cta']}
        </button>
    </a>
    """, unsafe_allow_html=True)

elif page == "risk_assessment":
    # Import the Risk_Assessment page content here
    import Risk_Assessment

elif page == "results":
    # Import the Results page content here
    import Results

elif page == "recommendations":
    # Import the Recommendations page content here
    import Recommendations
