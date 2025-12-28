import streamlit as st
from core.storage import list_worlds

st.set_page_config(page_title="Worldastical", layout="wide")
st.title("Worldastical: Main Menu")

# Initialize session state for current world
if "current_world" not in st.session_state:
    st.session_state.current_world = None

st.subheader("📜🪶 Create or Load a World")

world_files = list_worlds()
selected_world = st.selectbox("📜 Load existing world:", [""] + world_files)

if selected_world:
    st.session_state.current_world = selected_world
    st.success(f"Loaded {selected_world}")

new_world_name = st.text_input("Or create a new world (without .json)")
if st.button("🪶 Create World"):
    if not new_world_name.strip():
        st.error("World name cannot be empty")
    else:
        file_name = new_world_name.strip() + ".json"
        if file_name in world_files:
            st.error("World already exists")
        else:
            from core.default_world import DEFAULT_WORLD
            from core.storage import save_world_section
            save_world_section(file_name, "Name", new_world_name)
            st.session_state.current_world = file_name
            st.success(f"World {file_name} created")

st.subheader("✒️ Navigate to a Section")
st.write("Click a page in the left sidebar to edit its section. All pages will auto-fill if a world is loaded.")

st.write("Your current world:", st.session_state.current_world)

