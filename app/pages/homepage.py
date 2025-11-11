import streamlit as st
import pandas as pd

st.title("Can you afford to live in Zurich")

st.header("Project overview")

st.header("Data overview")

df_housing = pd.read_csv("/Users/celineschwarz/github-projects/final-project/app/data/Bevoelkerung_nach_Stadtquartier.csv")

col_data, spacer, col_chart = st.columns((0.8, 0.05, 1))

with col_data:
    st.subheader("Raw Data: Population by District")
    st.dataframe(df_housing)

with col_chart:
    st.subheader("Data Overview")
    st.markdown("Placeholder for charts")


