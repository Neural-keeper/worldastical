from __future__ import annotations

import json
import os
import re
import sqlite3
from functools import wraps
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from flask import Flask, has_request_context, redirect, render_template, request, session, url_for
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
LOCAL_DB = DATA_DIR / "worlds.db"

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["JSON_SORT_KEYS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"

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

WORLD_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _-]{0,79}$")
MAX_SECTION_LENGTH = 5000
MAX_LIST_ITEMS = 100
USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_]{3,30}$")


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
            CREATE TABLE IF NOT EXISTS users (
                id {id_type}, username {name_type} NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS worlds (
                id {id_type}, user_id INTEGER NOT NULL REFERENCES users(id), name {name_type} NOT NULL,
                inspiration TEXT, geology TEXT, religion TEXT,
                politics TEXT, history TEXT, quirk TEXT, sections TEXT,
                UNIQUE (user_id, name)
            )
        """)
        if database_url:
            cur.execute("ALTER TABLE worlds ADD COLUMN IF NOT EXISTS sections TEXT")
            cur.execute("ALTER TABLE worlds ADD COLUMN IF NOT EXISTS user_id INTEGER")
        else:
            try:
                cur.execute("ALTER TABLE worlds ADD COLUMN sections TEXT")
            except sqlite3.OperationalError:
                pass
            try:
                cur.execute("ALTER TABLE worlds ADD COLUMN user_id INTEGER")
            except sqlite3.OperationalError:
                pass
        marker = "%s" if database_url else "?"
        cur.execute("SELECT COUNT(*) FROM worlds WHERE user_id IS NULL")
        legacy_world_count = cur.fetchone()
        legacy_world_count = (
            legacy_world_count["count"] if database_url else legacy_world_count[0]
        )
        if legacy_world_count:
            cur.execute(f"SELECT id FROM users WHERE username = {marker}", ("legacy_owner",))
            legacy_user = cur.fetchone()
            if not legacy_user:
                cur.execute(
                    f"INSERT INTO users (username, password_hash) VALUES ({marker}, {marker})",
                    ("legacy_owner", generate_password_hash(os.urandom(32).hex())),
                )
                cur.execute(f"SELECT id FROM users WHERE username = {marker}", ("legacy_owner",))
                legacy_user = cur.fetchone()
            legacy_user_id = legacy_user["id"] if database_url else legacy_user[0]
            cur.execute(
                f"UPDATE worlds SET user_id = {marker} WHERE user_id IS NULL",
                (legacy_user_id,),
            )


def current_user_id() -> int | None:
    return session.get("user_id") if has_request_context() else None


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if current_user_id() is None:
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def user_by_username(username: str):
    database_url = os.getenv("DATABASE_URL")
    marker = "%s" if database_url else "?"
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM users WHERE LOWER(username) = LOWER({marker})", (username,))
        row = cur.fetchone()
    return dict(row) if row else None


def create_user(username: str, password: str) -> None:
    database_url = os.getenv("DATABASE_URL")
    marker = "%s" if database_url else "?"
    with get_db_connection() as conn:
        conn.cursor().execute(
            f"INSERT INTO users (username, password_hash) VALUES ({marker}, {marker})",
            (username, generate_password_hash(password)),
        )


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


def load_worlds(user_id: int | None = None) -> list[dict]:
    user_id = user_id if user_id is not None else current_user_id()
    database_url = os.getenv("DATABASE_URL")
    marker = "%s" if database_url else "?"
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM worlds WHERE user_id = {marker} ORDER BY id", (user_id,))
        return [dict(row) for row in cur.fetchall()]


def load_world(name: str, user_id: int | None = None) -> dict | None:
    user_id = user_id if user_id is not None else current_user_id()
    database_url = os.getenv("DATABASE_URL")
    marker = "%s" if database_url else "?"
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            f"SELECT * FROM worlds WHERE user_id = {marker} AND LOWER(name) = LOWER({marker})",
            (user_id, name),
        )
        row = cur.fetchone()
    return row_to_world(dict(row)) if row else None


def create_world_record(name: str, user_id: int | None = None) -> None:
    user_id = user_id if user_id is not None else current_user_id()
    database_url = os.getenv("DATABASE_URL")
    marker = "%s" if database_url else "?"
    with get_db_connection() as conn:
        conn.cursor().execute(
            f"INSERT INTO worlds (user_id, name, sections) VALUES ({marker}, {marker}, {marker})",
            (user_id, name, json.dumps(blank_world(name))),
        )


def save_world(name: str, world: dict, user_id: int | None = None) -> None:
    user_id = user_id if user_id is not None else current_user_id()
    database_url = os.getenv("DATABASE_URL")
    marker = "%s" if database_url else "?"
    with get_db_connection() as conn:
        conn.cursor().execute(f"""
            UPDATE worlds SET name = {marker}, inspiration = {marker}, geology = {marker},
                religion = {marker}, politics = {marker}, history = {marker},
                quirk = {marker}, sections = {marker}
            WHERE user_id = {marker} AND LOWER(name) = LOWER({marker})
        """, (
            world["Name"], str(world.get("Inspiration", "")),
            json.dumps(world.get("Geology", {})), str(world.get("Religion", "")),
            json.dumps(world.get("Politics", [])), json.dumps(world.get("History", [])),
            str(world.get("Quirk", "")), json.dumps(world), user_id, name,
        ))


def delete_world_record(name: str, user_id: int | None = None) -> None:
    user_id = user_id if user_id is not None else current_user_id()
    database_url = os.getenv("DATABASE_URL")
    marker = "%s" if database_url else "?"
    with get_db_connection() as conn:
        conn.cursor().execute(
            f"DELETE FROM worlds WHERE user_id = {marker} AND LOWER(name) = LOWER({marker})",
            (user_id, name),
        )


def lines(value: str) -> list[str]:
    return [item.strip() for item in value.splitlines() if item.strip()]


def validate_world_name(name: str) -> str | None:
    if not name:
        return "World name is required."
    if len(name) > 80:
        return "World name must be 80 characters or fewer."
    if not WORLD_NAME_PATTERN.fullmatch(name):
        return "World name may use letters, numbers, spaces, hyphens, and underscores only."
    return None


def validate_credentials(username: str, password: str) -> str | None:
    if not USERNAME_PATTERN.fullmatch(username):
        return "Username must be 3-30 characters using letters, numbers, or underscores."
    if len(password) < 8:
        return "Password must be at least 8 characters."
    return None


def validate_section_form(section: str) -> str | None:
    if section == "Name":
        return validate_world_name((request.form.get("value") or "").strip())
    if section == "Inspiration":
        known = request.form.get("known")
        if known not in {"Yes", "No"}:
            return "Choose Yes or No for the inspiration question."
        if known == "Yes" and not (request.form.get("value") or "").strip():
            return "Enter an inspiration or choose No."
        if known == "No" and request.form.get("period") not in {"Past", "Present", "Future"}:
            return "Choose Past, Present, or Future."
    elif section == "Geology":
        if request.form.get("scale") not in {"Small", "Large"}:
            return "Choose Small or Large for the world scale."
        if len(lines(request.form.get("places", ""))) > MAX_LIST_ITEMS:
            return f"Enter no more than {MAX_LIST_ITEMS} places."
    elif section == "Political Geography":
        if len(lines(request.form.get("countries", ""))) > MAX_LIST_ITEMS:
            return f"Enter no more than {MAX_LIST_ITEMS} countries."
        if len(lines(request.form.get("borders", ""))) > MAX_LIST_ITEMS:
            return f"Enter no more than {MAX_LIST_ITEMS} borders."
    elif section in {"Symbolism", "Politics", "History"}:
        if len(lines(request.form.get("value", ""))) > MAX_LIST_ITEMS:
            return f"Enter no more than {MAX_LIST_ITEMS} lines."
    if len(request.form.get("value", "")) > MAX_SECTION_LENGTH:
        return f"This section must be {MAX_SECTION_LENGTH} characters or fewer."
    return None


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


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        error = validate_credentials(username, password)
        if not error and user_by_username(username):
            error = "That username is already in use."
        if not error:
            create_user(username, password)
            user = user_by_username(username)
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("index"))
    return render_template("auth.html", mode="Register", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        user = user_by_username(username)
        if not user or not check_password_hash(user["password_hash"], request.form.get("password") or ""):
            error = "Invalid username or password."
        else:
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(request.args.get("next") or url_for("index"))
    return render_template("auth.html", mode="Log in", error=error)


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.get("/")
@login_required
def index():
    return render_template("index.html", worlds=load_worlds(), error=None)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}, 200


@app.post("/worlds")
@login_required
def create_world():
    name = (request.form.get("name") or "").strip()
    error = validate_world_name(name)
    if error:
        return render_template("index.html", worlds=load_worlds(), error=error), 400
    if any(world["name"].lower() == name.lower() for world in load_worlds()):
        return render_template(
            "index.html", worlds=load_worlds(), error="A world with that name already exists."
        ), 409
    create_world_record(name)
    return redirect(url_for("edit_section", name=name, section="Name"))


@app.get("/worlds/<name>")
@login_required
def open_world(name: str):
    return redirect(url_for("edit_section", name=name, section="Name"))


@app.route("/worlds/<name>/<section>", methods=["GET", "POST"])
@login_required
def edit_section(name: str, section: str):
    if section not in SECTIONS:
        return redirect(url_for("index"))
    world = load_world(name)
    if world is None:
        return redirect(url_for("index"))
    error = None
    if request.method == "POST":
        error = validate_section_form(section)
        if error:
            return render_template(
                "section.html", world=world, name=name, section=section, sections=SECTIONS,
                content=CONTENT[section], section_index=SECTIONS.index(section),
                progress=sum(bool(world.get(item)) for item in SECTIONS) / len(SECTIONS),
                value=section_value(world, section), places=section_value(world, "Geology", "Places"),
                countries=section_value(world, "Political Geography", "Countries"),
                borders=section_value(world, "Political Geography", "Borders"), error=error,
            ), 400
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
        error=error,
    )


@app.post("/worlds/<name>/delete")
@login_required
def delete_world(name: str):
    delete_world_record(name)
    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
