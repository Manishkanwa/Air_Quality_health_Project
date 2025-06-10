import streamlit as st
import pandas as pd
import numpy as np
import os, sys
from src.predict import custom_data, PredictPipeline
import matplotlib.pyplot as plt
import pickle as pkl

    
st.title("Air Quality Health Impact Analyzer")


states = ['Odisha', 'Kerala', 'Meghalaya', 'Mizoram', 'Tamil Nadu', 'Punjab',
       'Karnataka', 'West Bengal', 'Bihar', 'Rajasthan', 'Gujarat',
       'Andhra Pradesh', 'Uttar Pradesh', 'Delhi (NCT)', 'Telangana',
       'Maharashtra', 'Tripura', 'Jharkhand', 'Madhya Pradesh',
       'Nagaland', 'Assam', 'Haryana', 'Chhattisgarh']

# Sidebar filters
state1 = st.sidebar.selectbox("Select State",states )
pollutant = st.sidebar.selectbox("Select Pollutant", ['co µg/m³', 'no2 µg/m³', 'pm10 µg/m³', 'pm25 µg/m³', 'so2 µg/m³'])

# Main section
st.header("Pollution Trend")
df = pd.read_excel(os.path.join('data', 'clean_data', 'Data_pivot.xlsx'))
st.line_chart(df[df["State"] == state1][[pollutant]])

# Input for model prediction
st.header("Predict Health Impact")    
state2 = st.selectbox("Select State",states,key =123 )
month = st.slider("month", 1, 12)
pm25 = st.slider("PM2.5", min_value=0.0, max_value=300.0 )
pm10 = st.slider("PM10", min_value=0.0, max_value=400.0 )
co = st.slider("CO", min_value=0.0, max_value=2000.0 )
no2 = st.slider("NO2", min_value=0.0, max_value=70.0)
so2 = st.slider("SO2", min_value=0.0, max_value=200.0)
value = np.mean([pm25, pm10, co, no2, so2])


if st.button("Predict"):
    Data = custom_data(state2, month, co, no2, pm10, pm25, so2)
    df = Data.get_data_as_dataframe()
    make_pred = PredictPipeline()
    pred = make_pred.predictpipeline('Asthama_Model',df)
    st.success(f"Predicted Asthma Cases (per Lakh): {pred}")

