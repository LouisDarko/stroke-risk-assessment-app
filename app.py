    ),unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    info_card("🧩", "Types of Stroke", """
    <ul>
        <li><strong>Ischemic:</strong> Blockage in brain arteries.</li>
        <li><strong>Hemorrhagic:</strong> Burst blood vessels in the brain.</li>
        <li><strong>TIA:</strong> Temporary blockage (mini-stroke).</li>
    </ul>
    """)
    info_card("❗", "Common Causes", """
    <ul>
        <li>High blood pressure</li>
        <li>Heart disease</li>
        <li>Diabetes</li>
        <li>Smoking</li>
        <li>Obesity and cholesterol</li>
    </ul>
    """)
    info_card("🏃", "Prevention", """
    <ul>
        <li>Control blood pressure & sugar</li>
        <li>Exercise regularly</li>
        <li>Eat a healthy diet</li>
        <li>Stop smoking</li>
    </ul>
    """)
with col2:
    info_card("⚠️", "Symptoms", """
    <ul>
        <li>Sudden numbness or weakness (face, arm, leg)</li>
        <li>Confusion, speech trouble</li>
        <li>Vision problems</li>
        <li>Dizziness or balance issues</li>
    </ul>
    """)
    info_card("⏱️", "Recognize a Stroke (FAST)", """
    <strong>Use the FAST test:</strong>
    <ul>
        <li><strong>F:</strong> Face drooping</li>
        <li><strong>A:</strong> Arm weakness</li>
        <li><strong>S:</strong> Speech difficulty</li>
        <li><strong>T:</strong> Time to call emergency</li>
    </ul>
    """)
    info_card("📊", "Stroke Statistics", """
    <ul>
        <li>2nd leading cause of death globally</li>
        <li>12.2 million cases in 2020</li>
        <li>5.5 million deaths annually</li>
    </ul>
    """)

# Call to Action Section
st.markdown("""
    <div style='background-color:#e6f2ff; padding:30px; border-radius:12px; text-align:center; margin-top:30px;'>
        <h4>📝 Assess Your Stroke Risk</h4>
        <p>Click below to use our intelligent tool and evaluate your risk level.</p>
        <a href='/Risk_Assessment' target='_self'><button style='background-color:#4C9D70; color:white; padding:12px 24px; font-size:16px; border:none; border-radius:8px; cursor:pointer; transition:all 0.3s ease;'>➡️ Start Risk Assessment</button></a>
    </div>
    <style>
    button:hover {
        background-color: #3e8e41;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# Custom Footer
st.markdown("""
    <style>
        .custom-footer {
            background-color: rgba(76, 157, 112, 0.6);
            color: white;
            padding: 30px 0;
            border-radius: 12px;
            margin-top: 40px;
            text-align: center;
            font-size: 14px;
            width: 100%;
            position: relative;
        }
        .custom-footer a {
            color: white;
            text-decoration: none;
            margin: 0 15px;
        }
        .custom-footer a:hover {
            text-decoration: underline;
        }
        .footer-text {
            width: 80%;
            margin: 0 auto;
        }
    </style>
    <div class="custom-footer">
        <div class="footer-text">
            <p>&copy; 2025 Stroke Risk Assessment Tool | All rights reserved</p>
            <p>
                <a href='/Home' target='_self'>Home</a>
                <a href='/Risk_Assessment' target='_self'>Risk Assessment</a>
                <a href='/Results' target='_self'>Results</a>
                <a href='/Recommendations' target='_self'>Recommendations</a>
            </p>
            <p style="font-size: 12px; margin-top: 10px;">Developed by Victoria Mends</p>
        </div>
    </div>
""", unsafe_allow_html=True)
