import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

from drafts.cleaning_rent import load_rent_data

df = load_rent_data()

st.set_page_config(page_title="Miete Viewer", layout="wide")
st.header("Rent Prices in Zurich per District")

st.sidebar.header("Filter Options")

#Year filter
years = sorted(df['year'].dropna().unique())
selected_year = st.sidebar.selectbox("Select Year", years)

st.sidebar.header("Filter Options")

#Geografischer Raum filter
area_types = df['area_type'].unique()
selected_raum = st.sidebar.selectbox("Select area type", area_types)

#Number of rooms filter
rooms = df['rooms'].dropna().unique()
selected_rooms = st.sidebar.selectbox("Select number of rooms", rooms)

#Brutto/Netto filter
rent_types = df['price_type'].dropna().unique()
selected_rent_type = st.sidebar.selectbox("Select brutto / netto", rent_types)

#Price per m² / pro Wohnung filter
unit_kinds = df['unit_kind'].dropna().unique()
selected_unit = st.sidebar.selectbox("Select price type", unit_kinds)

# Filter the dataframe
df_filtered = df[
    (df['year'] == selected_year) &
    (df['area_type'] == selected_raum) &
    (df['rooms'] == selected_rooms) &
    (df['price_type'] == selected_rent_type) &
    (df['unit_kind'] == selected_unit)
]

# Display filtered table
st.subheader(f"Filtered Data: {selected_year}, {selected_raum}")
st.dataframe(df_filtered)

st.subheader("Percentile Chart of Rent Prices")

#AGGREGATE FOR PLOTTING
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

# --- PLOT ---
fig, ax = plt.subplots(figsize=(8, 4))

y_positions = range(len(agg))

for i, row in agg.iterrows():
    y = i

    # 10–90 percentile line
    ax.hlines(y, xmin=row["qu10"], xmax=row["qu90"], linewidth=8, alpha=0.2)

    # 25–75 percentile box
    ax.hlines(y, xmin=row["qu25"], xmax=row["qu75"], linewidth=8, alpha=0.4)

    # Median point
    ax.plot(row["qu50"], y, marker="o", markersize=10)

ax.set_yticks(list(y_positions))
ax.set_yticklabels(agg["district"])
ax.set_xlabel("Rent price (Median & Perzentile)")
ax.grid(axis='x', linestyle='--', alpha=0.3)

st.pyplot(fig)