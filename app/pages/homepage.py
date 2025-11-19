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
df_rent_2024 = df_rent[(df_rent['year'] == 2024) & (df_rent['area_type'] == "Stadtkreise") & (df_rent['price_type']=="Netto") & (df_rent['unit_kind']=="Wohnung")]

df_housing_2024 = df_housing_2024.drop(columns=['year'])
df_population_2024 = df_population_2024.drop(columns=['year'])
df_rent_2024 = df_rent_2024.drop(columns=['year', 'area_type']) 

# Merge all three data frames
merged_df = (
    df_rent_2024
        .merge(df_population_2024, on='district', how='outer')
        .merge(df_housing_2024, on=['district', 'rooms'], how='outer')
)

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

st.subheader("Your chances of finding affordable housing per district")

#User input
salary = st.number_input(
    "Enter your monthly net salary (CHF):",
    min_value=1000,
    max_value=30000,
    step=100,
    key="salary_input"
)

if salary:
    # Affordability: 1 if fully affordable, smaller if expensive
    rent_ratio = merged_df["mean"] / (salary * 0.3)
    merged_df["affordability"] = ((1 / rent_ratio) * 100).clip(0, 100)

    st.write("Based on your salary and the average rents, we estimated a preliminary chance of affording an apartment in each district. " \
    "A higher salary relative to the district’s average rent increases your chance. " \
    "The values are scaled so that districts where rent is much lower than " \
    "30 percent of your salary appear with higher chances, while districts with higher rents appear lower. " \
    "This gives a first overview of where your budget fits best.")
   
   
    #Availability
    #merged_df["availability"] = merged_df["available_units"] / merged_df["available_units"].max()
    
    # Competition: more population → lower chance
    #merged_df["competition"] = 1 - (merged_df["population"] / merged_df["population"].max())
    
    # Combined chance
    #merged_df["chance"] = (merged_df["affordability"] *
                          #  merged_df["availability"] *
                         #   merged_df["competition"] * 100).clip(0, 100)
    
    # Plot grouped by housing type per district
    #fig = px.bar(
       # merged_df,
       # x="district",
       # y="chance",
       # color="type",
       # barmode="group",
       # labels={"chance": "Chance (%)", "district": ""},
   # )
   # fig.update_yaxes(range=[0, 100])
   # st.plotly_chart(fig, use_container_width=True)