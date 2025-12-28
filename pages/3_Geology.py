import streamlit as st
from core.storage import load_world, save_world_section
from core.preview import render_world_markdown
import uuid

st.title("Geology (and Geography)")

# Require a loaded world
if "current_world" not in st.session_state or not st.session_state.current_world:
    st.warning("Please create or load a world from the main menu first.")
else:
    file_name = st.session_state.current_world
    world_data = load_world(file_name)

    # Correctly get nested keys
    scale_default_value = world_data.get("Geology", {}).get("Scale", "")
    scale_options = ["Small", "Medium", "Large"]
    scale_default = scale_options.index(scale_default_value) if scale_default_value in scale_options else 0
    places_default = world_data.get("Geology", {}).get("Places", [])

    # Initialize session_state list
    if "places_list" not in st.session_state:
        st.session_state.places_list = [
            {"id": str(uuid.uuid4()), "value": p}
            for p in places_default
        ]

    def delete_place(place_id):
        st.session_state.places_list = [
            p for p in st.session_state.places_list if p["id"] != place_id
        ]

    def add_place():
        st.session_state.places_list.append(
            {"id": str(uuid.uuid4()), "value": ""}
        )

    st.write("""
    The best way to do this part is to visualize. \
I'm not sure if you're a traditional paper person or a web person so I'll tell you how \
to do both. On paper, pour some rice and draw along the greater outlines. Online, \
go to [Fantasy Map Generator](https://azgaar.github.io/Fantasy-Map-Generator/). Don't pay \
too much attention to the map yet, we're just here for a random outline. 
    """)

    st.write("""
    Now, think about the main features you want the part of the world your \
story takes place to have. If this story spans over the entire world, what diverse \
features do you want to include? Snowy mountains and parched deserts? What \
else? 
    """)

    st.subheader("Scale")
    scale_input = st.selectbox(
        "Decide the scope of your world (small, medium, large):",
        scale_options,
        index=scale_default
    )

    st.subheader("Places")
    st.write("Great! Now, think about some really cool scenes you want in your story. \
Where do they take place? At the edge of a dangerously tall cliff? On the docks \
of a harbor? Out in the open sea, up in the sky, what are some cool stages and \
locations? It's tempting to want to think about every aspect of the world, but \
we're not gods.")

    # Editable, deletable list of places
    for place in st.session_state.places_list:
        col1, col2 = st.columns([3,1])

        with col1:
            place["value"] = st.text_input(
                "Place",
                value=place["value"],
                key=f"place_input_{place['id']}",
                placeholder="Cliffs of Moher"
            )

        with col2:
            st.button(
                "Delete",
                key=f"delete_{place['id']}",
                on_click=delete_place,
                args=(place["id"],)
            )


    st.button("Add new place", on_click=add_place)

    # Save All
    if st.button("Save All"):
        geology_input = {
            "Scale": scale_input,
            "Places": [
                p["value"] for p in st.session_state.places_list if p["value"].strip()
            ]
        }
        save_world_section(file_name, "Geology", geology_input)
        st.success(f"Saved Geology for {file_name}")
        # reload world_data for preview
        world_data = load_world(file_name)

    st.subheader("World Manuscript (Live)")
    st.markdown(render_world_markdown(world_data))
