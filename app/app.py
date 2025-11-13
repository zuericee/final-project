import streamlit as st
import pandas as pd
import openpyxl

st.set_page_config(page_title="Can you afford to live in Zurich?", layout="wide")

homepage = st.Page("pages/homepage.py", title="Homepage")

housing_stock_page = st.Page("pages/data_overview.py", title="Housing Data Overview")

user_pages = [homepage, housing_stock_page]

pg = st.navigation(user_pages, position="sidebar", expanded=True)

pg.run()
