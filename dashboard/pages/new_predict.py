import streamlit as st
import pandas as pd
import numpy as np
import os
from src.predict import custom_data, PredictPipeline

Data = pd.read_excel(os.path.join('data', 'clean_data', 'AQI_Cases_data.xlsx'))
Data_pivot = pd.read_excel(os.path.join('data', 'clean_data', 'Data_pivot.xlsx'))

states = ['Odisha', 'Kerala', 'Meghalaya', 'Mizoram', 'Tamil Nadu', 'Punjab',
       'Karnataka', 'West Bengal', 'Bihar', 'Rajasthan', 'Gujarat',
       'Andhra Pradesh', 'Uttar Pradesh', 'Delhi (NCT)', 'Telangana',
       'Maharashtra', 'Tripura', 'Jharkhand', 'Madhya Pradesh',
       'Nagaland', 'Assam', 'Haryana', 'Chhattisgarh']

months =['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']

pollutant = ['co µg/m³', 'no2 µg/m³', 'pm10 µg/m³', 'pm25 µg/m³', 'so2 µg/m³'] 

st.title("Predict Patients (Per Lakh)") 
s1, s2 = st.columns(2)
c1, c2, c3, c4, c5 = st.columns(5)
state2 = s1.selectbox("Select State",states,key =123 )
month = s2.number_input("month", min_value=1,max_value= 12, )
pm25 = c1.number_input("PM2.5", min_value=0.0, max_value=300.0 )
pm10 = c2.number_input("PM10", min_value=0.0, max_value=400.0 )
co = c3.number_input("CO", min_value=0, max_value=2000, step=10 )
no2 = c4.number_input("NO2", min_value=0.0, max_value=70.0)
so2 = c5.number_input("SO2", min_value=0.0, max_value=200.0)
value = np.mean([pm25, pm10, co, no2, so2])


if st.button("Predict"):
    Data = custom_data(state2, month, co, no2, pm10, pm25, so2)
    df = Data.get_data_as_dataframe()
    make_pred = PredictPipeline()
    pred = make_pred.predictpipeline('Asthama_Model',df)
    pred1 = make_pred.predictpipeline('COPD_Model',df)
    pred2 = make_pred.predictpipeline('Bronchitis_Model',df)
    pred3 = make_pred.predictpipeline('Heart_Model',df)
    pred4 = make_pred.predictpipeline('Neumonia_Model',df)
    st.success(f"Predicted Asthma Cases (per Lakh): {pred}")
    st.success(f"Predicted COPD Cases (per Lakh): {pred1}")
    st.success(f"Predicted Bronchitis Cases (per Lakh): {pred2}")
    st.success(f"Predicted Heart Attack Cases (per Lakh): {pred3}")
    st.success(f"Predicted Pneumonia Cases (per Lakh): {pred4}")
    

st.markdown("""
---
### 🧠 About the Model

This prediction tool uses a machine learning regression model trained on synthetic monthly data combining air quality metrics and assumed health case numbers. The model was developed as part of the **Air Quality & Health Impact Analyzer** project to showcase data science and machine learning capabilities.

**Key Notes:**
- The health case numbers for conditions like Asthma, Bronchitis, COPD, Heart Attacks, and Pneumonia were **not collected from real medical sources**. They are **simulated estimates** generated with the help of ChatGPT to create a plausible dataset for learning and demonstration.
- The predictions made by this model **should not be interpreted as medical advice, real forecasts, or official statistics**.
- This project is designed purely for **educational and portfolio purposes**, demonstrating:
  - Data cleaning and merging from multiple sources
  - Feature engineering (e.g., cyclic encoding for months)
  - Regression modeling and evaluation
  - Interactive dashboard development using Streamlit

### ✅ Purpose

This project aims to demonstrate skills in:
- Data preprocessing and transformation
- Statistical and visual analysis
- Model building and deployment
- Front-end integration with dashboards

---

📌 *If you're a recruiter or reviewer, feel free to explore the codebase and visualizations. Feedback is always welcome!*

""")
