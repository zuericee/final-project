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

# Optional: district filter
if 'district' in df.columns:
    districts = df['district'].unique()
    selected_districts = st.sidebar.multiselect("Select District(s)", districts, default=districts)
else:
    df['district'] = "All"
    selected_districts = ["All"]

# Filter the dataframe
df_filtered = df[
    (df['year'] == selected_year) &
    (df['unit_type'] == selected_raum) &
    (df['district'].isin(selected_districts))
]

# Display filtered table
st.subheader(f"Filtered Data: {selected_year}, {selected_raum}")
st.dataframe(df_filtered)
