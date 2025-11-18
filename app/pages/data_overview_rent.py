import streamlit as st
import pandas as pd
import plotly.express as px

from drafts.cleaning_rent import load_rent_data

df = load_rent_data()
    
# Page setup
st.set_page_config(page_title="Miete Viewer", layout="wide")
st.header("Rent Prices in Zurich per District")

# Sidebar filters
st.sidebar.header("Filter Options")

# Year filter
years = sorted(df['year'].dropna().unique())
selected_year = st.sidebar.selectbox("Select Year", years)

# Geografischer Raum filter
raum_types = df['unit_type'].unique()
selected_raum = st.sidebar.selectbox("Select Geografischer Raum", raum_types)

st.sidebar.header("Filter Options")

#Number of rooms filter
rooms = df['zimmersort'].dropna().unique()
selected_rooms = st.sidebar.selectbox("Anzahl Zimmer", rooms)

#Brutto / Netto filter
rent_types = df['price_type'].dropna().unique()
selected_rent_type = st.sidebar.selectbox("Brutto / Netto", rent_types)

#Preis pro m² / pro Wohnung filter
unit_kinds = df['unit_kind'].dropna().unique()
selected_unit = st.sidebar.selectbox("Preisart", unit_kinds)

# Filter the dataframe
df_filtered = df[
    (df['year'] == selected_year) &
    (df['unit_type'] == selected_raum) &
    (df['zimmersort'] == selected_rooms) &
    (df['price_type'] == selected_rent_type) &
    (df['unit_kind'] == selected_unit)
]

# Display filtered table
st.subheader(f"Filtered Data: {selected_year}, {selected_raum}")
st.dataframe(df_filtered)