import streamlit as st

def top_nav():
    st.markdown("""
    <style>
    .nav-menu {
        background-color: #4C9D70;
        padding: 15px;
        border-radius: 10px;
        display: flex;
        justify-content: center;
        gap: 40px;
        font-size: 18px;
        margin-bottom: 30px;
    }
    .nav-menu a {
        color: white;
        text-decoration: none;
        font-weight: bold;
    }
    .nav-menu a:hover {
        text-decoration: underline;
    }
    </style>

    <div class='nav-menu'>
        <a href='Home' target='_self'>🏠 Home</a>
        <a href='Risk_Assessment' target='_self'>📝 Risk Assessment</a>
        <a href='Results' target='_self'>📊 Results</a>
        <a href='Recommendations' target='_self'>💡 Recommendations</a>
    </div>
    """, unsafe_allow_html=True)
