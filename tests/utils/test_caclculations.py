import pytest

from utils import calculations


@pytest.fixture()
def sample_data():
    return {
        "woning_typologie_m2": {
            "appartement": 80,
            "rijtjeshuis": 120,
            "vrijstaand": 160,
        }
    }


def test_create_building_profile_impact_table():
    pass
