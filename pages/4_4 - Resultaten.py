""" Results page with saving options and AI report generation. """

import streamlit as st

import utils.column_configs as column_configs
from utils import display_helpers, layout
from utils.ai_report import produce_report
from utils.reportgenerator import generate_report_pdf

layout.set_page_title("Resultaten")
layout.save_and_load_scenario_sidebar()
session = st.session_state

if "scenarios" in session and len(session.scenarios):
    tabs = st.tabs(["Comparison"] + list(session.scenarios.keys()))
    to_delete = []

    with tabs[0]:
        col1, col2 = st.columns((1, 2))
        comparison_fig = display_helpers.create_scenario_comparison()
        with col1:
            container = st.empty()

            if "ai_report_text" not in session:
                st.button(
                    "Create AI-generated report (experimental)",
                    on_click=produce_report,
                    args=(container,),
                )
            else:
                st.write(session["ai_report_text"])

                with st.spinner("Generating report..."):
                    pdf_bytes = generate_report_pdf(
                        session["ai_report_text"], {"comparison": comparison_fig}
                    )
                    st.download_button(
                        label="Download report",
                        data=pdf_bytes,
                        file_name="report.pdf",
                        mime="application/pdf",
                    )

        with col2:
            st.plotly_chart(comparison_fig)

    for i, (scenario, scenario_data) in enumerate(session.scenarios.items()):
        with tabs[i + 1]:
            st.dataframe(
                scenario_data["impact_df"], column_config=column_configs.impact_df
            )
            st.dataframe(
                scenario_data["summary_df"], column_config=column_configs.summary_df
            )
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
