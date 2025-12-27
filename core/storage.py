import json
from pathlib import Path

DATA_DIR = Path("worlds")
DATA_DIR.mkdir(exist_ok=True)

def world_file(name: str):
    """Return Path object for a given world name"""
    return DATA_DIR / f"{name}.json"

def save_world(name: str, data: dict):
    """Save world data to JSON"""
    WORLD_FILE = world_file(name)
    WORLD_FILE.write_text(json.dumps(data, indent=2))

def load_world(name: str):
    """Load world data; return empty dict if file does not exist"""
    WORLD_FILE = world_file(name)
    if WORLD_FILE.exists():
        return json.loads(WORLD_FILE.read_text())
    return {}

def list_worlds():
    """Return a list of saved world names"""
    return [f.stem for f in DATA_DIR.glob("*.json")]

def delete_world(name: str):
    """Delete a saved world"""
    WORLD_FILE = world_file(name)
    if WORLD_FILE.exists():
        WORLD_FILE.unlink()
