from core.storage import load_world, save_world, list_worlds, delete_world

CURRENT_WORLD_KEY = "current"  # tracks current active world in memory

_world_cache = {}

def set_current_world(name: str):
    global _world_cache
    _world_cache[CURRENT_WORLD_KEY] = name
    data = load_world(name)
    _world_cache[name] = data
    return data

def get_current_world():
    global _world_cache
    name = _world_cache.get(CURRENT_WORLD_KEY)
    if not name:
        return {}
    return _world_cache.get(name, {})

def update_section(key: str, value):
    """Update current world section and save immediately"""
    global _world_cache
    name = _world_cache.get(CURRENT_WORLD_KEY)
    if not name:
        raise ValueError("No world loaded")
    world = _world_cache.get(name, {})
    world[key] = value
    save_world(name, world)
    _world_cache[name] = world
