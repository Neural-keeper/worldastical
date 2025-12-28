import streamlit as st
from core.storage import load_world, save_world_section
from core.preview import render_world_markdown
import uuid

st.title("Political Geography")
st.subheader("(Countries & Borders)")

# Require a loaded world
if "current_world" not in st.session_state or not st.session_state.current_world:
    st.warning("Please create or load a world from the main menu first.")
else:
    file_name = st.session_state.current_world
    world_data = load_world(file_name)

    # Correctly get nested keys
    religions_default = world_data.get("Religion", [])

    # Initialize session_state list
    if "religions_list" not in st.session_state:
        st.session_state.religions_list = [
            {"id": str(uuid.uuid4()), "value": v}
            for v in religions_default
        ]

    def delete_religion(religion_id):
        st.session_state.religions_list = [
            r for r in st.session_state.religions_list if r["id"] != religion_id
        ]

    def add_religion():
        st.session_state.religions_list.append(
            {"id": str(uuid.uuid4()), "value": ""}
        )

    st.subheader("religions")
    st.write("""
    Use your inspiration to see how this works in real life. What are \
    important things to each country? Think about the USA with its bald eagles and \
    flag elements. Enter these potential elements in the form of Country : element 1, \
    element 2, etc.
    """)
    
    # Editable, deletable list of places
    for religion in st.session_state.countries_list:
        col1, col2 = st.columns([3,1])

        with col1:
            religion["value"] = st.text_input(
                "Country - religion(s)",
                value=religion["value"],
                key=f"religion_input_{religion['id']}",
                placeholder="Elysium : Worship the plants"
            )

        with col2:
            st.button(
                "Delete",
                key=f"delete_religion_{religion['id']}",
                on_click=delete_religion,
                args=(religion["id"],)
            )

    st.button("Add new religion", on_click=add_religion)

    # Save
    if st.button("Save"):
        religions_input = [
                r["value"] for r in st.session_state.religions_list if r["value"].strip()
            ],
        
        save_world_section(file_name, "Religion", religions_input)
        st.success(f"Saved Religion for {file_name}")
        # reload world_data for preview
        world_data = load_world(file_name)

    st.subheader("World Manuscript (Live)")
    st.markdown(render_world_markdown(world_data))