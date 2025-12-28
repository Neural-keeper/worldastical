import streamlit as st
from core.storage import load_world, save_world_section
from core.preview import render_world_markdown
from core.theme import inject_theme

st.title("Name")

# Require a loaded world
if "current_world" not in st.session_state or not st.session_state.current_world:
    st.warning("Please create or load a world from the main menu first.")
else:
    file_name = st.session_state.current_world
    world_data = load_world(file_name)

    quirk_default = world_data.get("Quirk", "")

    st.subheader("World's Quirk")
    quirk_input = st.text_input("Each world has some quirks that make it memorable. \
The Koroks in Zelda, the 'dam' joke in Percy Jackson and the Olympians. What's \
yours? ", value=quirk_default)

    if st.button("Save"):
        save_world_section(file_name, "Quirk", quirk_input)
        st.success(f"Saved Quirk for {file_name}")

    st.subheader("World Manuscript (Live)")
    st.markdown(render_world_markdown(world_data))