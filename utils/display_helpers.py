""" This file contains the utility functions for creating maps and visual elements """

import folium
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_folium import st_folium

session = st.session_state

LOCATION = (52.309033724116524, 4.967533318175478)
ZOOM_START = 13
TILES = "Cartodb Positron"
POPUP_FIELDS = ["fuuid", "bouwjaar", "gebruiksdo", "sloop", "transform"]

def display_dummy_sankey(data) -> go.Figure:
    """Create a dummy sankey plot, just to test the layout and interactivity"""

    df = pd.DataFrame(data)
    all_nodes = list(set(df["source"]).union(set(df["target"])))
    node_dict = {node: i for i, node in enumerate(all_nodes)}

    # Map the source and target to their respective indices
    df["source_id"] = df["source"].map(node_dict)
    df["target_id"] = df["target"].map(node_dict)

    # Create Sankey diagram
    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line={"color": "black", "width": 0.5},
                    label=all_nodes,
                ),
                link=dict(
                    source=df["source_id"],
                    target=df["target_id"],
                    value=df["Value"],
                    color=["#f0f0f0"] * len(df),  # Very light grey hex code
                ),
            )
        ]
    )

    return fig


@st.cache_data(experimental_allow_widgets=True)
def create_map(_gdf_bag, _gdf_bag_no_geom) -> folium.Map:
    """Create a map with the BAG data, color the buildings based on the 'transform' column"""

    # Create a new GeoDataFrame with updated 'transform' and 'sloop' columns
    _gdf_bag["transform"] = _gdf_bag_no_geom["transform"]
    _gdf_bag["sloop"] = _gdf_bag_no_geom["sloop"]

    def style_function(feature):
        transform_value = feature["properties"]["transform"]
        if transform_value:  # If 'transform' is True
            return {
                "fillColor": "#FF0000",
                "color": "#0000FF",
            }  # Red (or your chosen color)

        return {
            "fillColor": "#0000FF",
            "color": "#FF0000",
        }  # Blue (or your chosen color)

    m = folium.Map(location=LOCATION, zoom_start=ZOOM_START, tiles=TILES)
    folium.GeoJson(
        _gdf_bag,
        style_function=style_function,
        popup=folium.GeoJsonPopup(
            fields=POPUP_FIELDS,
        ),
    ).add_to(m)

    return st_folium(m, use_container_width=True)


def create_project_map(_gdf_bag) -> folium.Map:
    """Create a map with the BAG data, color the buildings based on the 'transform' column"""

    # Create a new GeoDataFrame with updated 'transform' and 'sloop' columns

    def style_function(feature):
        """Style function for the GeoJson layer"""
        transform_value = feature["properties"]["transform"]
        if transform_value:  # If 'transform' is True
            return {
                "fillColor": "#FF0000",
                "color": "#0000FF",
            }  # Red (or your chosen color)

        return {
            "fillColor": "#0000FF",
            "color": "#FF0000",
        }  # Blue (or your chosen color)

    m = folium.Map(location=LOCATION, zoom_start=ZOOM_START, tiles=TILES)
    folium.GeoJson(
        _gdf_bag,
        style_function=style_function,
        popup=folium.GeoJsonPopup(
            fields=POPUP_FIELDS,
        ),
    ).add_to(m)

    return st_folium(m, use_container_width=True)


def display_project_shape_diagram(coords) -> plt.Figure:
    """Display the shape of the selected project"""
    x_coords = [point[0] for point in coords[0]]
    y_coords = [point[1] for point in coords[0]]

    # Close the polygon (Matplotlib expects the first and last points to be the same)
    x_coords.append(x_coords[0])
    y_coords.append(y_coords[0])

    # Create the plot
    fig, ax = plt.subplots(figsize=(1, 1))  # Set smaller figure size
    ax.plot(x_coords, y_coords, color="red")

    # Remove labels and axes
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_xticks([])  # Remove x ticks
    ax.set_yticks([])  # Remove y ticks
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Display in Streamlit
    return fig


def display_project_data(df, selected_point_id, coords):
    """Display the data of the selected project"""

    data = df.loc[df["fuuid"] == selected_point_id]

    col1, col2 = st.columns(2)
    with col1:
        st.title(selected_point_id[0:8])
        st.write("Bouwjaar:", int(data.iloc[0]["bouwjaar"]))
        st.write("Gebruiksdoel:", data.iloc[0]["gebruiksdo"])
        sloop = st.selectbox("Sloop", [True, False], index=0)
        transform = st.selectbox("Transform", [True, False], index=0)
        project_type = st.selectbox("Project type", ["Biobased", "Regulier"], index=0)
        button = st.button("Save changes")
        if button:
            st.success("Changes saved")

    with col2:
        fig = display_project_shape_diagram(coords)
        st.pyplot(fig, use_container_width=False)


def create_scenario_comparison():
    """Compares scenarios and returns a bar chart."""
    scenario_dfs = {}
    for key, value in session.scenarios.items():
        scenario_dfs[key] = pd.DataFrame(value["building_profiles"])

    combined_df = pd.concat(scenario_dfs.values(), keys=scenario_dfs.keys())
    combined_df.reset_index(level=0, inplace=True)
    melted_df = combined_df.melt(
        id_vars="level_0", var_name="Gebouwprofiel", value_name="Totale impact"
    )
    melted_df.rename(columns={"level_0": "Scenario"}, inplace=True)

    fig = px.bar(
        melted_df,
        x="Scenario",
        y="Totale impact",
        # Or use y="Normalized Share" if you calculated relative shares
        color="Gebouwprofiel",
        barmode="stack",  # Create stacked bars
        title="Stacked Bar Chart of Gebouwprofiel Impact Across Scenarios",
    )
    return fig
