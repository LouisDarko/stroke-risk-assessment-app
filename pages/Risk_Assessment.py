import streamlit as st
import pandas as pd
import joblib
from translations import get_translation


# Page title
st.set_page_config(page_title="Stroke Risk Assessment", layout="wide")
st.title("📝 " + translate("assessment", st.session_state.language))

# Load the trained model
@st.cache_resource
def load_model():
    return joblib.load("best_gb_model.pkl")

model = load_model()

# Encode input fields
def preprocess_input(data):
    # Map gender, marital_status, work_type, etc.
    gender_map = {"Male": 1, "Female": 0, "Other": 2}
    marital_map = {"Single": 0, "Married": 1, "Divorced": 2, "Separated": 3}
    work_map = {"Unemployed": 0, "Self-employed": 1, "Private": 2, "Public": 3}
    smoke_map = {"Never smoked": 0, "Formerly smoked": 1, "Smokes": 2}

    return pd.DataFrame([{
        "age": data["age"],
        "gender": gender_map.get(data["gender"], 0),
        "ever_married": marital_map.get(data["marital_status"], 0),
        "work_type": work_map.get(data["work_type"], 0),
        "hypertension": 1 if data["hypertension"] == "Yes" else 0,
        "heart_disease": 1 if data["heart_disease"] == "Yes" else 0,
        "avg_glucose_level": data["avg_glucose"],
        "smoking_status": smoke_map.get(data["smoking_status"], 0)
    }])

# Personal Information
with st.expander("👤 Personal Information", expanded=True):
    age = st.number_input("Age", min_value=1, max_value=120, help="Enter your age in years.")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"], help="Select your gender.")
    marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Separated"], help="Select your marital status.")
    work_type = st.selectbox("Employment Status", ["Unemployed", "Self-employed", "Private", "Public"], help="Select your current employment status.")

# Health Information
with st.expander("🩺 Health Information", expanded=True):
    hypertension = st.radio("Do you have high blood pressure?", ["Yes", "No"])
    heart_disease = st.radio("Do you have any heart disease?", ["Yes", "No"])
    avg_glucose = st.number_input("Average Glucose Level (mg/dL)", min_value=1, max_value=500)
    smoking_status = st.selectbox("Smoking Status", ["Never smoked", "Formerly smoked", "Smokes"])

# Disclaimer
st.markdown("### 📄 Consent and Disclaimer")
st.write("This tool provides an estimate of stroke risk based on the information you provide. It is not a diagnostic tool and " \
"should not replace professional medical advice. This prediction is based on general patterns" \
"and may not account for your specific health situation.")
st.write("By submitting this form, you agree to allow us to estimate your stroke risk based on the provided information.")
st.checkbox("✅ I agree to the terms and allow risk estimation", key="consent")

# Submit Button
submit_button = st.button("Calculate Stroke Risk 📈")

if submit_button:
    if not st.session_state.consent:
        st.error("You must agree to the terms before proceeding!")
    elif age < 1 or avg_glucose <= 0:
        st.error("Invalid input values.")
    else:
        input_data = {
            "age": age,
            "gender": gender,
            "marital_status": marital_status,
            "work_type": work_type,
            "hypertension": hypertension,
            "heart_disease": heart_disease,
            "avg_glucose": avg_glucose,
            "smoking_status": smoking_status
        }
        X_input = preprocess_input(input_data)

        # Get the probability score (model.predict_proba() returns probabilities for each class)
        prediction_prob = model.predict_proba(X_input)[0][1]  # Prob of high risk (class 1)

        # Store the user data and prediction probability in session state for use on the Results page
        st.session_state.user_data = input_data
        st.session_state.prediction_prob = prediction_prob

        # Display the probability as a score
        st.success(f"🧠 Based on your information, your estimated stroke risk probability is: **{prediction_prob * 100:.2f}%**")

        # Display input data
        st.write("### 🔍 Your Inputs:")
        st.json(input_data)



import openai  # If not already imported

# --- Chatbot widget (floating button) ---
st.markdown("""
<style>
#floating-chat {
  position: fixed;
  bottom: 25px;
  right: 30px;
  z-index: 9999;
}
.chat-popup {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 320px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
</style>
<div id="floating-chat">
  <details>
    <summary style="cursor:pointer;
                    font-size:16px;
                    background:#4C9D70;
                    color:white;
                    padding:10px 20px;
                    border-radius:20px;">
      💬 Chat
    </summary>
    <div class="chat-popup">
""", unsafe_allow_html=True)

chat_input = st.text_input("💡 Ask about stroke:", key="global_chat")
if chat_input:
    resp = openai.Completion.create(
        engine="text-davinci-003",
        prompt=chat_input,
        max_tokens=100
    )
    reply = resp.choices[0].text.strip()
    st.markdown(f"<div style='margin-top:10px;'><strong>🤖:</strong> {reply}</div>",
                unsafe_allow_html=True)

st.markdown("</div></details></div>", unsafe_allow_html=True)
