import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import folium
from streamlit_folium import st_folium
import streamlit as st
import matplotlib.pyplot as plt

amsterdam_zuidoost = (52.309033724116524, 4.967533318175478)
zoom_start = 13
tiles = "Cartodb Positron"
popup_fields = ["fuuid", "bouwjaar", "gebruiksdo", "sloop", "transform"]
file_location = "spatial_data/final/bag-ams-zuidoost-platdak-buurt.shp"


def load_data() -> gpd.GeoDataFrame:
    """Load the BAG data and create a dummy column for the transformation and demolition of buildings"""

    gdf_bag = gpd.read_file(file_location)
    gdf_bag = gdf_bag.sample(n=200).reset_index(drop=True)
    gdf_bag["sloop"] = True
    gdf_bag["transform"] = False
    # create some random categories for the buildings.
    gdf_bag["use"] = np.random.choice(
        ["Apartment", "Office", "Low-Rise"], size=len(gdf_bag)
    )
    return gdf_bag


def display_dummy_sankey(gdf_bag, data) -> go.Figure:
    """Create a dummy sankey plot, just to test the layout and interactivity"""

    df = pd.DataFrame(data)

    print(gdf_bag.head())
    for s in df["source"].unique():
        df.loc[df["source"] == s, "Value"] = df.loc[df["source"] == s, "Value"] * len(
            gdf_bag[gdf_bag["use"] == s]
        )
    print(df.head())

    all_nodes = list(set(df["source"]).union(set(df["target"])))
    node_dict = {node: i for i, node in enumerate(all_nodes)}

    # Map the source and target to their respective indices
    df["source_id"] = df["source"].map(node_dict)
    df["target_id"] = df["target"].map(node_dict)

    # Calculate node values (assuming values represent incoming flow)

    # Create Sankey diagram
    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=all_nodes,
                ),
                link=dict(
                    source=df["source_id"],
                    target=df["target_id"],
                    value=df["Value"],
                    color="#f0f0f0"  # Very light grey hex code

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
        else:
            return {
                "fillColor": "#0000FF",
                "color": "#FF0000",
            }  # Blue (or your chosen color)

    m = folium.Map(location=amsterdam_zuidoost, zoom_start=zoom_start, tiles=tiles)
    folium.GeoJson(
        _gdf_bag,
        style_function=style_function,
        popup=folium.GeoJsonPopup(
            fields=popup_fields,
        ),
    ).add_to(m)

    return st_folium(m, use_container_width=True)

def create_project_map(_gdf_bag) -> folium.Map:
    """Create a map with the BAG data, color the buildings based on the 'transform' column"""

    # Create a new GeoDataFrame with updated 'transform' and 'sloop' columns
    
    def style_function(feature):
        transform_value = feature["properties"]["transform"]
        if transform_value:  # If 'transform' is True
            return {
                "fillColor": "#FF0000",
                "color": "#0000FF",
            }  # Red (or your chosen color)
        else:
            return {
                "fillColor": "#0000FF",
                "color": "#FF0000",
            }  # Blue (or your chosen color)

    m = folium.Map(location=amsterdam_zuidoost, zoom_start=zoom_start, tiles=tiles)
    folium.GeoJson(
        _gdf_bag,
        style_function=style_function,
        popup=folium.GeoJsonPopup(
            fields=popup_fields,
        ),
    ).add_to(m)

    return st_folium(m, use_container_width=True)

def display_project_shape_diagram(coords) -> plt.Figure:
    """ Display the shape of the selected project"""
    x_coords = [point[0] for point in coords[0]]
    y_coords = [point[1] for point in coords[0]]

    # Close the polygon (Matplotlib expects the first and last points to be the same)
    x_coords.append(x_coords[0]) 
    y_coords.append(y_coords[0])

    # Create the plot
    fig, ax = plt.subplots(figsize=(1, 1))  # Set smaller figure size
    ax.plot(x_coords, y_coords, color='red')

    # Remove labels and axes
    ax.set_xlabel("") 
    ax.set_ylabel("") 
    ax.set_xticks([])  # Remove x ticks
    ax.set_yticks([])  # Remove y ticks
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Display in Streamlit
    st.pyplot(fig,use_container_width=False) 

def display_project_data(df, selected_point_id, coords):
    """ Display the data of the selected project"""
    
    data = df.loc[df['fuuid'] == selected_point_id]

    col1, col2 = st.columns(2)
    with col1:
        st.title(selected_point_id[0:8])
        st.write('Bouwjaar:', int(data.iloc[0]['bouwjaar']))
        st.write('Gebruiksdoel:', data.iloc[0]['gebruiksdo'])
        sloop = st.selectbox('Sloop', [True, False], index=0)
        transform = st.selectbox('Transform', [True, False], index=0)
        project_type = st.selectbox('Project type', ['Biobased', 'Regulier'], index=0)
        button = st.button('Save changes')    
        if button:
            st.success(f"Changes saved")
    
    with col2:
        display_project_shape_diagram(coords)

