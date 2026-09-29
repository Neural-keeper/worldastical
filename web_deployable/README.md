# Worldastical Web Deployable

This directory contains the authenticated, deployable web version of the Worldastical worldbuilding app. It is structured as a browser-based Flask service with a hosted Postgres database option for production, while still supporting a local SQLite fallback for development.

## Recommended deployment stack

The most practical free-tier setup is:

- Render for the web app host
- Supabase Postgres for the database
- Environment variables for configuration
- Gunicorn as the production server

This gives you a working production architecture without needing to manage your own VPS.

## Tech stack

- Flask — backend web application
- Jinja templates — page rendering
- PostgreSQL via Supabase — production database
- Redis — optional cache for frequently loaded worlds
- SQLite — local development fallback
- Gunicorn — production server for Render
- Python-dotenv — environment variable loading

## Local development

```powershell
cd web_deployable
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Deployment options

### Option 1: Recommended — Render + Supabase

This is the easiest path to a fully deployable app.

1. Create a new Supabase project.
2. In the SQL editor, run:

```sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS worlds (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    inspiration TEXT,
    geology TEXT,
    religion TEXT,
    politics TEXT,
    history TEXT,
    quirk TEXT,
    sections TEXT,
    UNIQUE (user_id, name)
);
```

The app hashes passwords and stores only the hash. World queries are always scoped by the signed-in user's `user_id`, so accounts cannot view or modify one another's worlds.

3. In Supabase, click **Connect**, choose **Session pooler**, select the **URI** format, and copy that connection string. The Session Pooler avoids direct IPv6 connection failures from Render.
4. In Render, create a new Web Service and connect this repository.
5. Set the following environment variables:

```bash
DATABASE_URL=postgresql://postgres.<project-id>:<password>@aws-0-<region>.pooler.supabase.com:5432/postgres
REDIS_URL=rediss://default:<password>@<redis-host>:<port>
CACHE_TTL_SECONDS=300
SECRET_KEY=your-random-secret
FLASK_DEBUG=false
SESSION_COOKIE_SECURE=true
```

6. Use the start command:

```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2
```

7. Deploy the service. Render will expose a live URL for the app.

### Option 2: Vercel frontend + Render backend

If you want a separate frontend deployment, Vercel can host a static front-end or a lightweight Next.js/React shell, while Render hosts the Flask backend API. In that case:

- Render keeps the Python app and database access
- Vercel handles the browser-facing UI shell
- Supabase remains the shared database layer

This is a cleaner frontend split, but it is more work than a single Render service.

### Option 3: Streamlit Cloud

This project can also be adapted to Streamlit Cloud if you prefer a no-frontend-code approach. The tradeoff is that Streamlit Cloud is less flexible for a multi-service production architecture and usually requires a simpler deployment model.

## Render project files included

This directory includes the deployment-ready files needed for Render:

- `requirements.txt`
- `app.py`
- `render.yaml`
- `Procfile`
- `.env.example`
- `runtime.txt`

## Database notes

- Local development uses SQLite automatically when no `DATABASE_URL` is present.
- Production uses Supabase Postgres automatically when `DATABASE_URL` is set.
- Redis caching is enabled when `REDIS_URL` is set; otherwise the app uses the database directly.
- Cached world lists and details are scoped by user and expire after `CACHE_TTL_SECONDS` (default: 300).
- World creation, edits, renames, and deletion invalidate the affected cache entries.
- Authentication is required for the web app, and each world belongs to one user account.
- This approach keeps local testing simple while making deployment easy.

### Redis setup

Create a Redis instance with a managed provider such as Upstash, then add its
connection string as the `REDIS_URL` environment variable in Render. Use `rediss://`
when the provider requires TLS. Redis is an optimization rather than a required
service: if it is unavailable, cache operations are ignored and database reads
continue normally.

### Render startup migration failure

If Render reports `psycopg2.errors.InFailedSqlTransaction` during `init_db()`, the
database migration attempted to add a column that already existed. PostgreSQL then
marked that transaction as failed, so later setup queries were rejected as well.
The migration now uses PostgreSQL's idempotent `ADD COLUMN IF NOT EXISTS` syntax and
keeps separate SQLite handling, so restarting the service safely supports both new
and previously initialized databases. PostgreSQL legacy rows are also read by
column name because production connections use `RealDictCursor`.

## Environment setup example

Copy `.env.example` to `.env` and edit it locally:

```powershell
Copy-Item .env.example .env
```

Example:

```bash
DATABASE_URL=postgresql://postgres:yourpassword@db.xxxxxx.supabase.co:5432/postgres
SECRET_KEY=super-secret-key
FLASK_DEBUG=false
```

## Production checklist

Before launching publicly, make sure you also have:

- a secure `SECRET_KEY`
- a real production database instead of local SQLite
- HTTPS enabled on the production host
- proper logging and monitoring
- backups for the database
- environment variables set in Render instead of hardcoded values

## Purpose

This folder is intentionally separated from the original prototype so the main project can remain a local creative tool, while the deployable version shows how to convert it into a hosted web application.
