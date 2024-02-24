"""
This page is used to set the mix of building types to be used in a scenario.
It saves the scenario to the session state and to a file.
"""

import streamlit as st
import pandas as pd
import numpy as np
from utils.buildingdata import BuildingData
from utils import layout
from utils import data_manager
from utils import calculations as calc
from utils import utils
from utils import column_configs

layout.set_page_title("Keuze nieuwbouw")
session = st.session_state

data_manager.load_scenario_from_file()
data_manager.load_first_scenario()

if "BuildingData" not in session:
    session.BuildingData = BuildingData()
    session.BuildingData.load_all_data()
BuildingData = session.BuildingData

st.write("Here a lot of text describing what you need to do here.")

tabs1, tabs2 = st.tabs(["Woningtypologie", "Gebouwprofielen"])
if "building_size_slider" not in session:
    session.building_size_slider = {}
    for key in BuildingData.woning_typologie_m2.keys():
        session.building_size_slider[key] = 33

# Selection of mix of living sizes.
with tabs2:
    col1, col2, col3 = st.columns((3, 1, 3))
    with col1:
        st.write("Kies percentage per woningtypologie.")
        session.building_size_slider = {
            w: st.slider(
                key=w,
                min_value=0,
                max_value=100,
                label=w,
                value=session.building_size_slider.get(w, 33),
            )
            for w in BuildingData.woning_typologie_m2.keys()
        }
        totaal = sum(session.building_size_slider.values())
        if (totaal) > 100:
            st.warning(f"Totaal percentage: {totaal}% is groter dan 100%.")
        else:
            st.success(f"Totaal percentage: {totaal}%")
    with col3:
        m2_totaal = list(session.building_size_slider.values()) * np.array(
            list(BuildingData.woning_typologie_m2.values())
        )
        chart_data = pd.DataFrame(
            ((m2_totaal),), columns=session.building_size_slider.keys()
        )
        st.write("M2 per woningtypologie")
        st.bar_chart(chart_data)

    # Generate metrics of the projected needs
    housing_needs_m2 = calc.calculate_total_amount_of_houses_per_type(
        BuildingData.woning_typologie_m2,
        session.building_size_slider,
        BuildingData.needs["dwelling_needs"]["Woningen"],
    )
    # Generating the building profile sliders

with tabs1:
    if "building_profile" not in session:
        session.building_profile = {}

    col1, col2, col3 = st.columns((1, 1, 1))

    building_type_labels = list(BuildingData.building_profiles.keys())
    secondary_type_labels = unique_impact_keys = {
        key
        for profile in BuildingData.building_profiles.values()
        for key in profile["impact_m2"].keys()
    }

    building_type = col2.selectbox("Gebouwtype", building_type_labels)
    secondary_type = col3.selectbox("Profiel", secondary_type_labels)

    if col1.button("Voeg gebouw toe"):
        if building_type not in session.building_profile:
            session.building_profile[building_type] = {}
        session.building_profile[building_type][
            secondary_type
        ] = session.building_profile[building_type].get(secondary_type, 0)

    # Generating the building profile sliders and storing them in the session state
    def update_slider_value(profile, secondary_type, key):
        session.building_profile[profile][secondary_type] = session[key]

    col1, col2 = st.columns((1, 2))
    for profile in session.building_profile.keys():
        for secondary_type in session.building_profile[profile]:
            key = f"{profile}+{secondary_type}"
            min_value = BuildingData.building_profiles[profile]["min_m2"]
            with col1:
                st.slider(
                    key=key,
                    min_value=min_value,
                    max_value=min_value * 100,
                    label=f"{profile} -> {secondary_type}",
                    value=session.building_profile.get(profile, {}).get(
                        secondary_type, min_value
                    ),
                    on_change=update_slider_value,
                    args=(profile, secondary_type, key),
                )

impact_df = calc.create_building_profile_impact_table(
    BuildingData.building_profiles, session.building_profile
)
realisation_df = calc.create_building_profile_realisation_table(
    BuildingData.building_profiles,
    session.building_profile,
)
summary_df = calc.summarize_realisation_table(
    realisation_df,
    BuildingData.needs["other_needs"],
    {"Woningen": sum(housing_needs_m2.values())},
)

col2.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True,
    column_config=column_configs.summary_df,
)
col2.dataframe(
    impact_df,
    use_container_width=True,
    hide_index=True,
    column_config=column_configs.impact_df,
)
col2.dataframe(realisation_df, use_container_width=True, hide_index=True)

st.markdown("##")
layout.save_scenario_form(
    to_file=False,
    building_profiles=session.building_profile,
    woning_typologie_m2=session.building_size_slider,
    impact_df=impact_df,
    realisation_df=realisation_df,
    summary_df=summary_df,
)
