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

    name_default = world_data.get("Name", "")

    st.subheader("World Name")
    name_input = st.text_input("What is the name of the world? Put something in as a placeholder,\
 we'll come back to this.", value=name_default)

    if st.button("Save"):
        save_world_section(file_name, "Name", name_input)
        st.success(f"Saved Name for {file_name}")

    st.subheader("World Manuscript (Live)")
    st.markdown(render_world_markdown(world_data))
    

