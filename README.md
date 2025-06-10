# 🏥 Air Quality & Health Impact Analyzer

A full-time data science project exploring the impact of air pollution on public health across Indian states. The project integrates air quality data and monthly health statistics to uncover patterns and correlations using visualizations, EDA, and statistical modeling.

---

## 📌 Project Objective

To analyze how varying levels of air pollution affect public health metrics like respiratory and cardiovascular disease cases, and build a reproducible pipeline for data fetching, aggregation, analysis, and insights visualization.

---

## 📅 Timeline Covered

- **Year**: 2020
- **Granularity**:
  - **Air Quality**: Monthly state-wise average (aggregated from daily city-level sensor data)
  - **Health Data**: Monthly state-wise counts

---

## 📂 Data Collected

### 🏭 Air Quality Data (via OpenAQ API)
- Parameters: `PM2.5`, `PM10`, `NO2`, `SO2`, `O3`, `CO`
- Source: [OpenAQ Platform](https://docs.openaq.org/)
- Granularity: Hourly → aggregated to daily → aggregated to monthly (state-wise)
- Coverage: All Indian states

### 🩺 Health Impact Data
- Source: Publicly available health reports
- Collected indicators (monthly, per state):
  - `Asthma_Cases`
  - `Bronchitis_Cases`
  - `Heart_Attacks`
  - `COPD_Cases`
  - `Pneumonia_Cases`

---

## 📊 Next Steps

### ✅ Exploratory Data Analysis (EDA)
- Trends and seasonal visualization
- Heatmaps and state-wise comparisons
- Correlation between pollutants and diseases

### 🧠 Predictive Modeling (Planned)
- Regression and classification models for health risk prediction
- State-level clustering based on AQI and disease metrics

### 📈 Dashboard (Planned)
- Interactive dashboard to explore air quality and health impact

---

## 🛠️ Tools & Stack

- **Languages**: Python
- **Libraries**: Pandas, NumPy, Matplotlib, Seaborn, Plotly, Scikit-learn
- **API**: OpenAQ (v3)
- **Data Handling**: CSV, JSON
- **IDE**: Jupyter Notebooks,Visual Studio
- **Planned Additions**: Flask dashboard, Map visualizations, Logging, Time-lag correlation

---

## 📊 Exploratory Data Analysis (Completed)

- 📆 **Monthly pollution trends** across states and pollutants


- 📌 **State-wise comparison** of health cases vs pollution




- 🔁 **Correlation heatmaps** between pollutants and diseases

---

## 🔮 Model Summary (Completed)

| Model                   | Target              | Score (R²)      |
|-------------------------|---------------------|-----------------|
| XGBoost Regression      | Asthma Cases        | `0.97`          |
| XGBoost Regression      | Bronchitis_Cases    | `0.98`          | 
| XGBoost Regression      | Heart_attacks       | `0.98`          | 
| XGBoost Regression      | COPD                | `0.94`          | 
| XGBoost Regression      | Neumonia_Cases      | `0.96`          | 

- ✅ **Preprocessing**: StandardScaler, OneHotEncoder, CyclicEncoder, OrdinalEncoder
- ✅ **Feature Engineering**: Month cyclic encoding, AQI categorization, state dummies
- ✅ **Evaluation**: R², MAE, feature importances

---

The metrices for  Asthama_Cases
                      Model       RMSE       MAE        R²
4        XGBoost Regression   7.662990  1.640370  0.974454
3  Random Forest Regression   8.004050  2.607360  0.972129
0         Linear Regression   8.929375  5.769518  0.965312
2          Lasso Regression   9.037726  5.215046  0.964465
1          Ridge Regression  12.940147  8.188244  0.927153

The metrices for  Bronchitis_Cases
                      Model      RMSE       MAE        R²
4        XGBoost Regression  1.097937  0.238995  0.987008
3  Random Forest Regression  2.373072  0.647909  0.939308
0         Linear Regression  2.826007  1.544492  0.913929
2          Lasso Regression  3.068762  1.665929  0.898507
1          Ridge Regression  3.380535  1.899716  0.876836

The metrices for  Heart_attacks
                      Model      RMSE       MAE        R²
4        XGBoost Regression  0.420315  0.138767  0.984607
3  Random Forest Regression  0.436128  0.147995  0.983427
0         Linear Regression  0.558065  0.376944  0.972863
1          Ridge Regression  0.955295  0.603239  0.920483
2          Lasso Regression  1.618980  0.914740  0.771615

The metrices for  COPD
                      Model      RMSE       MAE        R²
4        XGBoost Regression  1.267361  0.428012  0.948847
3  Random Forest Regression  1.415144  0.567937  0.936222
0         Linear Regression  1.628857  1.297157  0.915504
1          Ridge Regression  1.680125  1.307095  0.910101
2          Lasso Regression  2.092514  1.407011  0.860553

The metrices for  Neumonia_Cases
                      Model      RMSE       MAE        R²
4        XGBoost Regression  0.570303  0.269458  0.969398
3  Random Forest Regression  0.940921  0.362490  0.916700
1          Ridge Regression  1.867537  1.547558  0.671846
2          Lasso Regression  1.898508  1.544942  0.660872
0         Linear Regression  1.977739  1.631150  0.631975



## 📈 Key Visualizations

- 📊 Pollution vs Disease scatter plots
- 🔥 Correlation heatmaps (PM2.5 vs Asthma, etc.)
- 🧭 Time-series trendlines (monthly)

> *Visuals created using Plotly, Seaborn, and Matplotlib*

---

## 🚀 Upcoming Work

### 🔧 Dashboard (In Progress)
- Streamlit interface to input pollutant values
- Predict asthma/COPD cases in real-time
- Interactive graphs and summary cards

### 🔗 Flask API (Optional)
- Expose trained model via REST endpoint
- Allow JSON-based prediction inputs

### 🌐 Deployment
- Streamlit Cloud or Render for public access
- Integration with portfolio website







## 👤 Author

**Manish**  
B.Tech in Artificial Intelligence & Data Science  
GATE 2025 DA Qualified | Aspiring Data Scientist

---

## 📬 Contact

- LinkedIn: (https://www.linkedin.com/in/manish-birla-93457120a/)
- GitHub: (https://github.com/Manishkanwa)
- Email: (kanwamanish212@gmail.com)

---

## 📌 Note

This project is under active development. New visualizations, modeling experiments, and dashboards will be added iteratively.
