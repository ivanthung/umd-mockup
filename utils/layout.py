import streamlit as st

def set_page_title(title: str):
    st.set_page_config(page_title=title, layout="wide")
    col1, col2 = st.columns((1, 3))
    
    with col1:
        st.image("resources/Amsterdam City.png", width=200)
    
    with col2:
        st.title(title)
    st.divider()