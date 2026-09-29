# Worldastical Web Deployable

This directory contains a deployable version of the Worldastical worldbuilding app. It is structured as a browser-based Flask service with a hosted Postgres database option for production, while still supporting a local SQLite fallback for development.

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
CREATE TABLE IF NOT EXISTS worlds (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    inspiration TEXT,
    geology TEXT,
    religion TEXT,
    politics TEXT,
    history TEXT,
    quirk TEXT,
    sections TEXT
);
```

3. Copy your Supabase connection string from Project Settings > Database > Connection string.
4. In Render, create a new Web Service and connect this repository.
5. Set the following environment variables:

```bash
DATABASE_URL=postgresql://postgres:<password>@<host>:5432/postgres
SECRET_KEY=your-random-secret
FLASK_DEBUG=false
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
- This approach keeps local testing simple while making deployment easy.

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
- authentication if multiple users will access it
- proper logging and monitoring
- backups for the database
- environment variables set in Render instead of hardcoded values

## Purpose

This folder is intentionally separated from the original prototype so the main project can remain a local creative tool, while the deployable version shows how to convert it into a hosted web application.
