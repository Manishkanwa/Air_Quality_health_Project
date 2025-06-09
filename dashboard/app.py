import streamlit as st
import pandas as pd
import numpy as np
import os, sys
from src.train_model import Data_Transformation
import matplotlib.pyplot as plt
import pickle as pkl

def load_object(file_path):
    try:
        with open(file_path, "rb") as obj :
            return pkl.load(obj)
    except Exception as e:
        print("exception occured in loading object!", e)
    
    
st.title("Air Quality Health Impact Analyzer")
preprocessor_path = os.path.join('models', 'preprocessor.pkl')
model_path = os.path.join('models', 'model.pkl')


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
pm25 = st.slider("PM2.5", 0, 2100)
pm10 = st.slider("PM10", min_value=0.0, max_value=400.0, value=35.0)
co = st.slider("CO", 0, 500)
no2 = st.slider("NO2 µg/m³", min_value=0.0, max_value=70.0, value=35.0)
so2 = st.slider("SO2", 0, 500)

value = np.mean([pm25, pm10, co, no2, so2])

data = {'State' : [state2],
        'Month':[month], 
        'co µg/m³':[co],
        'no2 µg/m³' : [no2], 
        'pm10 µg/m³' :[pm10], 
        'pm25 µg/m³':[pm25], 
        'so2 µg/m³':[so2]}

df = pd.DataFrame(data )

prep = load_object(preprocessor_path)
model = load_object(model_path)

print("df before transform:\n", df)
print("Type:", type(df))
print("Shape:", getattr(df, 'shape', 'N/A'))

df = prep.transform(df)
pred = model['Asthama_Model'].predict(df)

if st.button("Predict"):
    st.success(f"Predicted Asthma Cases: {pred}")

