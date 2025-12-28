import streamlit as st
from core.storage import load_world, save_world_section
from core.preview import render_world_markdown
import uuid

st.title("History")
st.subheader("(Countries & their histories)")

# Require a loaded world
if "current_world" not in st.session_state or not st.session_state.current_world:
    st.warning("Please create or load a world from the main menu first.")
else:
    file_name = st.session_state.current_world
    world_data = load_world(file_name)

    # Correctly get nested keys
    histories_default = world_data.get("History", [])

    # Initialize session_state list
    if "histories_list" not in st.session_state:
        st.session_state.histories_list = [
            {"id": str(uuid.uuid4()), "value": v}
            for v in histories_default
        ]

    def delete_history(history_id):
        st.session_state.histories_list = [
            h for h in st.session_state.histories_list if h["id"] != history_id
        ]

    def add_history():
        st.session_state.histories_list.append(
            {"id": str(uuid.uuid4()), "value": ""}
        )

    st.subheader("History")
    st.write("""
    What are some events that define the world? Maybe creation myths, maybe \
    a war hundreds of years ago that still leaves its impression on the people.
    """)
    
    # Editable, deletable list of places
    for history in st.session_state.histories_list:
        col1, col2 = st.columns([3,1])

        with col1:
            history["value"] = st.text_input(
                "Country - history(s)",
                value=history["value"],
                key=f"history_input_{history['id']}",
                placeholder="Elysium : Worship the plants"
            )

        with col2:
            st.button(
                "Delete",
                key=f"delete_history_{history['id']}",
                on_click=delete_history,
                args=(history["id"],)
            )

    st.button("Add new history", on_click=add_history)

    # Save
    if st.button("Save"):
        histories_input = [
                h["value"] for h in st.session_state.histories_list if h["value"].strip()
            ],
        
        save_world_section(file_name, "History", histories_input)
        st.success(f"Saved History for {file_name}")
        # reload world_data for preview
        world_data = load_world(file_name)

    st.subheader("World Manuscript (Live)")
    st.markdown(render_world_markdown(world_data))