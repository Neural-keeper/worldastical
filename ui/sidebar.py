import streamlit as st
from core.theme import inject_theme
from core.storage import load_world

inject_theme()


# --- Progress Calculation ---
sections = [
    "name", "inspiration", "geology", "political_geography",
    "symbolism", "religion", "politics", "history",
    "znb", "quirk"
]

file_name = st.session_state.current_world
world_data = load_world(file_name)
progress = sum(1 for s in sections if s in world_data) / len(sections)
st.sidebar.markdown("### Progress")
st.sidebar.progress(progress)










# # ------
# import streamlit as st
# from core.storage import list_worlds, load_world

# def rerun():
#     """Safe rerun replacement for deprecated st.experimental_rerun"""
#     st.session_state._rerun = True
#     st.stop()  # stops execution and triggers full rerun

# def render_sidebar():
#     st.sidebar.title("Worldastical")
#     saved_worlds = list_worlds()
#     if saved_worlds:
#         selected = st.sidebar.selectbox("Load saved world", ["-- New World --"] + saved_worlds)
#         if selected != "-- New World --":
#             st.session_state.world = load_world(selected)
#             st.session_state.current_section = "Name"
#             st.session_state.saved_sections = list(st.session_state.world.keys())
#             rerun()  # reload app with selected world


# SECTIONS = ["Name","Inspiration","Geology","Political Geography","Symbolism",
#             "Religion","Politics","History","Zoology and Botany","Quirk"]

# def render_sidebar():
#     st.sidebar.title("Worldastical")
#     section = st.sidebar.radio("Go to Section", SECTIONS, index=SECTIONS.index(st.session_state.current_section))
#     st.session_state.current_section = section
#     # Progress
#     progress = len(st.session_state.saved_sections)/len(SECTIONS)
#     st.sidebar.progress(progress)
