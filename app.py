import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from dotenv import load_dotenv
from google import genai
from prediction_engine import predict_capacity

# 1. Setup and Environment
# This safely checks for the API key in Streamlit Secrets, 
# falling back to your local .env file if it's not found.
api_key = st.secrets.get("API_KEY")

if not api_key:
    load_dotenv()
    api_key = os.getenv("API_KEY")

st.set_page_config(page_title="Smartech1 Research Co-Pilot", layout="wide")

# 2. Sidebar: AI Chatbot
st.sidebar.title("🤖 Smartech1 AI Assistant")

if api_key:
    # Initialize the client only if the key is present
    client = genai.Client(api_key=api_key)
else:
    st.sidebar.error("API_KEY not found! Please check your Streamlit Secrets or .env file.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.sidebar.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input logic
if prompt := st.sidebar.chat_input("Ask about materials or DAC..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.sidebar.chat_message("user"):
        st.markdown(prompt)
    
    if api_key:
        with st.sidebar.chat_message("assistant"):
            try:
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"AI Error: {e}")
    else:
        st.sidebar.error("Cannot query AI: API Key missing.")

# 3. Main Content: Prediction UI
st.title("Smartech1: CO2 Adsorbent Predictor")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("1. Enter Properties")
    amine = st.number_input("Amine Loading (%)", value=20.0)
    area = st.number_input("Surface Area (m²/g)", value=450.0)
    humidity = st.number_input("Humidity (%)", value=50.0)
    temp = st.number_input("Temperature (K)", value=300.0)
    
    if st.button("Predict Capacity"):
        result = predict_capacity(amine, area, humidity, temp)
        st.success(f"Predicted Capacity: *{result}* mmol/g")
        st.session_state.last_prediction = {'amine': amine, 'area': area, 'hum': humidity, 'temp': temp}

with col2:
    st.subheader("2. Sensitivity Analysis")
    if 'last_prediction' in st.session_state:
        inputs = st.session_state.last_prediction
        sweep_var = st.selectbox("Analyze Trend:", ['Amine Loading', 'Surface Area', 'Humidity', 'Temperature'])
        
        # Sweep Logic for Visualizing Trends
        if sweep_var == 'Amine Loading':
            vals = np.linspace(0, 50, 50)
            res = [predict_capacity(v, inputs['area'], inputs['hum'], inputs['temp']) for v in vals]
        elif sweep_var == 'Surface Area':
            vals = np.linspace(100, 1000, 50)
            res = [predict_capacity(inputs['amine'], v, inputs['hum'], inputs['temp']) for v in vals]
        elif sweep_var == 'Humidity':
            vals = np.linspace(0, 100, 50)
            res = [predict_capacity(inputs['amine'], inputs['area'], v, inputs['temp']) for v in vals]
        else: # Temperature
            vals = np.linspace(273, 373, 50)
            res = [predict_capacity(inputs['amine'], inputs['area'], inputs['hum'], v) for v in vals]
            
        df_plot = pd.DataFrame({'x': vals, 'Capacity': res})
        fig = px.line(df_plot, x='x', y='Capacity', title=f"Trend Analysis: {sweep_var}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👈 Enter data and click 'Predict Capacity' to see trends.")