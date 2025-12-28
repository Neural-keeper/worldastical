def render_world_markdown(world: dict) -> str:
    lines = []

    # --- Title ---
    if "name" in world:
        lines.append(f"# {world['name']}")
        lines.append("")

    # --- Inspiration ---
    if "inspiration" in world:
        lines.append("## Inspiration")
        lines.append(world["inspiration"])
        lines.append("")

    # --- Geology ---
    geo = world.get("geology")
    if geo:
        lines.append("## Geology")
        lines.append(f"**Scale:** {geo.get('scale','')}")
        if geo.get("locations"):
            lines.append("**Locations:**")
            for loc in geo["locations"]:
                lines.append(f"- {loc}")
        lines.append("")

    # --- Political Geography ---
    if "political_geography" in world:
        lines.append("## Political Geography")
        lines.append(world["political_geography"])
        lines.append("")

    # --- Symbolism ---
    if "symbolism" in world:
        lines.append("## Symbolism")
        lines.append(world["symbolism"])
        lines.append("")

    # --- Religion ---
    if "religion" in world:
        lines.append("## Religion")
        lines.append(world["religion"])
        lines.append("")

    # --- Politics ---
    if "politics" in world:
        lines.append("## Politics")
        lines.append(world["politics"])
        lines.append("")

    # --- History ---
    if "history" in world:
        lines.append("## History")
        lines.append(world["history"])
        lines.append("")

    # --- Zoology & Botany ---
    if "znb" in world:
        lines.append("## Zoology & Botany")
        lines.append(world["znb"])
        lines.append("")

    # --- Quirk ---
    if "quirk" in world:
        lines.append("## Quirk")
        lines.append(world["quirk"])
        lines.append("")

    return "\n".join(lines)

