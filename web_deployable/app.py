from __future__ import annotations

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

        if database_url:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS worlds (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    inspiration TEXT,
                    geology TEXT,
                    religion TEXT,
                    politics TEXT,
                    history TEXT,
                    quirk TEXT
                )
                """
            )
        else:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS worlds (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    inspiration TEXT,
                    geology TEXT,
                    religion TEXT,
                    politics TEXT,
                    history TEXT,
                    quirk TEXT
                )
                """
            )


init_db()


def load_worlds() -> list[dict]:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, name, inspiration, geology, religion, politics, history, quirk FROM worlds ORDER BY id"
        )
        rows = cur.fetchall()
        return [dict(row) for row in rows]


def create_world_record(payload: dict) -> None:
    database_url = os.getenv("DATABASE_URL")
    with get_db_connection() as conn:
        cur = conn.cursor()
        if database_url:
            cur.execute(
                """
                INSERT INTO worlds (name, inspiration, geology, religion, politics, history, quirk)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    payload["name"],
                    payload["inspiration"],
                    payload["geology"],
                    payload["religion"],
                    payload["politics"],
                    payload["history"],
                    payload["quirk"],
                ),
            )
        else:
            cur.execute(
                """
                INSERT INTO worlds (name, inspiration, geology, religion, politics, history, quirk)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload["name"],
                    payload["inspiration"],
                    payload["geology"],
                    payload["religion"],
                    payload["politics"],
                    payload["history"],
                    payload["quirk"],
                ),
            )


def delete_world_record(world_name: str) -> None:
    database_url = os.getenv("DATABASE_URL")
    with get_db_connection() as conn:
        cur = conn.cursor()
        if database_url:
            cur.execute("DELETE FROM worlds WHERE LOWER(name) = LOWER(%s)", (world_name,))
        else:
            cur.execute("DELETE FROM worlds WHERE LOWER(name) = LOWER(?)", (world_name,))


@app.get("/")
def index():
    worlds = load_worlds()
    return render_template("index.html", worlds=worlds)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}, 200


@app.get("/api/worlds")
def api_worlds():
    return {"worlds": load_worlds()}


@app.post("/worlds")
def create_world():
    name = (request.form.get("name") or "").strip()
    if not name:
        return redirect(url_for("index"))

    worlds = load_worlds()
    if any(existing.get("name", "").strip().lower() == name.lower() for existing in worlds):
        return redirect(url_for("index"))

    payload = {
        "name": name,
        "inspiration": (request.form.get("inspiration") or "").strip(),
        "geology": (request.form.get("geology") or "").strip(),
        "religion": (request.form.get("religion") or "").strip(),
        "politics": (request.form.get("politics") or "").strip(),
        "history": (request.form.get("history") or "").strip(),
        "quirk": (request.form.get("quirk") or "").strip(),
    }
    create_world_record(payload)
    return redirect(url_for("index"))


@app.post("/worlds/<name>/delete")
def delete_world(name: str):
    delete_world_record(name)
    return redirect(url_for("index"))


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
