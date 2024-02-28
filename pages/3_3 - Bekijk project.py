"""
This page allows you to select individual projects and vies their state.
It does not yet allow you to update the state, even though buttons are present.
"""

import streamlit as st

from utils import data_manager, layout, display_helpers

session = st.session_state
layout.set_page_title("Pas project aan")
data_manager.load_bag_data()

col1, col2 = st.columns(2)
with col1:
    interaction_data = display_helpers.create_project_map(session.geometry_bag)
    st.write(interaction_data)

with col2:
    try:
        selected_point_id = (
            interaction_data.get("last_active_drawing", {})
            .get("properties", {})
            .get("fuuid")
        )
        coords = (
            interaction_data.get("last_active_drawing", {})
            .get("geometry", {})
            .get("coordinates")
        )
        display_helpers.display_project_data(
            df=session.gdf_bag, selected_point_id=selected_point_id, coords=coords
        )
    except AttributeError:
        st.write("Please select a project on the map")
