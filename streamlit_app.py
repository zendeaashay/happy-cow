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

from prettymaps import plot
from matplotlib import pyplot as plt

# Initialize a matplotlib figure
fig, ax = plt.subplots(figsize = (12, 12), constrained_layout = True)

# Define the location and parameters for the plot
backup = plot(
    # Center the map around a location
    'Hong Kong Island',

    # Define the radius to plot around the central point
    radius = 1100,

    # Define additional plotting parameters as needed
    ax = ax,

    # Layers to plot (streets, buildings, etc.)
    layers = {
            'perimeter': {},
            'streets': {
                'width': {
                    'motorway': 5,
                    'primary': 4,
                    'secondary': 3,
                    'tertiary': 2,
                    'residential': 1,
                    'service': 0.5,
                    'footway': 0,
                },
            },
            'building': {'tags': {'building': True, 'landuse': ['retail', 'commercial']}},
            'water': {'tags': {'natural': ['water', 'bay']}},
            'green': {'tags': {'landuse': 'grass', 'natural': ['island', 'wood']}},
            'forest': {'tags': {'landuse': 'forest'}},
            'garden': {'tags': {'leisure': 'garden'}},
    },

    # Additional parameters can include drawing labels, plotting points, etc.
)

# Show the plot
plt.savefig('hong_kong_island.png')
plt.show()