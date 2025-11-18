import streamlit as st
import pandas as pd
import plotly.express as px

from drafts.cleaning_population import load_population_data

df = load_population_data()

st.set_page_config(page_title="Population Viewer", layout="wide")

st.header("Zurich's Population per District")

st.subheader("Raw Data Preview")



#Selection for year
years = sorted(df['year'].dropna().unique())
selected_year = st.selectbox("Select year:", years)

df_filtered = df[df['year'] == selected_year]

st.dataframe(df_filtered)

st.subheader("How has the population of Zurich changed over time?")

# Group by year and sum population across all districts
df_over_time = df.groupby('year', as_index=False)['population'].sum()

# Plot the growth
fig_growth = px.line(
    df_over_time,
    x='year',
    y='population',
    markers=True,
    labels={'year': '', 'population': ''}
)

st.plotly_chart(fig_growth, use_container_width=True)

st.subheader("What is the population distribution across districts in 2024?")

df_2024 = df[df['year'] == 2024]

fig_2024 = px.bar(
    df_2024,
    x='district',
    y='population',
    labels={'district': '', 'population': ''}
)

fig_2024.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig_2024, use_container_width=True)