import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

# Page title
st.set_page_config(page_title='Happy Cow Case Study Group 7', page_icon='📊')
st.title('📊 Happy Cow Case Study Group 7')
df = pd.read_excel('data/Dataset final.xlsx')

# Load data
@st.cache
def load_data(sheet_name):
    return pd.read_excel('data/Dataset final.xlsx', sheet_name=sheet_name)

# Assuming these sheets are of interest
staff_weekly_df = load_data('Staff Weekly')
tourist_weekly_df = load_data('Tourist Weekly')

# Preprocess the data (e.g., parse dates, handle missing values)
# ...

# Input widgets to filter data
# Assuming you want to compare weekly sales for staff and tourists
week_selection = st.selectbox('Select Week', staff_weekly_df['Week'])

# Filter data based on selection
staff_weekly_selected = staff_weekly_df[staff_weekly_df['Week'] == week_selection]
tourist_weekly_selected = tourist_weekly_df[tourist_weekly_df['Week'] == week_selection]

# Visualize data
# Assuming you have columns like 'Sales' in these sheets
st.subheader('Weekly Sales Comparison')
sales_comparison_chart = alt.Chart(staff_weekly_selected).mark_bar().encode(
    x='Week',
    y='Sales',
    color=alt.value('orange'),
    tooltip=['Sales']
).properties(
    width=300,
    height=300
) | alt.Chart(tourist_weekly_selected).mark_bar().encode(
    x='Week',
    y='Sales',
    color=alt.value('blue'),
    tooltip=['Sales']
).properties(
    width=300,
    height=300
)

st.altair_chart(sales_comparison_chart, use_container_width=True)