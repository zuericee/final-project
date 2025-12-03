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

show_df = st.checkbox("Show cleaned dataframe")
if show_df:
    st.dataframe(df_filtered)

st.subheader("How has the population of Zurich changed over time?")

#Group by year and sum population across all districts
df_over_time = (
    df.groupby(['year', 'district'], as_index=False)['population'].sum()
      .groupby('year', as_index=False)['population'].sum()
)

fig_growth = px.line(
    df_over_time,
    x='year',
    y='population',
    markers=True,
    labels={'year': '', 'population': ''}
)
st.plotly_chart(fig_growth, use_container_width=True)

st.subheader(f"Population distribution across Zurich's districts in {selected_year}")

#Aggregate by district
df_district = (
    df_filtered
    .groupby('district', as_index=False)
    .agg({
        'population': 'sum'
    })
)

df_sub_info = df_filtered.groupby('district')['neighbourhood'].apply(list).reset_index()
df_district = df_district.merge(df_sub_info, on='district', how='left')

# Create bar chart with hover showing all subdistrict names
fig_2024 = px.bar(
    df_district,
    x='district',
    y='population',
    hover_data={'neighbourhood': True},
    labels={'district': '', 'population': ''}
)

fig_2024.update_layout(
    xaxis_tickangle=-45,
    hoverlabel_align='left'
)

st.plotly_chart(fig_2024, use_container_width=True)

st.markdown("""
**What this chart shows:**  
How residents are distributed across districts for a selected year.  
- Helps contextualize housing demand and availability.  

**Important notes:**  
- Does not account for population density within districts.  
- Only permanent residents are included.
""")