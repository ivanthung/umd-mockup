""" Contains re-usable visual components for the app."""
import os
import streamlit as st
from utils import utils
from utils import data_manager


def set_page_title(title: str, divider: bool = True) -> None:
    """Sets the page title and adds the Metabolic logo to the top of the page.
    Needs to be called at the start of every page."""
    st.set_page_config(page_title=title, layout="wide")
    col1, col2 = st.columns((1, 5))

    with col1:
        st.image("resources/Metabolic_logo.png", width=100)

    with col2:
        st.title(title)

    st.divider() if divider else None


def save_scenario_to_session_state_form(**kwargs) -> None:
    """Displays the form to save a scenario to the session state.
    Input as kwargs all the variables that need to be saved with their right naming."""

    with st.form("scenario_form"):
        scenarion_name = st.text_input("Scenario name", value="Scenario 1")
        submit_button = st.form_submit_button("Add scenarios to results page")
        if submit_button:
            if "scenarios" not in st.session_state:
                st.session_state.scenarios = {}
            data_manager.save_scenario_to_session_state(scenarion_name, kwargs)
            st.success(f"Scenario '{scenarion_name}' saved successfully!")


def save_and_load_scenario_sidebar() -> None:
    """Standard sidebar template to save and load scenarios."""
    with st.sidebar:
        load_scenario_collection()
        save_scenario_collection()


def load_scenario_collection() -> None:
    """Lists the files from the scenarios folder into a dropdown and has a button to open it."""
    scenario_collection = os.listdir("scenarios/")
    scenario_collection_trimmed = [filename[:-7] for filename in scenario_collection]

    with st.form("Load scenarios from file"):
        selected_scenario = st.selectbox(
            "Load scenarios from file", scenario_collection_trimmed
        )
        submit_button = st.form_submit_button("Load")
        if submit_button:
            print("loading scenario", selected_scenario)
            data_manager.load_scenario_from_file(selected_scenario, load_new=True)


def save_scenario_collection() -> None:
    """
    Displays the form to save a scenario collection with a name
    """

    with st.expander("Save scenarios to file"):
        with st.form("Save scenarios to file"):
            scenario_collection_name = st.text_input(
                "Scenario collection", value="Scenario collection 1"
            )
            submit_button = st.form_submit_button("Save scenarios to collection")
            if submit_button:
                data_manager.save_scenario_to_file(scenario_collection_name)
