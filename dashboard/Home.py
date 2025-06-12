import streamlit as st
import pandas as pd
import numpy as np
import os, sys
from src.predict import custom_data, PredictPipeline
import matplotlib.pyplot as plt
import pickle as pkl

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


lat =list(dict(Data)['Latitude'])
long = list(dict(Data)['Longitude'])

st.markdown("""# 🏥 Air Quality & Health Impact Analyzer

A full-time data science project exploring the impact of air pollution on public health across Indian states. The project integrates air quality data and monthly health statistics to uncover patterns and correlations using visualizations, EDA, and statistical modeling.

---

## 📌 Project Objective

To analyze how varying levels of air pollution affect public health metrics like respiratory and cardiovascular disease cases, and build a reproducible pipeline for data fetching, aggregation, analysis, and insights visualization.

---

## 📅 Timeline Covered

* **Year**: 2020
* **Granularity**:

  * **Air Quality**: Monthly state-wise average (aggregated from daily city-level sensor data)
  * **Health Data**: Monthly state-wise counts

---

## 📂 Data Collected

### 🏭 Air Quality Data (via OpenAQ API)

* Parameters: `PM2.5`, `PM10`, `NO2`, `SO2`, `O3`, `CO`
* Source: [OpenAQ Platform](https://docs.openaq.org/)
* Granularity: Hourly → aggregated to daily → aggregated to monthly (state-wise)
* Coverage: All Indian states

### 🩺 Health Impact Data

* Source: Publicly available health reports
* Collected indicators (monthly, per state):

  * `Asthma_Cases`
  * `Bronchitis_Cases`
  * `Heart_Attacks`
  * `COPD_Cases`
  * `Pneumonia_Cases`

---

## 📊 Exploratory Data Analysis (Completed)

* 📆 **Monthly pollution trends** across states and pollutants
* 📌 **State-wise comparison** of health cases vs pollution
* 🔁 **Correlation heatmaps** between pollutants and diseases

---

## 🔮 Model Summary (Completed)

| Model              | Target            | Score (R²) |
| ------------------ | ----------------- | ---------- |
| XGBoost Regression | Asthma Cases      | `0.97`     |
| XGBoost Regression | Bronchitis\_Cases | `0.98`     |
| XGBoost Regression | Heart\_attacks    | `0.98`     |
| XGBoost Regression | COPD              | `0.94`     |
| XGBoost Regression | Neumonia\_Cases   | `0.96`     |

* ✅ **Preprocessing**: StandardScaler, OneHotEncoder, CyclicEncoder, OrdinalEncoder
* ✅ **Feature Engineering**: Month cyclic encoding, AQI categorization, state dummies
* ✅ **Evaluation**: R², MAE, feature importances

---

### 📈 Model Metrics

#### Asthma Cases

| Model                    | RMSE  | MAE  | R²    |
| ------------------------ | ----- | ---- | ----- |
| XGBoost Regression       | 7.66  | 1.64 | 0.974 |
| Random Forest Regression | 8.00  | 2.61 | 0.972 |
| Linear Regression        | 8.93  | 5.77 | 0.965 |
| Lasso Regression         | 9.04  | 5.22 | 0.964 |
| Ridge Regression         | 12.94 | 8.19 | 0.927 |

#### Bronchitis Cases

| Model                    | RMSE | MAE  | R²    |
| ------------------------ | ---- | ---- | ----- |
| XGBoost Regression       | 1.10 | 0.24 | 0.987 |
| Random Forest Regression | 2.37 | 0.65 | 0.939 |
| Linear Regression        | 2.83 | 1.54 | 0.914 |
| Lasso Regression         | 3.07 | 1.67 | 0.899 |
| Ridge Regression         | 3.38 | 1.90 | 0.877 |

#### Heart Attacks

| Model                    | RMSE | MAE  | R²    |
| ------------------------ | ---- | ---- | ----- |
| XGBoost Regression       | 0.42 | 0.14 | 0.985 |
| Random Forest Regression | 0.44 | 0.15 | 0.983 |
| Linear Regression        | 0.56 | 0.38 | 0.973 |
| Ridge Regression         | 0.96 | 0.60 | 0.920 |
| Lasso Regression         | 1.62 | 0.91 | 0.772 |

#### COPD

| Model                    | RMSE | MAE  | R²    |
| ------------------------ | ---- | ---- | ----- |
| XGBoost Regression       | 1.27 | 0.43 | 0.949 |
| Random Forest Regression | 1.42 | 0.57 | 0.936 |
| Linear Regression        | 1.63 | 1.30 | 0.916 |
| Ridge Regression         | 1.68 | 1.31 | 0.910 |
| Lasso Regression         | 2.09 | 1.41 | 0.861 |

#### Pneumonia Cases

| Model                    | RMSE | MAE  | R²    |
| ------------------------ | ---- | ---- | ----- |
| XGBoost Regression       | 0.57 | 0.27 | 0.969 |
| Random Forest Regression | 0.94 | 0.36 | 0.917 |
| Ridge Regression         | 1.87 | 1.55 | 0.672 |
| Lasso Regression         | 1.90 | 1.54 | 0.661 |
| Linear Regression        | 1.98 | 1.63 | 0.632 |

---

## 📈 Key Visualizations

* 📊 Pollution vs Disease scatter plots
* 🔥 Correlation heatmaps (PM2.5 vs Asthma, etc.)
* 🧭 Time-series trendlines (monthly)

> *Visuals created using Plotly, Seaborn, and Matplotlib*

---

## ✅ Dashboard & Deployment

* Streamlit interface to input pollutant values
* Predict asthma/COPD/other health cases in real-time
* Interactive graphs, trend visualizations, and summary cards
* Deployed using **Streamlit Cloud** and linked in portfolio

---

## 👤 Author

**Manish**
B.Tech in Artificial Intelligence & Data Science
GATE 2025 DA Qualified | Aspiring Data Scientist

---

## 📬 Contact

* LinkedIn: [https://www.linkedin.com/in/manish-birla-93457120a/](https://www.linkedin.com/in/manish-birla-93457120a/)
* GitHub: [https://github.com/Manishkanwa](https://github.com/Manishkanwa)
* Email: [kanwamanish212@gmail.com](mailto:kanwamanish212@gmail.com)

---

## 📌 Note

This project is complete and has been fully deployed with a working dashboard and trained models. All results, visuals, and code are reproducible and open for review.

""")





