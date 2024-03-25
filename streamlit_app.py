import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
# Page title
st.set_page_config(page_title='Happy Cow Case Study Group 7', page_icon='📊')
st.title('📊 Happy Cow Case Study Group 7')

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

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Load the datasets from the Excel file
file_path = 'data/HCdata.xlsx'
sheets = ['Student Weekly', 'Staff Weekly', 'Tourist Weekly']
data = {}

# Read each sheet and perform preprocessing
for sheet in sheets:
    df = pd.read_excel(file_path, sheet_name=sheet, usecols=['Week', 'Sales'])
    df['Week'] = pd.to_datetime(df['Week']).dt.isocalendar().week  # Convert 'Week' to week number
    df['Sales'] = df['Sales'].astype(float)  # Ensure 'Sales' is float
    data[sheet] = df

# Scale the 'Sales' data
scaler = StandardScaler()

# Perform clustering for each sheet
for sheet, df in data.items():
    df_scaled = scaler.fit_transform(df[['Week', 'Sales']])
    kmeans = KMeans(n_clusters=3, random_state=42)  # Choose an appropriate number of clusters
    clusters = kmeans.fit_predict(df_scaled)
    df['Cluster'] = clusters  # Add the cluster labels to the DataFrame

    # Plotting the clusters
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Week'], df['Sales'], c=df['Cluster'], cmap='viridis', label=sheet)
    plt.title(f'KMeans Clustering of {sheet}')
    plt.xlabel('Week Number')
    plt.ylabel('Scaled Sales')
    plt.legend()
    plt.show()