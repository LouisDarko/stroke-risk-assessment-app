import streamlit as st
import plotly.graph_objects as go

def app(lang):
    st.header("📊 " + ("Understanding Your Results" if lang == "English" else "Comprendre Vos Résultats"))
    risk_score = 0.72
    label = "Estimated Stroke Risk" if lang == "English" else "Risque Estimé d'AVC"
    st.metric(label=label, value=f"{risk_score*100:.1f}%", delta="High" if risk_score > 0.7 else "Moderate")

    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = risk_score * 100,
        title = {'text': label},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "red"},
            'steps': [
                {'range': [0, 40], 'color': "lightgreen"},
                {'range': [40, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "red"},
            ]
        }
    ))
    st.plotly_chart(fig)