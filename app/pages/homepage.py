import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Can you afford to live in Zurich?", layout="wide")

st.header("Can you afford to live in Zurich?")

from drafts.cleaning_housing import reshape_housing_data
from drafts.cleaning_population import load_population_data
from drafts.cleaning_rent import load_rent_data
from drafts.cleaning_income import load_income_data

df_housing = reshape_housing_data()
df_population = load_population_data()
df_rent = load_rent_data()
df_income = load_income_data()

#Filter each data frame for year 2024
df_housing_2024 = df_housing[df_housing['year'] == 2024]
df_population_2024 = df_population[df_population['year'] == 2024]
df_rent_2024 = df_rent[(df_rent['year'] == 2024) & (df_rent['area_type'] == "Stadtkreise") & (df_rent['price_type']=="Netto") & (df_rent['unit_kind']=="Wohnung")]

df_housing_2024 = df_housing_2024.drop(columns=['year'])
df_population_2024 = df_population_2024.drop(columns=['year'])
df_rent_2024 = df_rent_2024.drop(columns=['year', 'area_type']) 

#Merge all three data frames
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

st.subheader("Your chances of finding affordable housing per district (Data for 2024)")

show_df = st.checkbox("Show cleaned dataframe")

if show_df:
    st.dataframe(merged_df)

#User inputs
salary = st.number_input(
    "Enter your monthly net salary (CHF):",
    min_value=1000,
    max_value=30000,
    step=100,
    key="salary_input"
)

selected_rooms = st.selectbox(
    "Select number of rooms:",
    options=[2, 3, 4],
    key="rooms_input"
)

selected_nonprofit = st.selectbox(
    "Select housing type:",
    options=["Gemeinnützig", "Nicht gemeinnützig"],
    key="nonprofit_input"
)

#Filter data by rooms and nonprofit status
filtered_df = merged_df[
    (merged_df["rooms"] == selected_rooms) &
    (merged_df["nonprofit"] == selected_nonprofit)
].copy()

#Aggregate per district
agg_df = filtered_df.groupby("district", as_index=False).agg({
    "mean rent": "mean",              # average rent per district
    "population": "mean"         # use population as proxy for depth of market
})


#Rent affordability score

agg_df["rent_ratio"] = agg_df["mean rent"] / salary
agg_df["rent_score"] = (1 - agg_df["rent_ratio"]).clip(0, 1)

#Population size scaling

# Larger population = more opportunities
p_min, p_max = agg_df["population"].min(), agg_df["population"].max()
agg_df["pop_score"] = (agg_df["population"] - p_min) / (p_max - p_min)


#Final score
#Rent dominates (80%), population moderates (20%)

agg_df["final_score"] = (
    0.8 * agg_df["rent_score"] +
    0.2 * agg_df["pop_score"]
).clip(0, 1)

agg_df = agg_df.dropna(subset=["final_score"])


#Visualisation

fig = px.bar(
    agg_df,
    x="district",
    y="final_score",
    color="mean rent",  # optional visual cue
    color_continuous_scale="Viridis",
    title=f"Likelihood to Find Affordable Housing — Salary CHF {salary:,.0f}, {selected_rooms} rooms, {selected_nonprofit}",
    labels={
        "district": "District",
        "final_score": "Likelihood (0–1)",
        "mean rent": "Average Rent (CHF)"
    },
)

fig.update_layout(
    yaxis=dict(range=[0, 1]),
    bargap=0.25,
)

st.plotly_chart(fig, use_container_width=True)


st.markdown("""
**What this chart shows:**  
This visual estimates your **likelihood of finding an affordable apartment** in each district, based on your selected salary, number of rooms, and housing type.  
- **High score (~1):** The district is likely affordable for you.  
- **Low score (~0):** Housing is less affordable or scarce.  

**How it’s calculated:**  
- 80% weight: average rent for apartments matching your criteria  
- 20% weight: market depth approximated by district population  

**Important notes:**  
- Scores are **indicative, not guaranteed availability**.  
- Only average rents are considered; specific listings may differ.  
- Other costs (utilities, maintenance) are not included.
""")

#Rent burden metric: % of income spent on average rent

