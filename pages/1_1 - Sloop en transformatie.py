"""
In this page you can view the data of the BAG dataset and change the transform and sloop columns,
both through a table and with a randomizer button.
It takes a randoms sample from the BAG dataset and initializes some random default dummy values, such as gebruik.
"""

import numpy as np
import pandas as pd
import streamlit as st

from utils import calculations as calc
from utils import data_manager, display_helpers, layout

session = st.session_state
layout.set_page_title("Sloop en nieuwbouw")
data_manager.load_bag_data()


def update_data():
    """Check this out for the data editor: https://github.com/streamlit/streamlit/issues/7749#issuecomment-1910188358"""
    for idx, change in session.changes["edited_rows"].items():
        for label, value in change.items():
            session.gdf_bag.loc[idx, label] = value


col1, col2 = st.columns(2)
with col1:
    st_data = display_helpers.create_map(session.geometry_bag, session.gdf_bag)

with col2:
    st.data_editor(
        session.gdf_bag,
        key="changes",
        on_change=update_data,
        column_order=[
            "sloop",
            "transform",
            "use",
            "oppervlakt",
            "buurt_naam",
            "bouwjaar",
        ],
        height=500,
    )
    col3, col4 = st.columns(2)

    with col3:

        def refresh_map():
            """Clear the cache of the map to force a refresh."""
            display_helpers.create_map.clear()

        st.button("Refresh map", on_click=refresh_map)
        # We can do load the selected point here if necessary.

    with col4:
        st.write("Transform a percentage of all offices, picked at random")
        transform_slider = st.slider(
            "Percentage of transformed offices", 0, 100, 50, 10
        )

        def update_office_button():
            """necessary evil function to update the data in the dataframe."""
            session.gdf_bag.loc[session.gdf_bag["use"] == "Office", "transform"] = (
                np.random.choice(
                    [True, False],
                    size=len(session.gdf_bag[session.gdf_bag["use"] == "Office"]),
                    p=[transform_slider / 100, 1 - transform_slider / 100],
                )
            )
            display_helpers.create_map.clear()

        st.button("Transform random office buildings", on_click=update_office_button)

st.divider()
st.title("Results")

col1, col2 = st.columns(2)
with col1:
    cola, colb, colc = st.columns(3)

    st.write(
        "Here's some dummy text for the results of the analysis. We can add more metrics and visualizations as needed."
    )
    with cola:
        st.metric("Herbestemde kantoren", session.gdf_bag["transform"].sum())
    with colb:
        st.metric("Gesloopte gebouwen", session.gdf_bag["sloop"].sum())
    with colc:
        st.metric(
            "Behouden woningen",
            session.gdf_bag.shape[0] - session.gdf_bag["sloop"].sum(),
        )
with col2:
    mfa_data = calc.create_mfa_data()
    fig = display_helpers.display_dummy_sankey(mfa_data)
    st.plotly_chart(fig)

print("Ran at: ", pd.Timestamp.now())
