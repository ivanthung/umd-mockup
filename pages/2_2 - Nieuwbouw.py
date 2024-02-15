# Needs van woningen in een graph.
# Daarna verhoudingen van hoeveelheid groot, klein en medium in percentages. 
# Dit weergeven als m2. 

import streamlit as st
import pandas as pd
import numpy as np

# Invoerdata
building_need_projection = {"Woningen": 600}
overige_needs_projection_m2 = {"Kantoren": 10000, "Horeca": 5000, "Utiliteits": 3000}
woning_typologie_m2 = {"Groot": 120, 
                       "Klein": 60,
                       "Medium": 80}
gebouwprofielen = {
    "Mixed_used_toren": {
        "split": {"Woningen": 0.6, "Kantoren": 0.1, "Horeca": 0.1},
        "impact_m2": 500,
    },
    "Kantoorgebouw": {"split": {"Kantoren": 1}, "impact_m2": 500},
    "Laagbouw": {"split": {"Woningen": 1}, "impact_m2": 500},
    "Hoogbouw": {"split": {"Woningen": 1}, "impact_m2": 300}
}

col1, col2 = st.columns(2)
with col1:
    st.write("Totaal te realiseren woningen:", building_need_projection['Woningen'])
    st.write("Kies percentage per woningtypologie.")
    
    slider = {'groot': st.slider(min_value=0, max_value=100, label="Groot", value=33),
               'klein': st.slider(min_value=0, max_value=100, label="Klein", value=33),
               'medium': st.slider(min_value=0, max_value=100, label="Medium", value=33)}
    totaal = slider['groot']+slider['klein']+slider['medium']

st.write('Totaal percentage"', totaal)
if((totaal) > 100):
    st.warning("Totaal is groter than 100%")

with col2:
    chart_data = pd.DataFrame(
            ((slider['groot'], slider['klein'], slider['medium']),),
            columns=slider.keys())

    st.bar_chart(chart_data)


# st.info("test")


