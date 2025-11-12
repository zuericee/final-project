import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from drafts.cleaning_Wohnungsbestand import load_data

df = load_data()
print(df)

st.set_page_config(page_title="Wohnungsbestand Viewer", layout="wide")

st.header("Housing stock overview")

# Display the dataframe
st.subheader("Kombinierte Daten")
st.dataframe(df)

# Filter by year
years = sorted(df["jahr"].unique())
selected_year = st.selectbox("Jahr auswählen:", years)
filtered_df = df[df["jahr"] == selected_year]

st.write(f"**Daten für {selected_year}:**")
st.dataframe(filtered_df)