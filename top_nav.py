import streamlit as st

def top_nav():
    st.markdown("""
    <style>
        .navbar { background-color: #4CAF50; padding: 10px; font-size: 18px; font-weight: bold; text-align: center; }
        .navbar a { color: white; text-decoration: none; padding: 14px 20px; display: inline-block; }
        .navbar a:hover { background-color: #3e8e41; }
    </style>
    <div class="navbar">
        <a href="Home">Home</a>
        <a href="Risk_Assessment">Risk Assessment</a>
        <a href="Results">Results</a>
        <a href="Recommendations">Recommendations</a>
    </div>
    """, unsafe_allow_html=True)
