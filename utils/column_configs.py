import streamlit as st

summary_df =    {"Percentage realized": st.column_config.ProgressColumn(
     "Percentage realized",
        help="Percentage van de functie dat gerealiseerd is.",
            format="",
            min_value=0,
            max_value=100,
)
}

impact_df = {"Share of total impact": st.column_config.ProgressColumn(
     "Share of total impact",
        help="Percentage van de totale impact van het gebouwprofiel.",
            format="",
            min_value=0,
            max_value=100,
)
}


# Path: utils/column_configs.py