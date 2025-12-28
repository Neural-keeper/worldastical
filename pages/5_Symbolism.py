import streamlit as st
from core.storage import load_world, save_world_section
from core.preview import render_world_markdown
import uuid

st.title("Symbolism")
st.subheader("(Countries & their symbols)")

# Require a loaded world
if "current_world" not in st.session_state or not st.session_state.current_world:
    st.warning("Please create or load a world from the main menu first.")
else:
    file_name = st.session_state.current_world
    world_data = load_world(file_name)

    # Correctly get nested keys
    symbols_default = world_data.get("Symbolism", [])

    # Initialize session_state list
    if "symbols_list" not in st.session_state:
        st.session_state.symbols_list = [
            {"id": str(uuid.uuid4()), "value": v}
            for v in symbols_default
        ]

    def delete_symbol(symbol_id):
        st.session_state.symbols_list = [
            s for s in st.session_state.symbols_list if s["id"] != symbol_id
        ]

    def add_symbol():
        st.session_state.symbols_list.append(
            {"id": str(uuid.uuid4()), "value": ""}
        )

    st.subheader("Symbols")
    st.write("""
    Use your inspiration to see how this works in real life. What are \
    important things to each country? Think about the USA with its bald eagles and \
    flag elements. Enter these potential elements in the form of Country : element 1, \
    element 2, etc.
    """)

    # Editable, deletable list of places
    for symbol in st.session_state.symbols_list:
        col1, col2 = st.columns([3,1])

        with col1:
            symbol["value"] = st.text_input(
                "Country - Symbol",
                value=symbol["value"],
                key=f"symbol_input_{symbol['id']}",
                placeholder="Elysium : Plants, Sapphires"
            )

        with col2:
            st.button(
                "Delete",
                key=f"delete_symbol_{symbol['id']}",
                on_click=delete_symbol,
                args=(symbol["id"],)
            )

    st.button("Add new symbol", on_click=add_symbol)

    # Save
    if st.button("Save"):
        symbols_input = [
                s["value"] for s in st.session_state.symbols_list if s["value"].strip()
            ],
        
        save_world_section(file_name, "Symbolism", symbols_input)
        st.success(f"Saved Symbolism for {file_name}")
        # reload world_data for preview
        world_data = load_world(file_name)

    st.subheader("World Manuscript (Live)")
    st.markdown(render_world_markdown(world_data))