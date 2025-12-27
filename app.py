import streamlit as st
from core.theme import inject_theme
from core.state import list_worlds, set_current_world, delete_world, get_current_world

inject_theme()
st.title("Worldastical")

# --- World Selection ---
st.sidebar.markdown("## Load or Create World")

existing = list_worlds()
choice = st.sidebar.selectbox("Select a world:", ["<new>"] + existing)

if choice == "<new>":
    new_name = st.sidebar.text_input("New world name:")
    if new_name:
        world = set_current_world(new_name)
        st.sidebar.success(f"New world '{new_name}' created.")
else:
    world = set_current_world(choice)
    st.sidebar.success(f"Loaded world '{choice}'")

# Delete world button
if choice != "<new>" and st.sidebar.button("Delete this world"):
    delete_world(choice)
    st.sidebar.warning(f"Deleted world '{choice}'")
    st.experimental_rerun()  # reload the app so selection updates

# Progress calculation
sections = [
    "name", "inspiration", "geology", "political_geography",
    "symbolism", "religion", "politics", "history",
    "zoology_and_botany", "quirk"
]

progress = sum(1 for s in sections if s in get_current_world()) / len(sections)
st.sidebar.markdown("### Progress")
st.sidebar.progress(progress)

st.markdown("Welcome! Use the navigation on the left to build your world.")

world = get_current_world()

st.download_button("Download JSON", json.dumps(world, indent=2), "world.json")
st.download_button("Download Markdown", "\n".join([
    f"# {world.get('name', 'Unnamed World')}",
    f"## Inspiration\n{world.get('inspiration','')}",
    f"## Geology\nScale: {world.get('geology',{}).get('scale','')}\n" +
    "\n".join(f"- {l}" for l in world.get('geology',{}).get('locations',[]))
]), "world.md")