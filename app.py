# app.py

import streamlit as st
import pandas as pd
import joblib

# Load the trained model
rf_model = joblib.load('model.pkl')

# Features based on the model
numerical_features = [
    'power_consumption (Watts)',
    'voltage_levels (Volts)',
    'current_fluctuations (Amperes)',
    'temperature (Celsius)',
    'current_fluctuations_env (Amperes)'
]

environmental_features = [
    'environmental_conditions_Cloudy',
    'environmental_conditions_Rainy'
]

all_features = numerical_features + environmental_features

# Fault type mapping
fault_type_mapping = {
    0: 'No fault',
    1: 'Short circuit',
    2: 'Voltage Surge',
    3: 'Bulb failure',
    4: 'Light Flickering'
}

# Streamlit UI
st.set_page_config(page_title="Street Light Fault Predictor")
st.title("Street Light Fault Prediction App")

st.markdown("### Enter Input Data")

with st.form(key='prediction_form'):
    user_input = {}
    for feature in numerical_features:
        user_input[feature] = st.number_input(f"{feature}", value=0.0)

    env_condition = st.selectbox("Environmental Conditions", ['Clear', 'Cloudy', 'Rainy'])

    submit_button = st.form_submit_button(label='Predict Fault Type')

if submit_button:
    # Encode environmental condition as one-hot
    user_input['environmental_conditions_Cloudy'] = 1 if env_condition == 'Cloudy' else 0
    user_input['environmental_conditions_Rainy'] = 1 if env_condition == 'Rainy' else 0

    # Convert to DataFrame and reorder columns
    input_df = pd.DataFrame([user_input])[all_features]

    # Prediction
    pred_fault_num = rf_model.predict(input_df)[0]
    pred_fault_desc = fault_type_mapping.get(pred_fault_num, "Unknown Fault Type")

    # Display result
    st.markdown("### Prediction Result")
    st.success(f"Predicted Fault Type: {pred_fault_desc} (Code: {pred_fault_num})")
