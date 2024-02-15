import streamlit as st
import utils.utils as utils

st.set_page_config(
    layout='wide',
    page_title="About",
    page_icon="👋",
)

session = st.session_state
if "gdf_bag" not in session:
    gdf_bag = utils.load_data()
    session.geometry_bag = gdf_bag
    session.gdf_bag = gdf_bag.drop(columns="geometry")

col1, col2 = st.columns((1, 4))

with col1:
    st.image("resources/Amsterdam City.png", width=200)

with col2:
    st.title("About the Urban Mining Dashboard")

st.divider()

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