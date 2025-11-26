import streamlit as st
import pandas as pd
import openpyxl

st.set_page_config(page_title="Can you afford to live in Zurich?", layout="wide")

homepage = st.Page("pages/homepage.py", title="Can you afford to live in Zurich?")

housing_stock_page = st.Page("pages/data_overview_housing.py", title="Housing Data Overview")

population_page = st.Page("pages/data_overview_population.py", title="Population Data Overview")

rent_page = st.Page("pages/data_overview_rent.py", title="Rent Data Overview")

user_pages = [homepage, housing_stock_page, population_page, rent_page]

import streamlit as st

# Custom CSS
st.markdown("""
    <style>
        /* Sidebar background color */
        [data-testid="stSidebar"] {
            background-color: #3cb371; /* mediumseagreen */
        }
        
        /* Sidebar text color */
        [data-testid="stSidebar"] * {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Light green background for each radio/select option */
section[data-testid="stSidebar"] div[data-baseweb="radio"] > div,
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: #8fd3a8 !important;  /* light green */
    border-radius: 6px;
}

/* Also lighten the dropdown menu options */
section[data-testid="stSidebar"] div[data-baseweb="option"] {
    background-color: #8fd3a8 !important;
}
</style>
""", unsafe_allow_html=True)

pg = st.navigation(user_pages, position="sidebar", expanded=True)

pg.run()