import streamlit as st
import pandas as pd
import plotly.express as px

from drafts.cleaning_population import load_population_data

df = load_population_data()

st.set_page_config(page_title="Bevölkerung Viewer", layout="wide")

st.header("Zurich's Population per District")

st.subheader("Raw Data Preview")

df.rename(columns={
    'StichtagDatJahr': 'jahr',
    'QuarSort': 'district number',
    'QuarLang': 'district',
    'AnzBestWir': 'population'
}, inplace=True)

df.drop(columns=['district number'], inplace=True)

#Selection for year
years = sorted(df['jahr'].dropna().unique())
selected_year = st.selectbox("Select year:", years)

df_filtered = df[df['jahr'] == selected_year]

st.dataframe(df_filtered)

st.subheader("How has the population of Zurich changed over time?")

# Group by year and sum population across all districts
df_over_time = df.groupby('jahr', as_index=False)['population'].sum()

# Plot the growth
fig_growth = px.line(
    df_over_time,
    x='jahr',
    y='population',
    markers=True,
    labels={'jahr': '', 'population': ''}
)

st.plotly_chart(fig_growth, use_container_width=True)