import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

# Page title
st.set_page_config(page_title='Happy Cow Case Study Group 7', page_icon='📊')
st.title('📊 Happy Cow Case Study Group 7')

file_path = 'data/Dataset final.xlsx'
df = pd.ExcelFile(file_path)

@st.experimental_memo
def load_data():
    # Load each sheet
    staff_weekly = pd.read_excel('data/Dataset final.xlsx', sheet_name='Staff Weekly')
    tourist_weekly = pd.read_excel('data/Dataset final.xlsx', sheet_name='Tourist Weekly')
    student_weekly = pd.read_excel('data/Dataset final.xlsx', sheet_name='Student Weekly')
    
    # Add a 'Type' column to differentiate the data
    staff_weekly['Type'] = 'Staff'
    tourist_weekly['Type'] = 'Tourist'
    student_weekly['Type'] = 'Student'
    
    # Add a 'Type' column to differentiate the data
    staff_weekly['Type'] = 'Staff'
    tourist_weekly['Type'] = 'Tourist'
    student_weekly['Type'] = 'Student'
    
    # Melt the DataFrames to have flavors as one column
    staff_flavors = staff_weekly.melt(id_vars=['Week', 'Type'], var_name='Flavor', value_name='Sales')
    tourist_flavors = tourist_weekly.melt(id_vars=['Week', 'Type'], var_name='Flavor', value_name='Sales')
    student_flavors = student_weekly.melt(id_vars=['Week', 'Type'], var_name='Flavor', value_name='Sales')
    
    # Combine the melted DataFrames
    combined_flavors_df = pd.concat([staff_flavors, tourist_flavors, student_flavors], ignore_index=True)
    return combined_flavors_df

combined_flavors_df = load_data()

st.subheader('Flavor Sales Comparison')

# Allow users to select one or more flavors
selected_flavors = st.multiselect('Select Flavors', options=combined_flavors_df['Flavor'].unique())

# Filter data based on selected flavors
filtered_data = combined_flavors_df[combined_flavors_df['Flavor'].isin(selected_flavors)]

# Create a line chart to compare selected flavors across weeks and customer types
flavor_sales_chart = alt.Chart(filtered_data).mark_line().encode(
    x='Week:N',
    y=alt.Y('Sales:Q', title='Sales'),
    color='Type:N',
    tooltip=['Week', 'Type', 'Flavor', 'Sales'],
    strokeDash='Flavor',
).interactive()

st.altair_chart(flavor_sales_chart, use_container_width=True)



