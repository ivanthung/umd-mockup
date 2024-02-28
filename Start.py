""" Starting page for the Streamlit app"""

import streamlit as st
from utils import data_manager, layout

layout.set_page_title("About")
data_manager.load_bag_data()

st.markdown(""" Boilerplate dummy text for main page """)
