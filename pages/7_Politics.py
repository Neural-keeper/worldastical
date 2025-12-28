import streamlit as st
from core.storage import load_world, save_world_section
from core.preview import render_world_markdown
import uuid

st.title("Politics")
st.subheader("(Countries & their relations)")

# Require a loaded world
if "current_world" not in st.session_state or not st.session_state.current_world:
    st.warning("Please create or load a world from the main menu first.")
else:
    file_name = st.session_state.current_world
    world_data = load_world(file_name)

    # Correctly get nested keys
    relations_default = world_data.get("Politics", [])

    # Initialize session_state list
    if "relations_list" not in st.session_state:
        st.session_state.relations_list = [
            {"id": str(uuid.uuid4()), "value": v}
            for v in relations_default
        ]

    def delete_relation(relation_id):
        st.session_state.relations_list = [
            r for r in st.session_state.relations_list if r["id"] != relation_id
        ]

    def add_relation():
        st.session_state.relations_list.append(
            {"id": str(uuid.uuid4()), "value": ""}
        )

    st.subheader("Politics")
    st.write("""
    Politics is inescapable, both in reality and fantasy. Again, this is a major plot \
    progressor. Politics defines the world, its people, and their differences. Think about \
    the main country your story will take place in. What are the political issues at play? \
    What is the power system? If multiple countries are involved, what are the striking \
    differences? Which countries' leaders strive for power and wish to conquer? Which \
    leaders are trying to progress science and economy, which are trying to progress \
    the arts? In short, what is the political state of your world? Is it embroiled in world \
    wars, is it a peaceful time with slight economic tensions? Try to make a mindmap \
    elsewhere connecting each country and its leaders.
    """)

    st.write("Here, though, just write a few sentences for each country in the \
    form of country - allies - enemies - leaders - goals")
    
    # Editable, deletable list of places
    for relation in st.session_state.relations_list:
        col1, col2 = st.columns([3,1])

        with col1:
            relation["value"] = st.text_input(
                "Country - relation(s)",
                value=relation["value"],
                key=f"relation_input_{relation['id']}",
                placeholder="Elysium - forests - humans - The Fae - take control of the human forests"
            )

        with col2:
            st.button(
                "Delete",
                key=f"delete_relation_{relation['id']}",
                on_click=delete_relation,
                args=(relation["id"],)
            )

    st.button("Add new relation", on_click=add_relation)

    # Save
    if st.button("Save"):
        relations_input = [
                r["value"] for r in st.session_state.relations_list if r["value"].strip()
            ],
        
        save_world_section(file_name, "Politics", relations_input)
        st.success(f"Saved Politics for {file_name}")
        # reload world_data for preview
        world_data = load_world(file_name)

    st.subheader("World Manuscript (Live)")
    st.markdown(render_world_markdown(world_data))