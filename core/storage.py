import json
import os

SAVE_DIR = "saved_worlds"

# Ensure the save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

def list_worlds():
    """Return a list of saved world filenames (without extension)."""
    return [f.replace(".json","") for f in os.listdir(SAVE_DIR) if f.endswith(".json")]

def save_world(name, world):
    """Save the world dict as a JSON file."""
    filepath = os.path.join(SAVE_DIR, f"{name}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(world, f, ensure_ascii=False, indent=4)

def load_world(name):
    """Load a world JSON file and return as dict."""
    filepath = os.path.join(SAVE_DIR, f"{name}.json")
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
