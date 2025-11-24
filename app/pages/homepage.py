import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Can you afford to live in Zurich?", layout="wide")

st.header("Can you afford to live in Zurich?")

from drafts.cleaning_housing import reshape_housing_data
from drafts.cleaning_population import load_population_data
from drafts.cleaning_rent import load_rent_data

df_housing = reshape_housing_data()
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
import streamlit as st
import plotly.express as px
import pandas as pd


# --- USER INPUTS ---
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

# --- FILTER DATA BY ROOMS AND NONPROFIT STATUS ---
filtered_df = merged_df[
    (merged_df["rooms"] == selected_rooms) &
    (merged_df["nonprofit"] == selected_nonprofit)
].copy()

# --- AGGREGATE PER DISTRICT ---
agg_df = filtered_df.groupby("district", as_index=False).agg({
    "mean": "mean",              # average rent per district
    "population": "mean"         # use population as proxy for depth of market
})

# -------------------------
# 1. RENT AFFORDABILITY SCORE
# -------------------------
agg_df["rent_ratio"] = agg_df["mean"] / salary
agg_df["rent_score"] = (1 - agg_df["rent_ratio"]).clip(0, 1)

# -------------------------
# 2. POPULATION SIZE SCALING
# -------------------------
# Larger population = more opportunities
p_min, p_max = agg_df["population"].min(), agg_df["population"].max()
agg_df["pop_score"] = (agg_df["population"] - p_min) / (p_max - p_min)

# -------------------------
# 3. FINAL SCORE
# Rent dominates (80%), population moderates (20%)
# -------------------------
agg_df["final_score"] = (
    0.8 * agg_df["rent_score"] +
    0.2 * agg_df["pop_score"]
).clip(0, 1)

agg_df = agg_df.dropna(subset=["final_score"])

# -------------------------
# 4. VISUALIZATION
# -------------------------
fig = px.bar(
    agg_df,
    x="district",
    y="final_score",
    color="mean",  # optional visual cue
    color_continuous_scale="Viridis",
    title=f"Likelihood to Find Affordable Housing — Salary CHF {salary:,.0f}, {selected_rooms} rooms, {selected_nonprofit}",
    labels={
        "district": "District",
        "final_score": "Likelihood (0–1)",
        "mean": "Average Rent (CHF)"
    },
)

fig.update_layout(
    yaxis=dict(range=[0, 1]),
    bargap=0.25,
)

st.plotly_chart(fig, use_container_width=True)


st.markdown("""
**How we calculate the “likeliness” to find affordable housing:**

The height of each bar shows the **overall affordability and availability score** for the selected district, number of rooms, and housing type.  
This score combines:

1. **Rent affordability** – how the average rent compares to your entered salary. Lower rent relative to income increases the score.  
2. **Housing availability** – the number of housing units relative to the district’s population. More units per person increase the score.  

The score is weighted (70% rent, 30% availability) and scaled from 0 (least affordable) to 1 (most affordable).  
A taller bar means housing in that district is **more likely to be available and affordable** for you.
""")

