import streamlit as st
import pandas as pd

st.set_page_config(page_title="Can you afford to live in Zurich?", layout="wide")

homepage = st.Page("pages/homepage.py", title="Homepage")

data_page = st.Page("pages/data_overview.py")

user_pages = [homepage, data_page]

pg = st.navigation(user_pages, position="sidebar", expanded=True)

pg.run()
