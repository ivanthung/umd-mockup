import streamlit as st
import pandas as pd
import utils.utils as utils
import numpy as np
import matplotlib.pyplot as plt


# Cartography settings

bag_columns = [
    "transform",
    "use",
    "oppervlakt",
    "buurt_naam",
    "platdak_in",
    "bouwjaar",
]

st.set_page_config(layout="wide", page_title="Urban Mining Dashboard")
session = st.session_state

col1, col2 = st.columns((1, 5))
with col1:
    st.image("resources/Amsterdam City.png", width=200)

with col2:
    st.title("Zuid-oost projecten")

st.divider()
col1, col2 = st.columns(2)

with col1:
    st_data = utils.create_project_map(session.geometry_bag)

with col2:
    try:
        selected_point_id = st_data.get("last_active_drawing", {}).get("properties", {}).get("fuuid")
        coords = st_data.get("last_active_drawing", {}).get("geometry", {}).get("coordinates")
        utils.display_project_data(df = session.gdf_bag, selected_point_id= selected_point_id, coords=coords)
    except:
        st.write("Please select a project on the map")

st.divider()

cola, colb, colc = st.columns(3)

st.write(
    "Here's some dummy text for the results of the analysis. We can add more metrics and visualizations as needed."
)


print("Ran at: ", pd.Timestamp.now())
