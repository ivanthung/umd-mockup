
import streamlit as st
import utils.utils as utils

st.set_page_config(page_title="Resultaten", layout="wide")
session = st.session_state

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

st.title("Resultaten")
fig = utils.display_dummy_sankey(session.gdf_bag , mfa_data)
st.plotly_chart(fig)

