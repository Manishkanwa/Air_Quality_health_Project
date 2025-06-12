import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import os, sys     

Data = pd.read_excel(os.path.join('data', 'clean_data', 'AQI_Cases_data.xlsx'))
Data_pivot = pd.read_excel(os.path.join('data', 'clean_data', 'Data_pivot.xlsx'))

month_map = {
                'January': 1, 'February': 2, 'March': 3, 'April': 4,
                'May': 5, 'June': 6, 'July': 7, 'August': 8,
                'September': 9, 'October': 10, 'November': 11, 'December': 12
            }
reverse_month_map = {v: k for k, v in month_map.items()}
Data_pivot['Month'] = Data_pivot['Month'].map(reverse_month_map )


pollutant = ['co µg/m³', 'no2 µg/m³', 'pm10 µg/m³', 'pm25 µg/m³', 'so2 µg/m³']

st.title("🌍 Air Quality Analysis Map  ")
st.markdown("""
This interactive map visualizes air quality across Indian states for different months. 
""")
with st.sidebar:
    st.header("🔧 Filters")
    selected_month = st.selectbox("Select Month", Data["Month"].unique())

pivot_month = Data_pivot[Data_pivot["Month"] == selected_month]
Data = Data[Data["Month"] == selected_month]
filtered_df = Data.merge(Data_pivot, on = ['State','Month'])

# Layer to visualize pollutant values as circle size
layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_df,
    get_position='[Longitude, Latitude]',
    get_color='[255, 0, 0, 200]',  # Bright red
    get_radius = 10000,  # Bigger circles
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=22.9734,
    longitude=78.6569,
    zoom=4,
    pitch=0,
)

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/outdoors-v12',
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"html": f"""
        <b>State:</b> {{State}}<br>
        <b>Month:</b> {selected_month}<br>
        <b>co µg/m³:</b> {{{'co µg/m³'}}} µg/m³ <br>
        <b>no2 µg/m³:</b> {{{'no2 µg/m³'}}} µg/m³<br>
        <b>pm10 µg/m³:</b> {{{'pm10 µg/m³'}}} µg/m³<br>
        <b>pm25 µg/m³:</b> {{{'pm25 µg/m³'}}} µg/m³<br>
        <b>so2 µg/m³:</b> {{{ 'so2 µg/m³'}}} µg/m³<br>
    """}),
    use_container_width=True, 
)

st.subheader(f"📊 Pollution Summary for {selected_month}")

# Filter the pivot data for the selected month
month_data = Data_pivot[Data_pivot["Month"] == selected_month]

# Create a column layout: 3 columns per row
cols = st.columns(3)

# Loop over pollutants and display metrics
for i, pol in enumerate(pollutant):
    avg = month_data[pol].mean()
    max_val = month_data[pol].max()
    min_val = month_data[pol].min()
    
    with cols[i % 3]:
        st.metric(f"{pol} (Avg)", f"{avg:.2f} µg/m³", help=f"Max: {max_val:.2f}, Min: {min_val:.2f}")


st.markdown("---")
st.caption("📌 Data Source: OpenAQ API | Project by Manish")
