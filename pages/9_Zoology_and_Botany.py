import streamlit as st
from core.storage import load_world, save_world_section
from core.preview import render_world_markdown
import uuid

st.title("Zoology and Botany")
st.subheader("(Flora & Fauna)")

# Require a loaded world
if "current_world" not in st.session_state or not st.session_state.current_world:
    st.warning("Please create or load a world from the main menu first.")
else:
    file_name = st.session_state.current_world
    world_data = load_world(file_name)

    # Correctly get nested keys
    flora_default = world_data.get("Zoology and Bonary", {}).get("Flora", [])
    fauna_default = world_data.get("Zoology and Bonary", {}).get("Fauna", [])

    # Initialize session_state list
    if "flora_list" not in st.session_state:
        st.session_state.flora_list = [
            {"id": str(uuid.uuid4()), "value": v}
            for v in flora_default
        ]

    def delete_flora(flora_id):
        st.session_state.flora_list = [
            c for c in st.session_state.flora_list if c["id"] != flora_id
        ]
        st.rerun()

    def add_flora():
        st.session_state.flora_list.append(
            {"id": str(uuid.uuid4()), "value": ""}
        )

    if "fauna_list" not in st.session_state:
        st.session_state.fauna_list = [
            {"id": str(uuid.uuid4()), "value": v}
            for v in fauna_default
        ]

    def delete_fauna(fauna_id):
        st.session_state.fauna_list = [
            b for b in st.session_state.fauna_list if b["id"] != fauna_id
        ]
        st.rerun()

    def add_fauna():
        st.session_state.fauna_list.append(
            {"id": str(uuid.uuid4()), "value": ""}
        )

    st.subheader("Flora")
    st.write("""
    What kinds of plants populate your world? Are they special in some way (magical, fire-flowers, etc)? Or perhaps \
    they can only be found in certain places (up in the mountains, inside a glacier)? Note a couple down here!
    """)
    # Editable, deletable list of places
    for flora in st.session_state.flora_list:
        col1, col2 = st.columns([3,1])

        with col1:
            flora["value"] = st.text_input(
                "Flora",
                value=flora["value"],
                key=f"flora_input_{flora['id']}",
                placeholder="Elysia - a mystical cure all found in the cracks of a geode"
            )

        with col2:
            st.button(
                "Delete",
                key=f"delete_flora_{flora['id']}",
                on_click=delete_flora,
                args=(flora["id"],)
            )

    st.button("Add new flora", on_click=add_flora)

    st.subheader("Fauna")
    st.write("""
    What are some creatures that prowl the world? This includes all species and races, \
    intelligent or not. Assign them some cool traits (vampires - can't go out in the sun) \
    or relations (werewolves - can't stant vampires because of the events of Twilight)!
    """)
    # Editable, deletable list of places
    for fauna in st.session_state.fauna_list:
        col1, col2 = st.columns([3,1])

        with col1:
            fauna["value"] = st.text_input(
                "Fauna",
                value=fauna["value"],
                key=f"fauna_input_{fauna['id']}",
                placeholder="Archangels - five of them were exiled to the ground centuries ago"
            )

        with col2:
            st.button(
                "Delete",
                key=f"delete_fauna_{fauna['id']}",
                on_click=delete_fauna,
                args=(fauna["id"],)
            )

    st.button("Add new fauna", on_click=add_fauna)

    # Save All
    if st.button("Save All"):
        znb_input = {
            "Flora": [
                c["value"] for c in st.session_state.flora_list if c["value"].strip()
            ],
            "Fauna": [
                b["value"] for b in st.session_state.fauna_list if b["value"].strip()
            ]
        }
        save_world_section(file_name, "Zoology and Bonary", znb_input)
        st.success(f"Saved Zoology and Bonary for {file_name}")
        # reload world_data for preview
        world_data = load_world(file_name)

    st.subheader("World Manuscript (Live)")
    st.markdown(render_world_markdown(world_data))
