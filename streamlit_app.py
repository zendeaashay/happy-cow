import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

# Page title
st.set_page_config(page_title='Happy Cow Case Study Group 7', page_icon='📊')
st.title('📊 Happy Cow Case Study Group 7')
df = pd.read_excel('data/Dataset final.xlsx')

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
    
    # Combine the DataFrames
    combined_weekly_df = pd.concat([staff_weekly, tourist_weekly, student_weekly], ignore_index=True)
    return combined_weekly_df

combined_weekly_df = load_data()

# Preprocess the data (e.g., parse dates, handle missing values)
# ...

st.subheader('Weekly Sales Comparison')

# Assuming 'Week' and 'Sales' are the column names in your Excel sheets
# Create a single bar chart with one axis for all weeks and sales for staff, tourists, and students
sales_comparison_chart = alt.Chart(combined_weekly_df).mark_bar().encode(
    x='Week:N',
    y='Sales:Q',
    color='Type:N',
    tooltip=['Week', 'Type', 'Sales']
).interactive()

st.altair_chart(sales_comparison_chart, use_container_width=True)
