import streamlit as st
from core.theme import inject_theme
from core.state import get_current_world

inject_theme()
world = get_current_world()

sections = [
    "name", "inspiration", "geology", "political_geography",
    "symbolism", "religion", "politics", "history",
    "znb", "quirk"
]

progress = sum(1 for s in sections if s in world) / len(sections)
st.sidebar.markdown("### Progress")
st.sidebar.progress(progress)
