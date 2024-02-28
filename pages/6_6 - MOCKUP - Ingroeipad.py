import streamlit as st
import plotly.express as px
import numpy as np


def create_s_curve(start_year, end_year, peak_value, peak_year):
    """
    Creates a list of values that follow an S-curve pattern.

    Args:
        start_year (int): The starting year of the S-curve.
        end_year (int): The ending year of the S-curve.
        peak_value (float): The peak value of the S-curve.
        peak_year (int): The year at which the peak value occurs.

    Returns:
        list: A list of values that follow an S-curve pattern.
    """

    # Calculate the number of years in the S-curve
    num_years = end_year - start_year + 1

    # Create a list of years
    years = np.linspace(start_year, end_year, num_years)

    # Define the S-curve function using the logistic function
    def s_curve(x):
        return peak_value / (1 + np.exp(-4 * (x - peak_year)))

    # Apply the S-curve function to the years
    s_curve_values = s_curve(years)

    return s_curve_values.tolist()


st.title("S-Curve Chart")

# Input Parameters
start_year = st.number_input("Start Year", value=2020)
end_year = st.number_input("End Year", value=2025)
peak_value = st.number_input("Peak Value", value=100)
peak_year = st.number_input("Peak Year", value=2023)

# Generate S-Curve Data
s_curve_values = create_s_curve(start_year, end_year, peak_value, peak_year)
years = list(range(start_year, end_year + 1))

# Create Plotly Chart
fig = px.line(x=years, y=s_curve_values)
fig.update_layout(title="S-Curve", xaxis_title="Year", yaxis_title="Value")

# Display in Streamlit
st.plotly_chart(fig)
