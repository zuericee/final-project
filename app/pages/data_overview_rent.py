import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

from drafts.cleaning_rent import load_rent_data

df = load_rent_data()

st.set_page_config(page_title="Rent Viewer", layout="wide")
st.header("Rent Prices in Zurich per District")

st.sidebar.header("Filter Options")

#Year filter
years = df['year'].dropna().unique()
selected_year = st.sidebar.selectbox("Select year:", years)

#Geografischer Raum filter
area_types = df['area_type'].dropna().unique()
selected_raum = st.sidebar.selectbox("Select area type:", area_types)

#Number of rooms filter
rooms = df['rooms'].dropna().unique()
selected_rooms = st.sidebar.selectbox("Select number of rooms:", rooms)

#Brutto/Netto filter
rent_types = df['price_type'].dropna().unique()
selected_rent_type = st.sidebar.selectbox("Select brutto / netto:", rent_types)

#Nonprofit filter
nonprofit_options = df['nonprofit'].dropna().unique()
selected_nonprofit = st.sidebar.selectbox("Select nonprofit / market price", nonprofit_options)

#Price per m² / pro Wohnung filter
unit_kinds = df['unit_kind'].dropna().unique()
selected_unit = st.sidebar.selectbox("Select price type:", unit_kinds)

#Filter the dataframe
df_filtered = df[
    (df['year'] == selected_year) &
    (df['area_type'] == selected_raum) &
    (df['rooms'] == selected_rooms) &
    (df['price_type'] == selected_rent_type) &
    (df['unit_kind'] == selected_unit) &
    (df['nonprofit'] == selected_nonprofit)
]

#Display filtered table
st.subheader(f"Filtered Data: {selected_year}, {selected_raum}")
show_df = st.checkbox("Show cleaned dataframe")

if show_df:
    st.dataframe(df_filtered)

st.subheader("Percentile Chart of Rent Prices")

#Aggregate for plotting
agg = (
    df_filtered.groupby("district")
    .agg({
        "qu10": "mean",
        "qu25": "mean",
        "qu50": "mean",
        "qu75": "mean",
        "qu90": "mean"
    })
    .reset_index()
)

#Visualisation
fig, ax = plt.subplots(figsize=(8, 4))

num_rows = len(agg)
fig_height = max(4, num_rows * 0.5)  # 0.5 inch per row minimum
fig, ax = plt.subplots(figsize=(8, fig_height))

y_positions = range(num_rows)

for i, row in enumerate(agg.itertuples(index=False)):
    y = y_positions[i]

    ax.hlines(y, xmin=row.qu10, xmax=row.qu90, linewidth=8, alpha=0.2)
    ax.hlines(y, xmin=row.qu25, xmax=row.qu75, linewidth=8, alpha=0.4)
    ax.plot(row.qu50, y, marker="o", markersize=10)

ax.set_yticks(y_positions)
ax.set_yticklabels(agg["district"])
ax.set_xlabel("Rent price (Median & Percentiles)")
ax.grid(axis='x', linestyle='--', alpha=0.3)

st.pyplot(fig)

st.markdown("""
**What this chart shows:**  
This visual displays the distribution of rents across Zurich and its districts.  

- **Median:** The rent value that splits the data in half – half of rents are below, half above.  
- **Quantile:** Shows the share of rents below a certain value. Example: the 25% quantile means 25% of rents are below this value.  
- **Confidence Interval:** The 95% confidence interval indicates the range that likely contains the true rent value. City-wide intervals are about ±4% of the median or mean, while smaller areas can have higher uncertainty, up to 20%.  

**Important notes:**  
- Percentiles and medians help understand rent spread.  
- Intervals show the reliability of estimates, especially for smaller districts.
""")