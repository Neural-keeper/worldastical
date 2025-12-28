import streamlit as st
from core.storage import list_worlds, load_world, delete_world

st.title("Worldastical: Create or Load a World")

# List existing worlds
world_files = list_worlds()
st.subheader("Existing Worlds")
if world_files:
    selected_world = st.selectbox("Select a world to load or delete", world_files)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Load World"):
            world_data = load_world(selected_world)
            st.json(world_data)
    with col2:
        if st.button("Delete World"):
            if delete_world(selected_world):
                st.success(f"{selected_world} deleted successfully")
            else:
                st.error("Failed to delete")
else:
    st.info("No worlds found. Create a new one below.")

# Create a new world
st.subheader("Create New World")
new_world_name = st.text_input("Enter new world name (no spaces - only letters and '_'))")
if st.button("Create World"):
    if not new_world_name.strip():
        st.error("Name cannot be empty")
    else:
        file_name = new_world_name.strip() + ".json"
        if file_name in world_files:
            st.error("World with this name already exists")
        else:
            # Save empty world structure
            from core.default_world import DEFAULT_WORLD
            from core.storage import save_world_section
            save_world_section(file_name, "Name", new_world_name)
            st.success(f"World {file_name} created successfully")
