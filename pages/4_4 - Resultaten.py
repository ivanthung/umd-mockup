#todo
# add scenario loading and load first scenario.
# Report download button / layout. 

import streamlit as st
import utils.utils as utils
import utils.layout as layout
import utils.column_configs as column_configs


layout.set_page_title("Resultaten")
utils.load_scenario_from_file()
session = st.session_state
    
if 'scenarios' in session and len(session.scenarios):
    tabs = st.tabs(['Comparison'] +list(session.scenarios.keys()))
    to_delete = [] 

    with tabs[0]:
        col1, col2 = st.columns((1,2))
        with col1:
            st.write("Here you can compare the scenarios. More to come.")
        with col2:
            utils.display_scenario_comparison()

    for i, (scenario, scenario_data) in enumerate(session.scenarios.items()):
        with tabs[i+1]:
            st.dataframe(scenario_data['impact_df'], column_config=column_configs.impact_df)
            st.dataframe(scenario_data['summary_df'], column_config=column_configs.summary_df)
            if st.button("Remove scenario", key=f"remove_{scenario}"):
                to_delete.append(scenario)

    for scenario in to_delete:
        del session.scenarios[scenario]
        # utils.save_scenario_to_file()
        st.success(f"Scenario '{scenario}' removed from file.")
        st.rerun()
else: 
    st.write("No scenarios found")

st.divider()



def show_mfa():
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

    fig = utils.display_dummy_sankey(session.gdf_bag , mfa_data)
    st.plotly_chart(fig)

