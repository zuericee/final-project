import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page setup ---
st.set_page_config(page_title="Can you afford to live in Zurich?", layout="wide")
st.header("Can you afford to live in Zurich?")

# --- Data loading ---
from drafts.cleaning_housing import reshape_housing_data
from drafts.cleaning_population import load_population_data
from drafts.cleaning_rent import load_rent_data
from drafts.cleaning_income import load_income_data

df_housing = reshape_housing_data()
df_population = load_population_data()
df_rent = load_rent_data()
df_income = load_income_data()

# --- Filter 2024 data ---
df_population_2024 = df_population[df_population['year'] == 2024].drop(columns=['year'])
df_rent_2024 = df_rent[
    (df_rent['year'] == 2024) &
    (df_rent['area_type'] == "Stadtkreise") &
    (df_rent['price_type'] == "Netto") &
    (df_rent['unit_kind'] == "Wohnung")
].drop(columns=['year', 'area_type'])

# --- Merge population and rent ---
merged_df = df_rent_2024.merge(df_population_2024, on='district', how='outer')

# --- District order ---
district_order = ["Ganze Stadt"] + [f"Kreis {i}" for i in range(1, 13)]
merged_df['district'] = pd.Categorical(merged_df['district'], categories=district_order, ordered=True)
merged_df = merged_df.sort_values('district')

# --- UI: Data preview ---
st.subheader("Your chances of finding affordable housing per district (Data for 2024)")
if st.checkbox("Show cleaned dataframe"):
    st.dataframe(merged_df)

# --- User inputs ---
salary = st.number_input("Enter your monthly net salary (CHF):", min_value=1000, max_value=30000, step=100)
selected_rooms = st.selectbox("Select number of rooms:", options=[2, 3, 4])

# --- Filter by selected rooms ---
filtered_df = merged_df[merged_df["rooms"] == selected_rooms].copy()

# --- Aggregate across housing types ---
agg_df = filtered_df.groupby("district", as_index=False).agg({
    "mean rent": "mean"
})

# Compute housing growth for selected room number
filtered_df_housing = df_housing[df_housing["rooms"]==selected_rooms].copy()

# Function to compute housing growth per district
def compute_housing_growth(df, value_col="count"):
    first_year = df[df["year"] == df["year"].min()].set_index("district")[value_col]
    last_year = df[df["year"] == df["year"].max()].set_index("district")[value_col]
    growth = ((last_year - first_year) / first_year).reset_index().rename(columns={value_col: "housing_growth"})
    return growth

# Keep only the last 3 years
last_year = filtered_df_housing["year"].max()
filtered_df_housing = filtered_df_housing[
    filtered_df_housing["year"].isin([last_year - 2, last_year - 1, last_year])
]

# Compute growth
housing_growth = compute_housing_growth(filtered_df_housing)

# Now you can merge it with your aggregated df
agg_df = agg_df.merge(housing_growth, on="district", how="left")

# --- Compute scores ---
# Affordability: lower share of salary spent = higher score
RENT_SHARE_MAX = 0.3  # 30% of salary is "modest"
agg_df["rent_score"] = (1 - (agg_df["mean rent"] / salary) / RENT_SHARE_MAX).clip(0, 1)

# Rescale housing growth to 0–1 across districts
min_growth = agg_df["housing_growth"].min()
max_growth = agg_df["housing_growth"].max()
agg_df["growth_score"] = ((agg_df["housing_growth"] - min_growth) / (max_growth - min_growth)).clip(0, 1)

# Combined final score
agg_df["final_score"] = (0.7 * agg_df["rent_score"] + 0.3 * agg_df["growth_score"]).clip(0, 1)



# --- Visualization ---
fig = px.bar(
    agg_df,
    x="district",
    y="final_score",
    color="mean rent",
    color_continuous_scale="Viridis",
    title=f"Likelihood to Find Affordable Housing — Salary CHF {salary:,.0f}, {selected_rooms} rooms",
    labels={"district_str": "District", "final_score": "Likelihood (0–1)", "mean rent": "Average Rent (CHF)"},
    hover_data=["mean rent", "rent_score", "growth_score"],
)
fig.update_layout(yaxis=dict(range=[0, 1]), bargap=0.25)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
**What this chart shows:**  
This visual estimates your **likelihood of finding an affordable apartment** in each district, based on your selected salary, number of rooms, and housing type.  

- **High score (~1):** Rent is affordable and housing stock is growing.  
- **Low score (~0):** Rent is high or housing stock growth is low.  

**How it’s calculated:**  
- 70% weight: average rent for apartments matching your criteria  
- 30% weight: normalized housing stock growth per district  

**Important notes:**  
- Scores are indicative.  
- Only average rents are considered; actual listings may vary.  
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

#Classify burden
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
    "Select number of rooms:", key="rooms_selectbox",
    options=sorted(merged_df["rooms"].unique())
)

selected_nonprofit = st.selectbox(
    "Select housing type:", key="nonprofit_selectbox",
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
- Percentages are based on **median salaries**, as an average of different tax tariffs and **average rents** for selected apartment types.  
- Individual situations may vary significantly from these averages. Color shading does not account for houshold size.
""")

