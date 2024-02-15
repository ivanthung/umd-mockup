import streamlit as st
import pandas as pd
import utils.utils as utils
import numpy as np
import matplotlib.pyplot as plt
import utils.layout as layout

layout.set_page_title("Pas project aan")
session = st.session_state

bag_columns = [
    "transform",
    "use",
    "oppervlakt",
    "buurt_naam",
    "platdak_in",
    "bouwjaar",
]

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