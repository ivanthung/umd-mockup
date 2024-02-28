""" Starting page for the Streamlit app"""

import streamlit as st
from streamlit_extras.app_logo import add_logo

from utils import data_manager, layout

session = st.session_state
layout.set_page_title("About")
data_manager.load_bag_data()

st.markdown(
    """
    Boilerplate dummy text:

* **Over Urban Mining:**
    * Urban mining is de kunst om steden te zien als bronnen voor waardevolle materialen. Door grondstoffen terug te winnen uit onze bestaande gebouwde omgeving, beperken we afval en sparen we natuurlijke hulpbronnen.
* **Metabolic's Missie:**
    * Metabolic versnelt de transitie naar een duurzame, circulaire economie. Met behulp van data en systeemkennis, stimuleren we innovatie voor een betere toekomst.
* **Doel van het Dashboard:**
    * Dit dashboard brengt cruciale inzichten voor stadsontwikkelaars, beleidsmakers, en bedrijven die willen bijdragen aan de circulaire economie van Amsterdam.

* **Verken de Data:** Ga dieper in op materiaalstromen, hergebruik kansen, en projecten op het gebied van urban mining.
* **Meer over Metabolic:** Ontdek onze expertise en projecten op het gebied van circulariteit en duurzaamheid.
* **Wordt Partner:** Neem contact met ons op voor samenwerkingsmogelijkheden op het gebied van urban mining.

   """
)
