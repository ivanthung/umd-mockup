""" Interface page to edit the building profiles and saving them to the session state.
ToDo: save this to a file and load it from a file"""

import pandas as pd
import streamlit as st

from utils.buildingdata import BuildingData
from utils.column_configs import split_column
from utils.layout import set_page_title

print("rerun at time: ", pd.Timestamp.now())
set_page_title("Edit building profiles")
session = st.session_state

if "BuildingData" not in session:
    session.BuildingData = BuildingData()
    session.BuildingData.load_all_data()
BuildingData = session.BuildingData


def app():
    """Interface for editing the building profiles.
    Wrapped in an app function because of the helper functions"""

    editable_data = st.selectbox(
        "Select data to edit",
        options=BuildingData.editable_data.keys(),
        index=1,
    )

    if editable_data == "building_profiles":
        for profile, profile_data in BuildingData.editable_data[editable_data].items():
            edit_existing_profile(profile, profile_data)
        st.text_input(
            "Add new profile", key="new_profile_name", on_change=add_new_profile
        )

    else:
        st.write(editable_data)
        st.dataframe(BuildingData.editable_data[editable_data])

    st.write("DEBUG INFO")
    st.write(BuildingData.building_profiles)


def edit_existing_profile(profile, profile_data):
    # Add a data editor for the profile data

    with st.expander(profile):
        col1, col2, col3, col4 = st.columns(4)

        description = col1.text_area(
            "Description",
            value=profile_data["description"],
            key=f"{profile}_description",
        )
        impact_m2 = col2.data_editor(
            profile_data["impact_m2"], key=f"{profile}_impact_m2", num_rows="dynamic"
        )
        split = col3.data_editor(
            profile_data["split"], key=f"{profile}_split", column_config=split_column
        )
        min_m2 = col4.number_input(
            "Minimum m2", value=profile_data["min_m2"], key=f"{profile}_min_m2"
        )

        BuildingData.update_profile_impact(profile, impact_m2)
        BuildingData.update_profile_min_m2(profile, min_m2)
        BuildingData.update_profile_description(profile, description)
        if not BuildingData.update_profile_split(profile, split):
            col3.error(f"Splits don't add up to 1")


def add_new_profile():
    # Collect new profile information from the user (e.g., using text inputss{}
    new_profile_data = BuildingData.get_profile_template()
    BuildingData.add_building_profile(session.new_profile_name, new_profile_data)


if __name__ == "__main__":
    app()
