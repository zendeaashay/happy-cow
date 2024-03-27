import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from math import pi
import matplotlib.pyplot as plt

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

# Cumulative Sales Over Time for Each Flavor
st.subheader('Cumulative Sales Over Time')
cumulative_sales_df = filtered_df.copy()
cumulative_sales_df['Cumulative Sale'] = cumulative_sales_df.groupby('Flavor')['Sale'].cumsum()
cumulative_line_chart = alt.Chart(cumulative_sales_df).mark_line().encode(
    x='Week',
    y='Cumulative Sale',
    color='Flavor',
    tooltip=['Week', 'Flavor', 'Cumulative Sale']
).interactive()
st.altair_chart(cumulative_line_chart, use_container_width=True)

# Stacked Bar Chart of Sales by Flavor Over Time
st.subheader('Stacked Sales by Flavor Over Time')
stacked_bar_chart = alt.Chart(filtered_df).mark_bar().encode(
    x='Week',
    y=alt.Y('sum(Sale)', stack='normalize'),  # This normalizes the bar heights to stack to 100%
    color='Flavor',
    tooltip=['Week', 'Flavor', 'sum(Sale)']
).interactive()
st.altair_chart(stacked_bar_chart, use_container_width=True)

import pydeck as pdk

# Load data into a pandas DataFrame
# Make sure to use the correct path to your CSV file
df = pd.read_csv('data/ASFPS.csv', usecols=['LATITUDE', 'LONGITUDE'])


# Define the layer for individual points with names
layer = pdk.Layer(
    'ScatterplotLayer',
    df,
    get_position=['LONGITUDE', 'LATITUDE'],
    get_color=[255, 0, 0, 160],  # You can customize the color
    get_radius=100,  # You can customize the radius of the points
    pickable=True
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
    map_style='mapbox://styles/mapbox/light-v9',
    tooltip={"text": "{NAME_EN}"}
)

# Render the map with the points and tooltips for names
st.pydeck_chart(r)


st.markdown("Radar chart for revenue contribution for each 'Flavour' ")
# Function to create radar chart
def create_radar_chart(data, title):
    categories = list(data)
    N = len(categories)

    # Repeat the first value to close the circular graph
    values = data.values.flatten().tolist()
    values += values[:1]

    # Calculate angle for each category
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    plt.xticks(angles[:-1], categories, color='black', size=10)

    # Draw the outline of our data
    ax.plot(angles, values)
    ax.fill(angles, values, 'teal', alpha=0.1)

    # Add a title
    plt.title(title, size=20, color='black', y=1.1)

    return fig

# Read data from Excel file
@st.experimental_memo
def load_data(sheet):
    return pd.read_excel('data/Dataset final.xlsx', sheet_name=sheet)

# Load 'Flavour Analysis' sheet
df = load_data('Flavour Analysis')

# Check if the DataFrame is loaded properly
if df is not None and not df.empty:
    # Process the data for radar chart
    # Group by 'Flavour' and sum the 'Revenue' for each flavour
    df_grouped = df.groupby('Flavour')['Revenue'].sum().reset_index()

    # Scale the 'Revenue' values between 0 and 1 for better display in radar chart
    df_grouped['Revenue'] = df_grouped['Revenue'] / df_grouped['Revenue'].max()

    # Transpose dataframe to have columns for each flavour
    df_transposed = df_grouped.set_index('Flavour').T

    # Plot the radar chart using the processed data
    fig = create_radar_chart(df_transposed, 'Flavour Analysis')

    # Display the radar chart in Streamlit
    st.pyplot(fig)
else:
    st.error('Data not loaded properly. Please check the file path and sheet name.')
