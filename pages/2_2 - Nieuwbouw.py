# Realiseren via gebouwprofielen.
# Percentage laagbouw, percentage hoogbou, etc.
# Voor elke percentage mixed use toren realiseren we x aantal m2 woningen, kantoren, horeca, etc.
# voor elke percentage kantoorgebouw realiseren we x aantal m2 kantoren.

import streamlit as st
import pandas as pd
import numpy as np
import utils.layout as layout
from streamlit_extras.add_vertical_space import add_vertical_space

layout.set_page_title("Keuze nieuwbouw")
session = st.session_state

# Invoerdata
building_need_projection = {"Woningen": 600}
overige_needs_projection_m2 = {"Kantoren": 10000, "Horeca": 5000, "Utiliteits": 3000}
woning_typologie_m2 = {"Groot": 120, "Klein": 60, "Medium": 80}
building_profiles = {
    "Mixed_used_toren": {
        "split": {"Woningen": 0.6, "Kantoren": 0.1, "Horeca": 0.1},
        "impact_m2": {"hybrid": 300, "secondary": 100, "regular":500},
        "min_m2": 500,
    },
    "Kantoorgebouw": {"split": {"Kantoren": 1}, "impact_m2": {"hybrid": 100, "secondary": 200, "regular":500}, "min_m2": 1000},
    "Laagbouw": {"split": {"Woningen": 1}, "impact_m2": {"hybrid": 100, "secondary": 200, "regular":500},  "min_m2": 120},
    "Multi-family": {"split": {"Woningen": 1}, "impact_m2": {"hybrid": 60, "secondary": 30, "regular":100},  "min_m2": 480},
}

col1, col2, col3 = st.columns((3,1,3))
with col1:
    st.write("Kies percentage per woningtypologie.")

    slider = {
        w: st.slider(
            min_value=0,
            max_value=100,
            label=w,
            value=33,
        )
        for w in woning_typologie_m2.keys()
    }
    totaal = sum(slider.values())

    if (totaal) > 100:
        st.warning(f"Totaal percentage: {totaal}% is groter dan 100%.")
    else:
        st.success(f"Totaal percentage: {totaal}%")

with col3:
    m2_totaal = list(slider.values()) * np.array(list(woning_typologie_m2.values()))
    chart_data = pd.DataFrame(((m2_totaal),), columns=slider.keys())

    st.write("M2 per woningtypologie")
    st.bar_chart(chart_data)

# Metrics of the projected needs
    
    columns = st.columns(len(slider))
    for i, (key, value) in enumerate(slider.items()):
        with columns[i]:
            woningen = int(value / 100 * building_need_projection["Woningen"])
            label = f"{key} ({woning_typologie_m2[key]} m2)"
            st.metric(
                value=woningen,
                label=label,
                delta=f"{value}%",
            )

add_vertical_space(2)
st.divider()
st.write("### Gebouwprofielen")

if "building_profile" not in session:
    session.building_profile = {}  # Initialize as a list

col1, col2, col3 = st.columns((1,1,1))

bu_ty = list(building_profiles.keys())
se_ty = unique_impact_keys = {key for profile in building_profiles.values() for key in profile['impact_m2'].keys()}

building_types = col2.selectbox("Gebouwtype", bu_ty)
secondary_type = col3.selectbox("Profiel", se_ty)

if (col1.button("Create")):
    session.building_profile[building_types] = { secondary_type : 0 }

col1, col2, col3 = st.columns((3,1,3))
for p in session.building_profile.keys():
    with col1:
        st.slider(
            key = p,
            min_value=0,
            max_value=100,
            label=p,
            value=0,
        )