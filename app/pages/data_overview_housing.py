import streamlit as st
import pandas as pd
import plotly.express as px

from drafts.cleaning_housing import load_housing_data

df = load_housing_data()

st.set_page_config(page_title="Housing Viewer", layout="wide")

st.header("Zurich's Housing Stock per District from 2008 to 2024")

st.subheader("Raw Data Preview")

#Filter by year
years = sorted(df["year"].unique())
selected_year = st.selectbox("Select year:", years)
filtered_df = df[df["year"] == selected_year]

show_df = st.checkbox("Show cleaned dataframe")

if show_df:
    st.dataframe(filtered_df)

st.subheader("How has the total housing stock in the city and per district changed over time?")

#Dropdown for city district selection
district_options = df['district'].unique()
selected_district_time = st.selectbox("Select a city district:", district_options, key="time_chart_selectbox")

#Filter the DataFrame based on selection
filtered_df = df[df['district'] == selected_district_time]

#Plotly line chart
fig = px.line(
    filtered_df,
    x='year',
    y='total housing units',
)

fig.update_layout(
    xaxis_title="",
    yaxis_title="",
    yaxis=dict(range=[0, filtered_df['total housing units'].max() * 1.1])  # starts at 0
)

#Display chart in Streamlit
st.plotly_chart(fig)

st.subheader("What is the distribution of apartment types in the city and per district in 2024?")

#Dropdown to select city district
district_options = df['district'].unique()
selected_district_bar = st.selectbox("Select a city district:", district_options, key="bar_chart_selectbox")

#Filter rows by selected city district and year 2024
filtered_df = df[(df['district'] == selected_district_bar) & (df.iloc[:, -1] == 2024)]

if not filtered_df.empty:
    #Take the first matching row
    row_values = filtered_df.iloc[0, 2:-1].tolist()  # skip first 2 columns and last column

    #Labels from column headers (skip first 2 and last column)
    labels = df.columns[2:-1].tolist()

    #Create bar chart
    fig = px.bar(
        x=labels,
        y=row_values,
        labels={'x': 'Apartment Type', 'y': 'Fraction'},
    )

    fig.update_layout(
    xaxis_title="",
    yaxis_title=""
    )

    st.plotly_chart(fig)
else:
    st.warning(f"No data available for {selected_district_bar} in 2024.")