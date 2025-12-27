def world_to_markdown(world):
    """Convert the world dictionary into Markdown format for preview/export."""
    lines = []
    for key, value in world.items():
        lines.append(f"## {key}")
        if isinstance(value, dict):
            for k, v in value.items():
                if isinstance(v, list):
                    lines.append(f"### {k}")
                    for item in v:
                        lines.append(f"- {item}")
                else:
                    lines.append(f"- {k}: {v}")
        elif isinstance(value, list):
            for item in value:
                lines.append(f"- {item}")
        else:
            lines.append(str(value))
        lines.append("")  # Empty line between sections
    return "\n".join(lines)