#Filter for 2022
df_housing_2022 = df_housing[df_housing['year'] == 2022]
df_population_2022 = df_population[df_population['year'] == 2022]
df_rent_2022 = df_rent[(df_rent['year'] == 2022) & (df_rent['area_type'] == "Stadtkreise") & (df_rent['price_type']=="Netto") & (df_rent['unit_kind']=="Wohnung")]
df_income_2022 = df_income[df_income["year"] == 2022].copy()

df_housing_2022 = df_housing_2022.drop(columns=['year'])
df_population_2022 = df_population_2022.drop(columns=['year'])
df_rent_2022 = df_rent_2022.drop(columns=['year', 'area_type']) 
df_income_2022 = df_income_2022.drop(columns=['year'])

#Aggregate median income per district (mean across tax tariffs)
income_per_district = (
    df_income_2022
    .groupby("district", as_index=False)
    .agg({"median income": "mean"})
)

#Merge with main dataframe
merged_df = merged_df.merge(
    income_per_district,
    on="district",
    how="left"
)

#Drop "Ganze Stadt" from dataframe
merged_df = merged_df[merged_df["district"] != "Ganze Stadt"].copy()

#Monthly income
merged_df["median income"] = merged_df["median income"] * 1000 / 12

#Compute rent burden
merged_df["rent_burden"] = merged_df["mean rent"] / merged_df["median income"]

# Classify burden
merged_df["burden_class"] = pd.cut(
    merged_df["rent_burden"],
    bins=[0, 0.30, 0.40, float("inf")],
    labels=["Affordable", "Stress", "Overburdened"]
)

st.subheader("Where Is Rent Hitting Residents Hardest? (Data for 2022)")

show_df_rent = st.checkbox("Show cleaned dataframe", key="show_df_rent_checkbox")

if show_df_rent:
    st.dataframe(merged_df[["district", "rooms", "mean rent", "median income", "rent_burden", "burden_class"]])

#Order districts by number
district_order = ["Kreis " + str(i) for i in range(1, 13)]

# --- User inputs ---
selected_rooms = st.selectbox(
    "Select number of rooms:",
    options=sorted(merged_df["rooms"].unique())
)

selected_nonprofit = st.selectbox(
    "Select housing type:",
    options=merged_df["nonprofit"].unique()
)

# --- Filter data ---
filtered_df = merged_df[
    (merged_df["rooms"] == selected_rooms) &
    (merged_df["nonprofit"] == selected_nonprofit)
].copy()

# --- Aggregate per district ---
agg_df = filtered_df.groupby("district", as_index=False).agg({
    "rent_burden": "mean",
    "burden_class": lambda x: x.mode()[0]  # most frequent class
})

# Optional: order districts
district_order = ["Kreis " + str(i) for i in range(1, 13)]
agg_df = agg_df.sort_values("district", key=lambda x: x.map({k: i for i, k in enumerate(district_order)}))

# --- Bar chart ---
fig = px.bar(
    agg_df,
    x="district",
    y="rent_burden",
    color="burden_class",
    category_orders={"district": district_order},
    color_discrete_map={
        "Affordable": "green",
        "Stress": "orange",
        "Overburdened": "red"
    },
    title=f"Rent Burden — {selected_rooms} Rooms, {selected_nonprofit}",
    labels={
        "district": "District",
        "rent_burden": "Rent Burden",
        "burden_class": "Burden Class"
    },
    text=agg_df["rent_burden"].apply(lambda x: f"{x:.0%}")
)

fig.update_layout(
    yaxis=dict(tickformat=".0%"),
    xaxis_title="District",
    yaxis_title="Rent as % of Monthly Income",
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
**What this chart shows:**  
This bar chart shows **what percentage of monthly income is spent on rent** for each district:  

- **Green (Affordable):** Rent ≤ 30% of income  
- **Orange (Stress):** Rent 30–40% of income  
- **Red (Overburdened):** Rent > 40% of income  

**Important notes:**  
- Percentages are based on **average rents** for selected apartment types.  
- Districts with few apartments may have extreme values.  
- This classification **does not account for other household costs**.
""")

