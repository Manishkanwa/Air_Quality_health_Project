# 📑 Project Insights & Report  
**Air Quality & Health Impact Analyzer**  
_Analyzing the link between air pollution and public health across Indian states (2020)_

---

## 📌 Summary

This project investigates the relationship between air quality and public health using monthly state-wise data from India (2020). The goal is to uncover how pollutants like PM2.5, PM10, NO2, and others correlate with health issues such as asthma, COPD, and pneumonia, and to build a predictive system that estimates health impact based on pollution levels.

---

## 📊 Key Findings from Data Analysis

- **Seasonality Detected:** Winter months (November–January) show a spike in PM2.5 and PM10 levels across most states.
- **State-Wise Disparity:** States like Delhi, Uttar Pradesh, and Punjab consistently show high pollutant levels and elevated respiratory case counts.
- **Strong Correlations:** PM2.5 and PM10 show high correlation with asthma and bronchitis cases.
- **AQI Category Distribution:** Majority of states fall in the ‘Moderate’ category, but some show consistent ‘Poor’ levels during peak months.
- **Geo Trends:** Geospatial visualizations highlighted North Indian states as pollution hotspots.

---

## 🔮 Modeling Insights


| Model                   | Target              | Score (R²)      |
|-------------------------|---------------------|-----------------|
| XGBoost Regression      | Asthma Cases        | `0.97`          |
| XGBoost Regression      | Bronchitis_Cases    | `0.98`          | 
| XGBoost Regression      | Heart_attacks       | `0.98`          | 
| XGBoost Regression      | COPD                | `0.94`          | 
| XGBoost Regression      | Neumonia_Cases      | `0.96`          | 

- **Feature Engineering:** Used cyclic encoding for month, one-hot for state, and ordinal encoding for AQI categories.
- **Important Features:** PM2.5, PM10, and NO2 had the highest importance across models.

---

## 📈 Visual Insights

- **Line plots** show time-based trends of pollution and health metrics.
- **Heatmaps** revealed pollutant-disease correlations.
- **Scatter plots** emphasized direct impact of PM2.5 on asthma cases.
- **Interactive Dashboard**: Allows users to input real AQI values and estimate expected health impacts.

---

## 📊 Dashboard Overview

Built using **Streamlit**, the dashboard includes:

- 📉 Visual summaries of pollutants and diseases
- 🎛️ Input controls for pollutants, month, and state
- 🔮 Live predictions for asthma and COPD cases
- 📊 Monthly trends and comparison charts

> **Try it yourself**: [Live Dashboard URL here]

---

## 🧠 Challenges Faced

- 🧹 Data cleaning and state-wise aggregation from inconsistent sources
- 📆 Aligning pollution data and health records month-wise
- 🔢 Encoding categorical data for modeling
- 🎨 Building interactive yet clean visualizations in the dashboard


---

## 👤 Author

**Manish**  
Final year B.Tech (AI & Data Science)  
GATE 2025 DA Qualified | Aspiring Data Scientist  
[GitHub](https://github.com/Manishkanwa) | [LinkedIn](https://www.linkedin.com/in/manish-birla-93457120a/) | Email: kanwamanish212@gmail.com

---
