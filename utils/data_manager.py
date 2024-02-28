""" Handles the loading and saving of spatial data and scenarios in the session state.
Needs to be imported in all pages that use spatial data or scenarios."""

import pathlib
import pickle
from copy import deepcopy

import geopandas as gpd
import numpy as np
import streamlit as st

session = st.session_state

BASE_PATH = pathlib.Path(__file__).resolve().parent.parent

FILE_LOCATION = (
    BASE_PATH / "spatial_data" / "final" / "bag-ams-zuidoost-platdak-buurt.shp"
)


def load_bag_data():
    """
    Load the BAG data and create a dummy column for the transformation and demolition of buildings.
    Saves data in the session state variable as geometry_bag and gdf_bag
    """
    if "gdf_bag" in session:
        return True

    try:
        with st.spinner("Loading spatial data in session"):
            gdf_bag = gpd.read_file(FILE_LOCATION)
            gdf_bag = gdf_bag.sample(n=200).reset_index(drop=True)
            gdf_bag["sloop"] = True
            gdf_bag["transform"] = False
            # create some random categories for the buildings.
            gdf_bag["use"] = np.random.choice(
                ["Apartment", "Office", "Low-Rise"], size=len(gdf_bag)
            )
            session.geometry_bag = gdf_bag
            session.gdf_bag = gdf_bag.drop(columns="geometry")
            return True

    except FileNotFoundError:
        st.error("No spatial data found")
        return False


def load_scenario_from_file(scenario_collection_name="scenario_data", load_new=False):
    """
    Load the data from a pickle assign it as a dictionary to the session state variable.
    Only execute this function if the session state variable does not contain a key called "scenarios"
    Add load_new = True to force loading a new file and overwrite the current session state variable.
    """
    if "scenarios" not in session or load_new:
        try:
            with open(f"scenarios/{scenario_collection_name}.pickle", "rb") as f:
                loaded_data = pickle.load(f)
                session.scenarios = loaded_data
                st.success("Scenarios loaded")
        except Exception as e:
            st.error("No scenarios found to load")
            print(e)


def load_first_scenario():
    """Load the first scenario from the session state variable"""

    if "scenarios" in session and len(session.scenarios):
        session.building_profile = session.scenarios[list(session.scenarios.keys())[0]][
            "building_profiles"
        ]
        session.building_size_slider = session.scenarios[
            list(session.scenarios.keys())[0]
        ]["woning_typologie_m2"]
        print("Loaded first scenario from file")
    else:
        print("No scenario found")


def save_scenario_to_file(filename="scenario_data"):
    """Save the data from the session state variable to a pickle file"""
    with open(f"scenarios/{filename}.pickle", "wb") as f:
        pickle.dump(session.scenarios, f)


def save_scenario_to_session_state(scenario_name, data_to_save: dict):
    """Save the data that we want to keep for the current scenario to the scenario's session state variable"""
    session.scenarios[scenario_name] = {}
    for attribute, value in data_to_save.items():
        session.scenarios[scenario_name][attribute] = deepcopy(value)
