import streamlit as st
from core.storage import list_worlds, load_world

def init_state():
    if "world" not in st.session_state:
        # Load last saved world if exists
        saved_worlds = list_worlds()
        if saved_worlds:
            last_world = saved_worlds[-1]
            st.session_state.world = load_world(last_world)
            st.session_state.current_section = "Name"
            st.session_state.saved_sections = list(st.session_state.world.keys())
        else:
            # Initialize empty world
            st.session_state.world = {
                "Name": "",
                "Inspiration": "",
                "Geology": {"Scale":"", "Places":[]},
                "Political Geography": {"Countries":[],"Borders":[]},
                "Symbolism": [],
                "Religion": "",
                "Politics": [],
                "History": [],
                "Zoology and Botany": "",
                "Quirk": ""
            }
            st.session_state.current_section = "Name"
            st.session_state.saved_sections = []
