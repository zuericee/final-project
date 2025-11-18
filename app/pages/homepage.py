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
df_rent_2024 = df_rent[df_rent['year'] == 2024 & (df_rent['area_type'] == "Statistische Quartiere")]

df_housing_2024 = df_housing_2024.drop(columns=['year'])
df_population_2024 = df_population_2024.drop(columns=['year'])
df_rent_2024 = df_rent_2024.drop(columns=['year', 'area_type']) 

# Merge all three data frames
merged_df = df_housing_2024.merge(df_population_2024, on='district', how='outer') \
                           .merge(df_rent_2024, on='district', how='outer') \
                           .merge(df_rent_2024, on='district', how='outer')

st.dataframe(merged_df)
