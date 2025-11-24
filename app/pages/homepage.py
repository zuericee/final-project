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
    "mean": "mean",              # average rent per district
    "population": "mean"         # use population as proxy for depth of market
})


#Rent affordability score

agg_df["rent_ratio"] = agg_df["mean"] / salary
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
### How this chart is calculated

To estimate your chances of finding affordable housing in each district, we combine three pieces of information:

**1. Your monthly salary**  
You enter your net salary.  
Housing is considered *affordable* if the monthly rent does not exceed **30% of your salary**.  
Instead of a simple yes/no rule, we use a **continuous scale**:  
- If the average rent in a district is below that threshold → score close to 1  
- If it is above → the score decreases proportionally

This avoids arbitrary cut-offs and reflects how “close” the rent is to being affordable.

---

**2. Rental prices in each district**  
We use the average rent for homes matching your selected criteria:
- housing type (gemeinnützig / nicht gemeinnützig)
- number of rooms

Districts with lower average rents will receive a higher score.

---

**3. District population size**  
Larger districts generally offer more listings, more turnover, and more opportunities to find a flat.  
Smaller districts may have very few available units, even if average rents look attractive.  
We therefore scale the population between 0 and 1:
- Larger population → higher availability score  
- Smaller population → lower availability score

This does **not** measure “density” or “crowdedness,” but rather the general depth of the market.

---

### Final score
We combine the two components with different weights:

- **80% rent affordability**
- **20% district size (market depth)**

This ensures that rent remains the primary factor, while still considering how likely it is to find an apartment in a given district.

---

### Interpretation
- **Scores close to 1** → high likelihood of finding something affordable  
- **Scores near 0** → low likelihood  
- The chart is not a prediction of available apartments, but a simplified indicator based on current rents and the size of the housing market.
""")


