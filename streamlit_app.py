import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
# Page title
st.set_page_config(page_title='Happy Cow Case Study Group 7', page_icon='📊')
st.title('📊 Happy Cow Case Study Group 7')
st.markdown("""
    <iframe title="Happy Cow dashboard" width="1140" height="541.25"
    src="https://app.powerbi.com/reportEmbed?reportId=08d68e57-7a2a-4cd8-955c-686ada36138d&autoAuth=true&ctid=a8eec281-aaa3-4dae-ac9b-9a398b9215e7"
    frameborder="0" allowFullScreen="true"></iframe>
""", unsafe_allow_html=True)
file_path = 'data/Dataset final.xlsx'

sheet_names = ['Staff Weekly', 'Tourist Weekly', 'Student Weekly']
data_frames = {sheet_name: pd.read_excel(file_path, sheet_name=sheet_name) for sheet_name in sheet_names}

# Dropdown to select the customer type
customer_type = st.selectbox('Select Customer Type', options=sheet_names)

# Load the selected DataFrame
df = data_frames[customer_type]


# Assuming 'Week' is a consistent column across all sheets and you want to exclude 'Sales' and 'Header' from melting
id_vars = ['Week']
value_vars = [col for col in df.columns if col not in id_vars + ['Sale', 'Header']]

# Confirm 'value_vars' only contains valid column names
st.write(f"Columns to melt: {value_vars}")  # This will display the columns to be melted in your Streamlit app for debugging

# Before melting, let's ensure there's no issue with the DataFrame
if 'Sale' not in df.columns:
    st.markdown(" ")
else:
    melted_df = df.melt(id_vars=id_vars, value_vars=value_vars, var_name='Flavor', value_name='Sale')
    # Proceed with your visualization code...
# Melt the DataFrame to long format for easier plotting with Altair
id_vars = ['Week']
value_vars = [col for col in df.columns if col not in id_vars + ['Sale', 'Header']]
melted_df = df.melt(id_vars=id_vars, value_vars=value_vars, var_name='Flavor', value_name='Sale')

# Sales Trends Over Time for Each Flavor
st.subheader('Sales Trends Over Time')
flavors = st.multiselect('Select Flavors', options=melted_df['Flavor'].unique(), default=melted_df['Flavor'].unique()[:5])
filtered_df = melted_df[melted_df['Flavor'].isin(flavors)]
line_chart = alt.Chart(filtered_df).mark_line().encode(
    x='Week',
    y='Sale',
    color='Flavor',
    tooltip=['Week', 'Flavor', 'Sale']
).interactive()
st.altair_chart(line_chart, use_container_width=True)

# Comparison of Flavor Popularity
st.subheader('Comparison of Flavor Popularity')
bar_chart = alt.Chart(filtered_df).mark_bar().encode(
    x='Flavor',
    y='sum(Sale)',
    color='Flavor',
    tooltip=['Flavor', 'sum(Sale)']
).interactive()
st.altair_chart(bar_chart, use_container_width=True)

import pydeck as pdk

# Load data into a pandas DataFrame
# Make sure to use the correct path to your CSV file
df = pd.read_csv('data/ASFPS.csv', usecols=['LATITUDE', 'LONGITUDE'])

# Define a layer for the heatmap
layer = pdk.Layer(
    'HeatmapLayer',     # The type of layer to use
    df,                 # The pandas DataFrame containing the data
    get_position=['LONGITUDE', 'LATITUDE'],  # The [longitude, latitude] pair
    get_weight=1,       # The weight of each position
    radius_pixels=60,   # The radius of each heatmap point
)

# Set the initial view state for the map
view_state = pdk.ViewState(
    latitude=df['LATITUDE'].mean(),
    longitude=df['LONGITUDE'].mean(),
    zoom=11,
    pitch=0
)

# Create the deck.gl map
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style='mapbox://styles/mapbox/light-v9'
)

# Render the map
st.pydeck_chart(r)