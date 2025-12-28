import os
import json

WORLD_FOLDER = "worlds"

if not os.path.exists(WORLD_FOLDER):
    os.makedirs(WORLD_FOLDER)

def list_worlds():
    """Return list of JSON world files"""
    return [f for f in os.listdir(WORLD_FOLDER) if f.endswith(".json")]

def load_world(file_name):
    """Load a world JSON, return empty dict if not found"""
    path = os.path.join(WORLD_FOLDER, file_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_world_section(file_name, section_key, section_data):
    """Update a section in a world JSON"""
    path = os.path.join(WORLD_FOLDER, file_name)
    world = load_world(file_name)
    world[section_key] = section_data
    with open(path, "w", encoding="utf-8") as f:
        json.dump(world, f, indent=4, ensure_ascii=False)

def delete_world(file_name):
    """Delete a world JSON file"""
    path = os.path.join(WORLD_FOLDER, file_name)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False

