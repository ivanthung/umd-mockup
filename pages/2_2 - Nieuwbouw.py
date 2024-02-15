# Realiseren via gebouwprofielen.
# Percentage laagbouw, percentage hoogbou, etc.
# Voor elke percentage mixed use toren realiseren we x aantal m2 woningen, kantoren, horeca, etc.
# voor elke percentage kantoorgebouw realiseren we x aantal m2 kantoren.

import streamlit as st
import pandas as pd
import numpy as np
import utils.layout as layout

layout.set_page_title("Keuze nieuwbouw")
session = st.session_state

# Invoerdata
building_need_projection = {"Woningen": 600}
overige_needs_projection_m2 = {"Kantoren": 10000, "Horeca": 5000, "Utiliteits": 3000}
woning_typologie_m2 = {"Groot": 120, "Klein": 60, "Medium": 80}
gebouwprofielen = {
    "Mixed_used_toren": {
        "split": {"Woningen": 0.6, "Kantoren": 0.1, "Horeca": 0.1},
        "impact_m2": 500,
    },
    "Kantoorgebouw": {"split": {"Kantoren": 1}, "impact_m2": 500},
    "Laagbouw": {"split": {"Woningen": 1}, "impact_m2": 500},
    "Hoogbouw": {"split": {"Woningen": 1}, "impact_m2": 300},
}



col1, col2 = st.columns(2)
with col1:
    st.write("Totaal te realiseren woningen:", building_need_projection["Woningen"])
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

with col2:
    m2_totaal = list(slider.values()) * np.array(list(woning_typologie_m2.values()))
    chart_data = pd.DataFrame(((m2_totaal),), columns=slider.keys())

    st.write("M2 per woningtypologie")
    st.bar_chart(chart_data)

# Metrics of the projected needs
st.write("### Woningen per typologie")
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
