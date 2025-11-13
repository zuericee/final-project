import streamlit as st
import pandas as pd
import plotly.express as px

from drafts.cleaning_Wohnungsbestand import load_data

df = load_data()

st.set_page_config(page_title="Wohnungsbestand Viewer", layout="wide")

st.header("Housing stock overview")

# Display the dataframe - delete later
st.subheader("Combined Housing Stock Data")
st.dataframe(df)

# Filter by year
years = sorted(df["jahr"].unique())
selected_year = st.selectbox("Select year:", years)
filtered_df = df[df["jahr"] == selected_year]

st.write(f"**Daten für {selected_year}:**")
st.dataframe(filtered_df)

st.subheader("How has the total housing stock in Zurich changed over time?")

# Filter rows where "city district" == "Ganze Stadt"
filtered_df = df[df['City district'] == 'Ganze Stadt']

# Create Plotly line chart
fig = px.line(
    filtered_df,
    x='jahr',
    y='Total',
)

# Show in Streamlit
st.plotly_chart(fig)