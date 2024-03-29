""" Classes to hold building profile data.
Also holds building needs data and woning typologie data, but this may need to be moved to a different class."""

import math


class BuildingData:
    """Class to hold all building profile data. Includes a needs dictionary but may want to put this in a different class."""

    def __init__(self):
        self.needs = {}
        self.building_profiles = {}
        self.woning_typologie_m2 = {}
        self.building_uses = []
        self.editable_data = {
            "needs": self.needs,
            "building_profiles": self.building_profiles,
            "woning_typologie_m2": self.woning_typologie_m2,
        }

    def load_all_data(self):
        """Generic function to load all the data from the bag, needs and building profiles."""
        self.load_needs_data()
        self.load_building_profile_data()

    def load_needs_data(self):
        """Load the needs data. This data should be put somewhere else, but for now it's here.
        Creates a list of building uses to use e.g. to set a column config"""
        self.needs["dwelling_needs"] = {"Woningen": 600}
        self.needs["other_needs"] = {
            "Kantoren": 10000,
            "Horeca": 5000,
            "Utiliteits": 3000,
        }
        self.editable_data["needs"] = self.needs
        self.building_uses = list(self.needs["other_needs"].keys()) + list(
            self.needs["dwelling_needs"].keys()
        )

    def load_building_profile_data(self):
        """Load building data. This data should be put somewhere else, but for now it's here."""
        self.woning_typologie_m2 = {"Groot": 120, "Klein": 60, "Medium": 80}
        self.building_profiles = {
            "Mixed_used_toren": {
                "split": {"Woningen": 0.6, "Kantoren": 0.3, "Horeca": 0.1},
                "impact_m2": {"hybrid": 300, "secondary": 100, "regular": 500},
                "min_m2": 500,
                "description": "Een toren met een mix van woningen, kantoren en horeca.",
            },
            "Kantoorgebouw": {
                "split": {"Kantoren": 1},
                "impact_m2": {"hybrid": 100, "secondary": 200, "regular": 500},
                "min_m2": 1000,
                "description": "Een gebouw met alleen kantoren.",
            },
            "Laagbouw": {
                "split": {"Woningen": 1},
                "impact_m2": {"hybrid": 100, "secondary": 200, "regular": 500},
                "min_m2": 120,
                "description": "Een laagbouw met alleen woningen.",
            },
            "Multi-family": {
                "split": {"Woningen": 1},
                "impact_m2": {"hybrid": 60, "secondary": 30, "regular": 100},
                "min_m2": 480,
                "description": "Een gebouw met alleen woningen voor meerdere gezinnen",
            },
        }
        self.editable_data["woning_typologie_m2"] = self.woning_typologie_m2
        self.editable_data["building_profiles"] = self.building_profiles

    def get_profile_template(self):
        """Returns a template for a building profile"""
        split = list(self.needs["dwelling_needs"].keys()) + list(
            self.needs["other_needs"].keys()
        )
        return {
            "split": {s: 0 for s in split},
            "impact_m2": {"hybrid": 0, "secondary": 0, "regular": 0},
            "min_m2": 0,
            "description": "Beschrijf hier het gebouwprofiel.",
        }

    def update_profile_split(self, profile_name: str, new_split: dict):
        """Updates the split of the building use (e.g. office, woningen, etc.
        in the building profile. The split should be a dictionary with the building uses as keys and the percentage
        of the building that should be used for that purpose as values.
        """
        sum_new_values = sum(new_split.values())
        if profile_name in self.building_profiles:
            if math.isclose(sum_new_values, 1, abs_tol=0.0001):
                self.building_profiles[profile_name]["split"] = new_split
                return True
            print("Sum of new values is not 1")
            return False
        print("Profile not found")
        return False

    def update_profile_impact(self, profile_name: str, new_impact: dict):
        """Updates the impact of the building profile. This is the impact of the building profile per m2."""
        if profile_name in self.building_profiles:
            self.building_profiles[profile_name]["impact_m2"] = new_impact
            return True
        return False

    def update_profile_min_m2(self, profile_name: str, new_m2: int):
        """Updates the minimum m2 of the building profile. This is the minimum amount of m2 that the building should have."""
        if profile_name in self.building_profiles:
            self.building_profiles[profile_name]["min_m2"] = new_m2
            return True
        return False

    def add_building_profile(self, profile_name: str, profile_data: dict) -> bool:
        """Adds a new building profil
        Args:
            profile_name: The name of the new profile
            profile_data: A dictionary containing 'split', 'impact_m2', and 'min_m2'
        """
        if profile_name not in self.building_profiles:
            if self.validate_building_profile(profile_data):  # Ensure data is valid
                self.building_profiles[profile_name] = profile_data
                self.editable_data["building_profiles"] = self.building_profiles
                print("Profile added successfully")
                print(self.building_profiles)
                return True
            print("Profile not valid")
            return False  # Indicate failure due to invalid data
        print("Profile name conflict")
        return False  # Indicate failure due to profile name conflict

    def update_profile_description(self, profile_name, new_description: str):
        """Updates the description of the building profile. This is a string that describes the building profile."""
        if profile_name in self.building_profiles:
            self.building_profiles[profile_name]["description"] = new_description
            return True
        return False

    def validate_building_profile(self, profile_data: dict):
        """ToDo: Validates the building profile data"""
        if profile_data:
            return True
        return False
