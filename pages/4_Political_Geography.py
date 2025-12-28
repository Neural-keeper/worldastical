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
    countries_default = world_data.get("Political Geography", {}).get("Countries", [])
    borders_default = world_data.get("Political Geography", {}).get("Borders", [])

    # Initialize session_state list
    if "countries_list" not in st.session_state:
        st.session_state.countries_list = [
            {"id": str(uuid.uuid4()), "value": v}
            for v in countries_default
        ]

    def delete_country(country_id):
        st.session_state.countries_list = [
            c for c in st.session_state.countries_list if c["id"] != country_id
        ]
        st.rerun()

    def add_country():
        st.session_state.countries_list.append(
            {"id": str(uuid.uuid4()), "value": ""}
        )

    if "borders_list" not in st.session_state:
        st.session_state.borders_list = [
            {"id": str(uuid.uuid4()), "value": v}
            for v in borders_default
        ]

    def delete_border(border_id):
        st.session_state.borders_list = [
            b for b in st.session_state.borders_list if b["id"] != border_id
        ]
        st.rerun()

    def add_border():
        st.session_state.borders_list.append(
            {"id": str(uuid.uuid4()), "value": ""}
        )

    st.subheader("Countries")
    st.write("""
    There are no doubt governing systems in your world. For the \
    sake of convenience, we'll refer to them as 'countries' in this app. How many \
    countries are in your world? What are their defining features? Enter in the form of \
    country : features. \n
    Use a known language (or perhaps you've created your own) to generate country \
    names based on the inspiration you picked earlier.
    """)
    # Editable, deletable list of places
    for country in st.session_state.countries_list:
        col1, col2 = st.columns([3,1])

        with col1:
            country["value"] = st.text_input(
                "Country",
                value=country["value"],
                key=f"country_input_{country['id']}",
                placeholder="Elysium : Sharp Cliffs"
            )

        with col2:
            st.button(
                "Delete",
                key=f"delete_country_{country['id']}",
                on_click=delete_country,
                args=(country["id"],)
            )

    st.button("Add new country", on_click=add_country)

    st.subheader("Borders")
    st.write("""
    How are these countries separated? By mountain ranges, rivers, \
    walls of fire, millions of miles of empty space, or just politically drawn imaginary \
    lines? Keeping these ideas in mind, enter the relations in the form of \
    country 1 - country 2 : border feature(s).
    """)
    # Editable, deletable list of places
    for border in st.session_state.borders_list:
        col1, col2 = st.columns([3,1])

        with col1:
            border["value"] = st.text_input(
                "Border",
                value=border["value"],
                key=f"border_input_{border['id']}",
                placeholder="Elysium - Manlore : Vast Ocean + Shadow Wall"
            )

        with col2:
            st.button(
                "Delete",
                key=f"delete_border_{border['id']}",
                on_click=delete_border,
                args=(border["id"],)
            )

    st.button("Add new border", on_click=add_border)

    # Save All
    if st.button("Save All"):
        polgeo_input = {
            "Countries": [
                c["value"] for c in st.session_state.countries_list if c["value"].strip()
            ],
            "Borders": [
                b["value"] for b in st.session_state.borders_list if b["value"].strip()
            ]
        }
        save_world_section(file_name, "Political Geography", polgeo_input)
        st.success(f"Saved Political Geography for {file_name}")
        # reload world_data for preview
        world_data = load_world(file_name)

    st.subheader("World Manuscript (Live)")
    st.markdown(render_world_markdown(world_data))
