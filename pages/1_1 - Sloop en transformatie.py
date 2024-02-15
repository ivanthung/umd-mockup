import streamlit as st
import pandas as pd
import utils.utils as utils
import numpy as np

# Cartography settings

bag_columns = [
    "sloop",
    "transform",
    "use",
    "oppervlakt",
    "buurt_naam",
    "bouwjaar",
]
mfa_data = {
    "source": [
        "Apartment",
        "Apartment",
        "Apartment",
        "Apartment",
        "Office",
        "Office",
        "Office",
        "Low-Rise",
        "Low-Rise",
        "Low-Rise",
    ],
    "target": [
        "Brick",
        "Wood",
        "Steel",
        "Stone",
        "Brick",
        "Steel",
        "Concrete",
        "Wood",
        "Steel",
        "Stone",
    ],
    "Value": [250, 100, 50, 25, 300, 200, 150, 150, 100, 75],
}

st.set_page_config(layout="wide", page_title="Urban Mining Dashboard")
session = st.session_state

if "gdf_bag" not in session:
    gdf_bag = utils.load_data()
    session.geometry_bag = gdf_bag
    session.gdf_bag = gdf_bag.drop(columns="geometry")


def update_data():
    """Check this out for the data editor: https://github.com/streamlit/streamlit/issues/7749#issuecomment-1910188358"""
    for idx, change in session.changes["edited_rows"].items():
        for label, value in change.items():
            session.gdf_bag.loc[idx, label] = value


col1, col2 = st.columns((1, 5))
with col1:
    st.image("resources/Amsterdam City.png", width=200)

with col2:
    st.title("Urban Mining Dashboard")
    st.write(
        "This is a mock-up of the Urban Mining Dashboard for internal testing. It is not connected to any real data."
    )

st.divider()
col1, col2 = st.columns(2)

with col1:
    st_data = utils.create_map(session.geometry_bag, session.gdf_bag)

with col2:
    st.data_editor(
        session.gdf_bag,
        key="changes",
        on_change=update_data,
        column_order=bag_columns,
        height=500,
    )
    col3, col4 = st.columns(2)

    with col3:

        def refresh_map():
            utils.create_map.clear()

        st.button("Refresh map", on_click=refresh_map)
        # We can do load the selected point here if necessary.

    with col4:
        st.write("Transform a percentage of all offices, picked at random")
        transform_slider = st.slider(
            "Percentage of transformed offices", 0, 100, 50, 10
        )

        def update_office_button():
            """necessary evil function to update the data in the dataframe."""
            session.gdf_bag.loc[
                session.gdf_bag["use"] == "Office", "transform"
            ] = np.random.choice(
                [True, False],
                size=len(session.gdf_bag[session.gdf_bag["use"] == "Office"]),
                p=[transform_slider / 100, 1 - transform_slider / 100],
            )
            utils.create_map.clear()

        st.button(
            "Transform random office buildings", on_click=update_office_button
        )

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
    fig = utils.display_dummy_sankey(session.gdf_bag , mfa_data)
    st.plotly_chart(fig)

print("Ran at: ", pd.Timestamp.now())
