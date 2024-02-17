# Realiseren via gebouwprofielen.
# Todo: add logic to load data so that I don't have to do that everytime...

import streamlit as st
import pandas as pd
import numpy as np
import utils.layout as layout
import utils.calculations as calc
import utils.utils as utils
import utils.column_configs as column_configs
import plotly.express as px

layout.set_page_title("Keuze nieuwbouw")
session = st.session_state

utils.load_scenario_from_file()
utils.load_first_scenario()

st.write("Here a lot of text describing what you need to do here.")

# Invoerdata
dwelling_needs_projection = {"Woningen": 600}
other_needs_m2 = {"Kantoren": 10000, "Horeca": 5000, "Utiliteits": 3000}
woning_typologie_m2 = {"Groot": 120, "Klein": 60, "Medium": 80}
building_profiles = {
    "Mixed_used_toren": {
        "split": {"Woningen": 0.6, "Kantoren": 0.3, "Horeca": 0.1},
        "impact_m2": {"hybrid": 300, "secondary": 100, "regular": 500},
        "min_m2": 500,
    },
    "Kantoorgebouw": {
        "split": {"Kantoren": 1},
        "impact_m2": {"hybrid": 100, "secondary": 200, "regular": 500},
        "min_m2": 1000,
    },
    "Laagbouw": {
        "split": {"Woningen": 1},
        "impact_m2": {"hybrid": 100, "secondary": 200, "regular": 500},
        "min_m2": 120,
    },
    "Multi-family": {
        "split": {"Woningen": 1},
        "impact_m2": {"hybrid": 60, "secondary": 30, "regular": 100},
        "min_m2": 480,
    },
}

tabs1, tabs2 = st.tabs(["Woningtypologie", "Gebouwprofielen"])
if "building_size_slider" not in session:
    session.building_size_slider = {}
    for key in woning_typologie_m2.keys():
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
                value=session.building_size_slider.get(w, 33)
            )
            for w in woning_typologie_m2.keys()
        }
        totaal = sum(session.building_size_slider.values())
        if (totaal) > 100:
            st.warning(f"Totaal percentage: {totaal}% is groter dan 100%.")
        else:
            st.success(f"Totaal percentage: {totaal}%")

    with col3:
        m2_totaal = list(session.building_size_slider.values()) * np.array(list(woning_typologie_m2.values()))
        chart_data = pd.DataFrame(((m2_totaal),), columns=session.building_size_slider.keys())
        st.write("M2 per woningtypologie")
        st.bar_chart(chart_data)

    # Generate metrics of the projected needs
    housing_needs_m2 = calc.calculate_total_amount_of_houses_per_type(
        woning_typologie_m2, session.building_size_slider, dwelling_needs_projection["Woningen"]
    )
    # Generating the building profile sliders

with tabs1:
    if "building_profile" not in session:
        session.building_profile = {}

    col1, col2, col3 = st.columns((1, 1, 1))

    bu_ty = list(building_profiles.keys())
    se_ty = unique_impact_keys = {
        key
        for profile in building_profiles.values()
        for key in profile["impact_m2"].keys()
    }

    building_type = col2.selectbox("Gebouwtype", bu_ty)
    secondary_type = col3.selectbox("Profiel", se_ty)

    if col1.button("Voeg gebouwprofiel toe"):
        if building_type not in session.building_profile:
            session.building_profile[building_type] = {}
        session.building_profile[building_type][secondary_type] = session.building_profile[building_type].get(secondary_type, 0)

    # Generating the building profile sliders and storing them in the session state
    def update_slider_value(profile, secondary_type, key):
        session.building_profile[profile][secondary_type] = session[key]

    col1, col2 = st.columns((1, 2))
    for profile in session.building_profile.keys():
        for secondary_type in session.building_profile[profile]:
            key = f"{profile}+{secondary_type}"
            min_value = building_profiles[profile]["min_m2"]
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
    building_profiles, session.building_profile
)
realisation_df = calc.create_building_profile_realisation_table(
    building_profiles,
    session.building_profile,
)
summary_df = calc.summarize_realisation_table(realisation_df,
                                              other_needs_m2,
                                            {'Woningen': sum(housing_needs_m2.values())}
                                            )

col2.dataframe(summary_df, use_container_width=True,
               hide_index=True,
               column_config=column_configs.summary_df)
col2.dataframe(impact_df, use_container_width=True, hide_index=True, 
               column_config= column_configs.impact_df)
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
