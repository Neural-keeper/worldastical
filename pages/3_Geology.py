import streamlit as st
from core.theme import inject_theme
from core.state import get_current_world, update_section

inject_theme()
world = get_current_world()

st.image("assets/icons/geology.png", width=40)
st.header("Geology")

scale = st.selectbox(
    "World Scale",
    ["Small", "Medium", "Large"],
    index=["Small", "Medium", "Large"].index(world.get("geology", {}).get("scale", "Medium"))
)

locations = st.text_area(
    "Important locations (one per line)",
    value="\n".join(world.get("geology", {}).get("locations", []))
)

if st.button("Save Geology"):
    update_section("geology", {"scale": scale, "locations": locations.splitlines()})
    st.success("Geology saved.")

st.markdown('<img src="assets/divider.png" style="width:100%; margin:1em 0;">', unsafe_allow_html=True)

# Live Markdown preview
st.markdown("### Live World Preview")
md = f"""
## Geology
- Scale: {scale}
- Locations:
"""
for loc in locations.splitlines():
    md += f"  - {loc}\n"

st.markdown(md)
