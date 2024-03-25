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
excel_file_path = 'data/HCdata.xlsx'
student_weekly_df = pd.read_excel(excel_file_path, sheet_name='Student Weekly', usecols=['Week', 'Sales'])
staff_weekly_df = pd.read_excel(excel_file_path, sheet_name='Staff Weekly', usecols=['Week', 'Sales'])
tourist_weekly_df = pd.read_excel(excel_file_path, sheet_name='Tourist Weekly', usecols=['Week', 'Sales'])

# Convert the 'Week' column into datetime and extract the week number for clustering
student_weekly_df['Week_Number'] = pd.to_datetime(student_weekly_df['Week']).dt.week
staff_weekly_df['Week_Number'] = pd.to_datetime(staff_weekly_df['Week']).dt.week
tourist_weekly_df['Week_Number'] = pd.to_datetime(tourist_weekly_df['Week']).dt.week

# Scale the 'Sales' values between 0 and 1
scaler = MinMaxScaler()
student_weekly_df['Sales_Scaled'] = scaler.fit_transform(student_weekly_df[['Sales']])
staff_weekly_df['Sales_Scaled'] = scaler.fit_transform(staff_weekly_df[['Sales']])
tourist_weekly_df['Sales_Scaled'] = scaler.fit_transform(tourist_weekly_df[['Sales']])

# Prepare the data for clustering
student_X = student_weekly_df[['Week_Number', 'Sales_Scaled']].values
staff_X = staff_weekly_df[['Week_Number', 'Sales_Scaled']].values
tourist_X = tourist_weekly_df[['Week_Number', 'Sales_Scaled']].values

# Perform KMeans clustering
kmeans_student = KMeans(n_clusters=3, random_state=42)
kmeans_staff = KMeans(n_clusters=3, random_state=42)
kmeans_tourist = KMeans(n_clusters=3, random_state=42)

student_weekly_df['Cluster'] = kmeans_student.fit_predict(student_X)
staff_weekly_df['Cluster'] = kmeans_staff.fit_predict(staff_X)
tourist_weekly_df['Cluster'] = kmeans_tourist.fit_predict(tourist_X)

# Plotting the clusters for Student Weekly data as an example
plt.figure(figsize=(14, 7))

# Scatter plot for each cluster
for cluster in student_weekly_df['Cluster'].unique():
    cluster_data = student_weekly_df[student_weekly_df['Cluster'] == cluster]
    plt.scatter(cluster_data['Week_Number'], cluster_data['Sales_Scaled'], label=f'Cluster {cluster}')

plt.title('KMeans Clustering of Student Weekly Sales Data')
plt.xlabel('Week Number')
plt.ylabel('Scaled Sales')
plt.legend()
plt.grid(True)
plt.show()