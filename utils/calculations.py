""" Generation of key calculations and tables"""

import pandas as pd


def create_building_profile_impact_table(
    building_profiles: dict, building_profiles_user_data: dict
) -> pd.DataFrame:
    """Create a table with the impact of the building profiles.
    args:
    Building profiles: the standard data for each profile.
    Building_profiles_user_data: the user input for each profile.
    Return: a pandas DataFrame with the impact of each building profiles.
    """
    impact_table = []
    for profile in building_profiles_user_data.keys():
        for secondary_type in building_profiles_user_data[profile]:
            impact_table.append(
                [
                    profile,
                    secondary_type,
                    building_profiles_user_data[profile][secondary_type],
                    building_profiles[profile]["impact_m2"][secondary_type]
                    * building_profiles_user_data[profile][secondary_type],
                ]
            )
    impact_df = pd.DataFrame(
        impact_table, columns=["Gebouwprofiel", "Secondary Type", "M2", "Totale impact"]
    )
    # Calculate the share of the imoact of the total impact of each profile
    impact_df["Share of total impact"] = (
        impact_df["Totale impact"] / impact_df["Totale impact"].sum() * 100
    )
    return impact_df


def create_building_profile_realisation_table(
    building_profiles: dict,
    building_profiles_user_data: dict,
) -> pd.DataFrame:
    """Create a table with actual realisation of gebruik fo reach of the building profiles."""
    realistion_table = []
    for profile, profile_data in building_profiles_user_data.items():
        for typology, split_percentage in building_profiles[profile]["split"].items():
            realized_m2 = split_percentage * sum(profile_data.values())
            realistion_table.append([profile, typology, realized_m2])

    return pd.DataFrame(
        realistion_table, columns=["Gebouwprofiel", "Gebruik", "Realized m2"]
    )


def calculate_total_amount_of_houses_per_type(
    m2_per_housing_type: dict,
    percentage_per_housing_type: dict,
    projected_houses: int,
) -> dict:
    """Multiplies the m2 per housing type with the percentage per housing type to get the amount of houses per housing type.
    Returns dict with amount of housing per type"""
    amount_of_houses = {}
    for key, value in m2_per_housing_type.items():
        amount_of_houses[key] = int(
            value * projected_houses * percentage_per_housing_type[key] / 100
        )
    return amount_of_houses


def summarize_realisation_table(
    realistion_df: pd.DataFrame,
    other_needs_m2: dict,
    dwelling_needs_m2: dict,
) -> pd.DataFrame:
    """
    Summarizes the realisation_table based on the 'Gebruik' column.
    Returns: a pandas DataFrame with the summarized realisation_table.
    """
    summary_df = pd.DataFrame(
        realistion_df.groupby("Gebruik")["Realized m2"].sum()
    ).reset_index()
    other_needs_m2.update(dwelling_needs_m2)
    summary_df["Needed m2"] = summary_df["Gebruik"].map(other_needs_m2)
    summary_df["Realized m2"] = summary_df["Realized m2"].astype(int)
    summary_df["Percentage realized"] = (
        summary_df["Realized m2"] / summary_df["Needed m2"] * 100
    )
    return summary_df


def create_mfa_data() -> dict:
    """Create a dict for the MFA data for the building profile. For now with dummy data"""
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

    return mfa_data
