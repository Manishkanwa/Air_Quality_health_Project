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
