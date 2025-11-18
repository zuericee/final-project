import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Can you afford to live in Zurich?", layout="wide")

st.header("Can you afford to live in Zurich?")

from drafts.cleaning_housing import load_housing_data
from drafts.cleaning_population import load_population_data
from drafts.cleaning_rent import load_rent_data

df_housing = load_housing_data()
df_population = load_population_data()
df_rent = load_rent_data()

#Filter each data frame for year 2024
df_housing_2024 = df_housing[df_housing['year'] == 2024]
df_population_2024 = df_population[df_population['year'] == 2024]
df_rent_2024 = df_rent[(df_rent['year'] == 2024) & (df_rent['area_type'] == "Stadtkreise")]

df_housing_2024 = df_housing_2024.drop(columns=['year'])
df_population_2024 = df_population_2024.drop(columns=['year'])
df_rent_2024 = df_rent_2024.drop(columns=['year', 'area_type']) 

# Merge all three data frames
merged_df = df_housing_2024.merge(df_population_2024, on='district', how='outer') \
                           .merge(df_rent_2024, on='district', how='outer')

order = ["Ganze Stadt"] + [f"Kreis {i}" for i in range(1, 13)]

merged_df['district'] = pd.Categorical(
    merged_df['district'],
    categories=order,
    ordered=True
)

merged_df = merged_df.sort_values('district')

show_df = st.checkbox("Show merged dataframe")

if show_df:
    st.dataframe(merged_df)

# Input for monthly net salary
salary = st.number_input(
    "Enter your monthly net salary (CHF):",
    min_value=1000,
    max_value=30000,
    step=100,
)

st.subheader("Your chances of finding affordable housing per district")

if salary > 0:
    merged_df["chance"] = 1 - (merged_df["mean"] / (salary * 0.3))
    merged_df["chance"] = merged_df["chance"].clip(0, 1)

    fig = px.bar(
        merged_df,
        x="district",
        y="chance",
        labels={"chance": "", "district": ""},
    )
    st.plotly_chart(fig, use_container_width=True)
