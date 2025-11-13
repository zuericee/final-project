import streamlit as st
import pandas as pd
import openpyxl

st.set_page_config(page_title="Can you afford to live in Zurich?", layout="wide")

homepage = st.Page("pages/homepage.py", title="Homepage")

housing_stock_page = st.Page("pages/data_overview_housing.py", title="Housing Data Overview")

population_page = st.Page("pages/data_overview_population.py", title="Population Data Overview")

rent_page = st.Page("pages/data_overview_rent.py", title="Rent Data Overview")

user_pages = [homepage, housing_stock_page, population_page, rent_page]

pg = st.navigation(user_pages, position="sidebar", expanded=True)

pg.run()