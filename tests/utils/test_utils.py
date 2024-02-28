import plotly

from utils.utils import display_dummy_sankey


def test_distplay_dummy_sankey():
    data = {
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

    fig = display_dummy_sankey(data)
    assert fig.data[0].type == "sankey"
