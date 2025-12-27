import streamlit as st
from ui.sections import SECTIONS, RENDER_MAP
from core.storage import list_worlds, load_world, save_world
from core import export

# --------------------------
# Safe rerun helper
# --------------------------
def rerun():
    """Replacement for deprecated st.experimental_rerun"""
    st.session_state._rerun = True
    st.stop()

# --------------------------
# Default world structure
# --------------------------
DEFAULT_WORLD = {
    "Name": "",
    "Inspiration": "",
    "Geology": {"Scale":"", "Places":[]},
    "Political Geography": {"Countries":[],"Borders":[]},
    "Symbolism": [],
    "Religion": "",
    "Politics": [],
    "History": [],
    "Zoology and Botany": "",
    "Quirk": ""
}

# --------------------------
# Initialize session state
# --------------------------
if "world" not in st.session_state:
    st.session_state.world = DEFAULT_WORLD.copy()
if "saved_sections" not in st.session_state:
    st.session_state.saved_sections = []
if "current_section" not in st.session_state:
    st.session_state.current_section = "Name"
if "load_flag" not in st.session_state:
    st.session_state.load_flag = False
if "button_clicks" not in st.session_state:
    st.session_state.button_clicks = {}

# --------------------------
# Sidebar
# --------------------------
st.sidebar.title("Worldastical")

# Section navigation in sidebar
section_choice = st.sidebar.radio(
    "Navigate Sections",
    SECTIONS,
    index=SECTIONS.index(st.session_state.current_section)
)
if section_choice != st.session_state.current_section:
    st.session_state.current_section = section_choice
    # Reset per-section button flags
    st.session_state.button_clicks = {}

# Progress bar
progress = len(st.session_state.saved_sections)/len(SECTIONS)
st.sidebar.progress(progress)

# Load saved worlds (only if Name not set yet)
if not st.session_state.world["Name"]:
    saved_worlds = list_worlds()
    if saved_worlds:
        selected = st.sidebar.selectbox("Load saved world", ["--"] + saved_worlds)
        if selected != "--" and not st.session_state.load_flag:
            loaded = load_world(selected)
            # Merge loaded world into default
            for key, default_value in DEFAULT_WORLD.items():
                if key in loaded:
                    if isinstance(default_value, dict) and isinstance(loaded[key], dict):
                        merged = default_value.copy()
                        merged.update(loaded[key])
                        st.session_state.world[key] = merged
                    else:
                        st.session_state.world[key] = loaded[key]
                else:
                    st.session_state.world[key] = default_value
            st.session_state.saved_sections = [
                k for k, v in st.session_state.world.items() if v and v != DEFAULT_WORLD[k]
            ]
            st.session_state.current_section = "Name"
            st.session_state.load_flag = True
            rerun()

# --------------------------
# Render current section
# --------------------------
current = st.session_state.current_section
RENDER_MAP[current](st.session_state.world)

# --------------------------
# Markdown preview with parchment
# --------------------------
st.markdown("---")
st.subheader("Live World Preview")
md_content = export.world_to_markdown(st.session_state.world)
st.markdown(
    f"""
    <div style="
        background: linear-gradient(rgba(248,241,228,0.9), rgba(248,241,228,0.9)), url('assets/parchment.jpg');
        background-size: cover;
        background-repeat: repeat;
        color:#3e2c15;
        font-family: 'Georgia', serif;
        padding:20px;
        border-radius:10px;
        box-shadow: 0 0 15px rgba(0,0,0,0.3);
        max-height:500px;
        overflow-y:auto;
        line-height:1.6;
        ">
        {md_content.replace('\n','<br>')}
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------
# Export / Save
# --------------------------
st.sidebar.subheader("Export / Save")
file_name = st.sidebar.text_input("World File Name", value=st.session_state.world.get("Name","world"))
if st.sidebar.button("Save World"):
    save_world(file_name, st.session_state.world)
    st.sidebar.success(f"World saved as {file_name}.json")
