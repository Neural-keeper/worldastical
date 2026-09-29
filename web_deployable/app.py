from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from psycopg2.extras import RealDictCursor

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
LOCAL_DB = DATA_DIR / "worlds.db"

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["JSON_SORT_KEYS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

SECTIONS = [
    "Name", "Inspiration", "Geology", "Political Geography", "Symbolism",
    "Religion", "Politics", "History", "Zoology and Botany", "Quirk",
]

CONTENT = {
    "Name": "What is the name of your world? Enter a placeholder if unsure - you can change it later.",
    "Inspiration": "Think about your story. What real-world inspirations influence your fantasy world? If you do not have a clear inspiration, choose a time period.",
    "Geology": "Visualize your world's main physical features. Decide on the scale and list interesting locations or landmarks.",
    "Political Geography": "Define the governing systems in your world. List countries and their defining features, then define borders or separations.",
    "Symbolism": "What symbols or cultural icons are important to each country or region? Enter them as Country: element1, element2, ...",
    "Religion": "Consider the belief systems of your people. What gods, values, or moral forces influence their lives?",
    "Politics": "Describe the political situation of your world. Include allies, enemies, leaders, goals, or conflicts.",
    "History": "List events that define your world, such as creation myths, wars, or major discoveries.",
    "Zoology and Botany": "Describe the creatures, plants, magical herbs, or spirits in your world.",
    "Quirk": "Every world has quirks that make it memorable. Think of unique cultural, environmental, or magical traits.",
}


def get_db_connection():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
        conn.autocommit = True
        return conn
    conn = sqlite3.connect(LOCAL_DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    database_url = os.getenv("DATABASE_URL")
    with get_db_connection() as conn:
        cur = conn.cursor()
        id_type = "SERIAL PRIMARY KEY" if database_url else "INTEGER PRIMARY KEY AUTOINCREMENT"
        name_type = "VARCHAR(255)" if database_url else "TEXT"
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS worlds (
                id {id_type}, name {name_type} NOT NULL UNIQUE,
                inspiration TEXT, geology TEXT, religion TEXT,
                politics TEXT, history TEXT, quirk TEXT, sections TEXT
            )
        """)
        try:
            cur.execute("ALTER TABLE worlds ADD COLUMN sections TEXT")
        except (sqlite3.OperationalError, psycopg2.errors.DuplicateColumn):
            pass


def blank_world(name: str = "") -> dict:
    return {
        "Name": name, "Inspiration": "",
        "Geology": {"Scale": "", "Places": []},
        "Political Geography": {"Countries": [], "Borders": []},
        "Symbolism": [], "Religion": "", "Politics": [], "History": [],
        "Zoology and Botany": "", "Quirk": "",
    }


def row_to_world(row: dict) -> dict:
    world = blank_world(row["name"])
    raw_sections = row.get("sections")
    if raw_sections:
        try:
            world.update(json.loads(raw_sections))
            return world
        except (TypeError, json.JSONDecodeError):
            pass
    world.update({
        "Inspiration": row.get("inspiration") or "",
        "Geology": row.get("geology") or "",
        "Religion": row.get("religion") or "",
        "Politics": row.get("politics") or "",
        "History": row.get("history") or "",
        "Quirk": row.get("quirk") or "",
    })
    return world


def load_worlds() -> list[dict]:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM worlds ORDER BY id")
        return [dict(row) for row in cur.fetchall()]


def load_world(name: str) -> dict | None:
    database_url = os.getenv("DATABASE_URL")
    marker = "%s" if database_url else "?"
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM worlds WHERE LOWER(name) = LOWER({marker})", (name,))
        row = cur.fetchone()
    return row_to_world(dict(row)) if row else None


def create_world_record(name: str) -> None:
    database_url = os.getenv("DATABASE_URL")
    marker = "%s" if database_url else "?"
    with get_db_connection() as conn:
        conn.cursor().execute(
            f"INSERT INTO worlds (name, sections) VALUES ({marker}, {marker})",
            (name, json.dumps(blank_world(name))),
        )


def save_world(name: str, world: dict) -> None:
    database_url = os.getenv("DATABASE_URL")
    marker = "%s" if database_url else "?"
    with get_db_connection() as conn:
        conn.cursor().execute(f"""
            UPDATE worlds SET name = {marker}, inspiration = {marker}, geology = {marker},
                religion = {marker}, politics = {marker}, history = {marker},
                quirk = {marker}, sections = {marker}
            WHERE LOWER(name) = LOWER({marker})
        """, (
            world["Name"], str(world.get("Inspiration", "")),
            json.dumps(world.get("Geology", {})), str(world.get("Religion", "")),
            json.dumps(world.get("Politics", [])), json.dumps(world.get("History", [])),
            str(world.get("Quirk", "")), json.dumps(world), name,
        ))


def delete_world_record(name: str) -> None:
    database_url = os.getenv("DATABASE_URL")
    marker = "%s" if database_url else "?"
    with get_db_connection() as conn:
        conn.cursor().execute(f"DELETE FROM worlds WHERE LOWER(name) = LOWER({marker})", (name,))


def lines(value: str) -> list[str]:
    return [item.strip() for item in value.splitlines() if item.strip()]


def section_value(world: dict, section: str, key: str = "") -> str:
    value = world.get(section, "")
    if key:
        value = value.get(key, []) if isinstance(value, dict) else []
    return "\n".join(value) if isinstance(value, list) else str(value)


def save_section_from_form(world: dict, section: str) -> dict:
    if section == "Name":
        world[section] = (request.form.get("value") or "").strip()
    elif section == "Inspiration":
        if request.form.get("known") == "Yes":
            world[section] = (request.form.get("value") or "").strip()
        else:
            world[section] = f"{request.form.get('period', 'Past')} world inspiration"
    elif section == "Geology":
        world[section] = {"Scale": request.form.get("scale", "Small"), "Places": lines(request.form.get("places", ""))}
    elif section == "Political Geography":
        world[section] = {
            "Countries": lines(request.form.get("countries", "")),
            "Borders": lines(request.form.get("borders", "")),
        }
    elif section in {"Symbolism", "Politics", "History"}:
        world[section] = lines(request.form.get("value", ""))
    else:
        world[section] = (request.form.get("value") or "").strip()
    return world


@app.get("/")
def index():
    return render_template("index.html", worlds=load_worlds())


@app.get("/healthz")
def healthz():
    return {"status": "ok"}, 200


@app.post("/worlds")
def create_world():
    name = (request.form.get("name") or "").strip()
    if not name or any(world["name"].lower() == name.lower() for world in load_worlds()):
        return redirect(url_for("index"))
    create_world_record(name)
    return redirect(url_for("edit_section", name=name, section="Name"))


@app.get("/worlds/<name>")
def open_world(name: str):
    return redirect(url_for("edit_section", name=name, section="Name"))


@app.route("/worlds/<name>/<section>", methods=["GET", "POST"])
def edit_section(name: str, section: str):
    if section not in SECTIONS:
        return redirect(url_for("index"))
    world = load_world(name)
    if world is None:
        return redirect(url_for("index"))
    if request.method == "POST":
        world = save_section_from_form(world, section)
        save_world(name, world)
        action = request.form.get("action", "save")
        index = SECTIONS.index(section)
        if action == "next" and index < len(SECTIONS) - 1:
            return redirect(url_for("edit_section", name=world["Name"], section=SECTIONS[index + 1]))
        if action == "previous" and index > 0:
            return redirect(url_for("edit_section", name=world["Name"], section=SECTIONS[index - 1]))
        name = world["Name"]
    progress = sum(bool(world.get(item)) for item in SECTIONS) / len(SECTIONS)
    return render_template(
        "section.html", world=world, name=name, section=section, sections=SECTIONS,
        content=CONTENT[section], section_index=SECTIONS.index(section), progress=progress,
        value=section_value(world, section), places=section_value(world, "Geology", "Places"),
        countries=section_value(world, "Political Geography", "Countries"),
        borders=section_value(world, "Political Geography", "Borders"),
    )


@app.post("/worlds/<name>/delete")
def delete_world(name: str):
    delete_world_record(name)
    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
