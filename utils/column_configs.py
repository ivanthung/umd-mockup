import streamlit as st

summary_df = {
    "Percentage realized": st.column_config.ProgressColumn(
        "Percentage realized",
        help="Percentage van de functie dat gerealiseerd is.",
        format="",
        min_value=0,
        max_value=100,
    )
}

impact_df = {
    "Share of total impact": st.column_config.ProgressColumn(
        "Share of total impact",
        help="Percentage van de totale impact van het gebouwprofiel.",
        format="",
        min_value=0,
        max_value=100,
    )
}

split_column = {
    "value": st.column_config.NumberColumn(
        "Value", min_value=0.0, max_value=1.0, step=0.01, required=True
    ),
}

# Path: utils/column_configs.py
