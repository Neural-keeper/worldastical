import streamlit as st
from ui.content import CONTENT

SECTIONS = [
    "Name","Inspiration","Geology","Political Geography","Symbolism",
    "Religion","Politics","History","Zoology and Botany","Quirk"
]

# --------------------------
# Safe rerun helper
# --------------------------
def rerun():
    st.session_state._rerun = True
    st.stop()

# --------------------------
# Section navigation buttons
# --------------------------
def section_navigation():
    idx = SECTIONS.index(st.session_state.current_section)
    col1, col2 = st.columns(2)

    # Initialize button click flags
    if "next_clicked" not in st.session_state:
        st.session_state.next_clicked = False
    if "prev_clicked" not in st.session_state:
        st.session_state.prev_clicked = False

    with col1:
        if idx > 0 and st.button("⬅ Previous") and not st.session_state.prev_clicked:
            st.session_state.prev_clicked = True
            st.session_state.next_clicked = False
            st.session_state.current_section = SECTIONS[idx - 1]
            rerun()
    with col2:
        if idx < len(SECTIONS) - 1 and st.button("Next ➡") and not st.session_state.next_clicked:
            st.session_state.next_clicked = True
            st.session_state.prev_clicked = False
            st.session_state.current_section = SECTIONS[idx + 1]
            rerun()

# --------------------------
# Save section helper
# --------------------------
def save_section(name):
    if name not in st.session_state.saved_sections:
        st.session_state.saved_sections.append(name)
        st.success(f"{name} saved!")

# --------------------------
# Section renderers
# --------------------------
def render_name(world):
    st.markdown("### Name")
    st.write(CONTENT["Name"])
    world["Name"] = st.text_input("World Name", value=world.get("Name",""))
    if st.button("Save Name"):
        save_section("Name")
    section_navigation()

def render_inspiration(world):
    st.markdown("### Inspiration")
    st.write(CONTENT["Inspiration"])
    known = st.radio("Do you know the real-world inspiration?", ["Yes", "No"])
    if known == "Yes":
        world["Inspiration"] = st.text_input("Enter your inspiration", value=world.get("Inspiration",""))
    else:
        period = st.radio("Choose time period", ["Past", "Present", "Future"])
        world["Inspiration"] = f"{period} world inspiration"
    if st.button("Save Inspiration"):
        save_section("Inspiration")
    section_navigation()

def render_geology(world):
    st.markdown("### Geology")
    st.write(CONTENT["Geology"])
    world["Geology"] = world.get("Geology", {"Scale":"", "Places":[]})
    world["Geology"]["Scale"] = st.radio("World Scale", ["Small", "Large"], index=0)
    places = st.text_area("List your locations, one per line", "\n".join(world["Geology"].get("Places",[])))
    world["Geology"]["Places"] = [p.strip() for p in places.split("\n") if p.strip()]
    if st.button("Save Geology"):
        save_section("Geology")
    section_navigation()

def render_political_geography(world):
    st.markdown("### Political Geography")
    st.write(CONTENT["Political Geography"])
    world["Political Geography"] = world.get("Political Geography", {"Countries":[],"Borders":[]})
    countries = st.text_area("List countries (country: features)", "\n".join(world["Political Geography"].get("Countries",[])))
    borders = st.text_area("List borders (country1 - country2 : feature)", "\n".join(world["Political Geography"].get("Borders",[])))
    world["Political Geography"]["Countries"] = [c.strip() for c in countries.split("\n") if c.strip()]
    world["Political Geography"]["Borders"] = [b.strip() for b in borders.split("\n") if b.strip()]
    if st.button("Save Political Geography"):
        save_section("Political Geography")
    section_navigation()

def render_symbolism(world):
    st.markdown("### Symbolism")
    st.write(CONTENT["Symbolism"])
    symbols = st.text_area("Country : symbols", "\n".join(world.get("Symbolism",[])))
    world["Symbolism"] = [s.strip() for s in symbols.split("\n") if s.strip()]
    if st.button("Save Symbolism"):
        save_section("Symbolism")
    section_navigation()

def render_religion(world):
    st.markdown("### Religion")
    st.write(CONTENT["Religion"])
    world["Religion"] = st.text_area("Describe Religion", value=world.get("Religion",""))
    if st.button("Save Religion"):
        save_section("Religion")
    section_navigation()

def render_politics(world):
    st.markdown("### Politics")
    st.write(CONTENT["Politics"])
    politics = st.text_area("Political details", "\n".join(world.get("Politics",[])))
    world["Politics"] = [p.strip() for p in politics.split("\n") if p.strip()]
    if st.button("Save Politics"):
        save_section("Politics")
    section_navigation()

def render_history(world):
    st.markdown("### History")
    st.write(CONTENT["History"])
    history = st.text_area("List historical events", "\n".join(world.get("History",[])))
    world["History"] = [h.strip() for h in history.split("\n") if h.strip()]
    if st.button("Save History"):
        save_section("History")
    section_navigation()

def render_zoology(world):
    st.markdown("### Zoology and Botany")
    st.write(CONTENT["Zoology and Botany"])
    world["Zoology and Botany"] = st.text_area("Describe creatures and plants", value=world.get("Zoology and Botany",""))
    if st.button("Save Zoology and Botany"):
        save_section("Zoology and Botany")
    section_navigation()

def render_quirk(world):
    st.markdown("### Quirk")
    st.write(CONTENT["Quirk"])
    world["Quirk"] = st.text_input("World Quirk", value=world.get("Quirk",""))
    if st.button("Save Quirk"):
        save_section("Quirk")
    section_navigation()

# --------------------------
# Mapping for app.py
# --------------------------
RENDER_MAP = {
    "Name": render_name,
    "Inspiration": render_inspiration,
    "Geology": render_geology,
    "Political Geography": render_political_geography,
    "Symbolism": render_symbolism,
    "Religion": render_religion,
    "Politics": render_politics,
    "History": render_history,
    "Zoology and Botany": render_zoology,
    "Quirk": render_quirk
}
