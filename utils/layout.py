import streamlit as st
import utils.utils as utils

def set_page_title(title: str, divider: bool = True) -> None:
    st.set_page_config(page_title=title, layout="wide")
    col1, col2 = st.columns((1, 5))
    
    with col1:
        st.image("resources/Metabolic_logo.png", width=100)
    
    with col2:
        st.title(title)
    
    st.divider() if divider else None

def save_scenario_form(to_file= False,**kwargs) -> None:
    """ Displays the form to save a scenario to the session state. Input as kwargs all the variables that need to be saved with their right naming."""
    
    with st.form("scenario_form"): 
        scenarion_name = st.text_input("Scenario name", value="Scenario 1")
        submit_button = st.form_submit_button("Add scenarios to results page") 
        if submit_button:
            if "scenarios" not in st.session_state:
                st.session_state.scenarios = {}  
            st.success(f"Scenario '{scenarion_name}' saved successfully!")
    if not to_file:
        utils.save_scenario_to_file()
