import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

Data = pd.read_excel(os.path.join('data', 'clean_data', 'AQI_Cases_data.xlsx'))
Data_pivot = pd.read_excel(os.path.join('data', 'clean_data', 'Data_pivot.xlsx'))

df_states = list(Data_pivot['State'].unique())

df_months =['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']

df_pollutant = ['co µg/m³', 'no2 µg/m³', 'pm10 µg/m³', 'pm25 µg/m³', 'so2 µg/m³']


# Sidebar Filters
st.sidebar.header("🧰 Filters")
states = st.sidebar.multiselect("Select States", options=df_states, default=["Delhi (NCT)", "Maharashtra"])
months = st.sidebar.multiselect("Select Months", options=df_months, default=["January", "February", "March"])
pollutants = st.sidebar.multiselect(
    "Select Pollutants",
    options=df_pollutant,
    default=['pm25 µg/m³']
)
health_issues = st.sidebar.multiselect(
    "Select Health Metrics",
    options=['Asthama_Cases', 'Bronchitis_Cases', 'COPD_Cases', 'Heart_Attack_Cases', 'Pneumonia_Cases'],
    default=['Asthama_Cases']
)



# Filter data based on selections
# Plot 1: Pollution trend by month for selected states
if len(states)< 5:
    st.subheader("📈 Monthly Pollution Trend")
    filtered_df = Data_pivot[Data_pivot['State'].isin(states)]
    # Plot pollutants in 2-column layout
    for i, pollutant in enumerate(pollutants):
        if i % 2 == 0:
            col1, col2 = st.columns(2)  # New row of 2 columns

        fig, ax = plt.subplots(figsize=(6, 4))
        sns.lineplot(data=filtered_df, x='Month', y=pollutant, hue='State', marker='o', ax=ax)
        plt.xticks(ticks=np.arange(12), labels=df_months, rotation=45)
        plt.title(f"{pollutant} Over Months")

        # Show plot in correct column
        if i % 2 == 0:
            col1.pyplot(fig)
        else:
            col2.pyplot(fig)
        

# Plot 2: pollution in cities
st.subheader("🩺 Pollutant in cities Comparison")
for pollutant in (pollutants):
    df_state = (Data_pivot.groupby('State')[pollutant].mean())
    st.line_chart(data=df_state, y = pollutant, x_label= "State",y_label= pollutant)
        

# Plot 3: Health condition trend by month
st.subheader("🩺 Monthly Health Issues Trend")
filtered_df = Data_pivot[Data_pivot['State'].isin(states)]
# Plot pollutants in 2-column layout
for i, issue in enumerate(health_issues):
    if i % 2 == 0:
        col1, col2 = st.columns(2)  # New row of 2 columns

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.lineplot(data=filtered_df, x='Month', y=issue, hue='State', marker='o', ax=ax)
    plt.xticks(ticks=np.arange(12), labels=df_months, rotation=45)
    plt.title(f"{issue} Over Months")

    # Show plot in correct column
    if i % 2 == 0:
        col1.pyplot(fig)
    else:
        col2.pyplot(fig)
        

# Plot 4: Disease cases in cities
st.subheader("🩺 Disease cases in cities Comparison")
for issue in (health_issues):
    df_state = (Data_pivot.groupby('State')[issue].mean())
    st.line_chart(data=df_state, y = issue, x_label= "State",y_label= issue)
    
# Footer
st.markdown("---")
st.markdown("📍 Use the sidebar filters to customize the visualizations.")








