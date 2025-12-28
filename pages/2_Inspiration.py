import streamlit as st
from core.storage import load_world, save_world_section
from core.preview import render_world_markdown
from core.theme import inject_theme

# inject_theme()
st.title("Inspiration")

# Require a loaded world
if "current_world" not in st.session_state or not st.session_state.current_world:
    st.warning("Please create or load a world from the main menu first.")
else:
    file_name = st.session_state.current_world
    world_data = load_world(file_name)

    inspo_default = world_data.get("Inspiration", "")

    st.subheader("Real World Inspiration")
    st.write("Think about your story. Now think about the vibes of the world \
you're trying to create.")
    inspo_exist = st.selectbox("Do you know what your real-world inspiration for your \
fantasy is?", ("Yes", "No"),)
    
    if inspo_exist == "Yes":
        inspo_input = st.text_input("Write down your inspiration below: ", value=inspo_default, placeholder="Eg: Medieval Europe")
    else:
        time_period = st.selectbox(
            "Start with time period: what time period is it closest to?",
            ("Past", "Present", "Future"),
        )
        if time_period == "Past":
            inspo_input = st.text_input(
                "Think about historical fiction. Is this similar to Regency \
Era England, Ancient China, or America admist the World War? Try to find a \
time period and place that matches the vibe of your story. What is the best match? ",
                value=inspo_default,
                placeholder="Eg: Ancient India",
            )
        elif time_period == "Present":
            inspo_input = st.text_input(
                "What present country has a similar vibe and tone for your \
story? Is it a democracy or is it like North Korea, trapping its inhabitants? This is a \
great time to research countries if you're not sure. ",
                value=inspo_default,
                placeholder="Eg: Greenland",
            )
        else:
            inspo_input = st.text_input(
                "A world of the future is hard to relate to the modern, real-life, \
world. That doesn't mean its impossible, though. What country do you expect, \
several years in the future, to look the most like your world? Or, if you're feeling \
even more adventerous, what planets are included in your world (enter as a comma \
separated list)? ",
                value=inspo_default,
                placeholder="Eg: Mars, Earth, Alpha Centauri",
            )

    if st.button("Save"):
        save_world_section(file_name, "Inspiration", inspo_input)
        st.success(f"Saved Inspiration for {file_name}")

    st.subheader("World Manuscript (Live)")
    st.markdown(render_world_markdown(world_data))
    
