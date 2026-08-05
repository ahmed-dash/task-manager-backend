# Task Manager — Backend

FastAPI + PostgreSQL + SQLAlchemy 2.0 + Alembic + JWT auth.

This is the backend half of a portfolio project. Pairs with the
[task-manager-frontend](../task-manager-frontend) repo. Full production
deployment (AWS EC2, Docker, Jenkins CI/CD) is documented separately as the
project progresses.

## Stack

- **FastAPI** — async Python web framework, auto-generated OpenAPI docs
- **PostgreSQL** — relational database
- **SQLAlchemy 2.0** — ORM
- **Alembic** — database migrations
- **JWT** (python-jose) — stateless auth, passwords hashed with bcrypt
- **pytest** — tests run against an isolated in-memory SQLite DB, no Docker needed

## Project layout

```
app/
  core/        settings, security (JWT + password hashing)
  db/          engine/session setup, declarative base
  models/      SQLAlchemy ORM models
  schemas/     Pydantic request/response models
  crud/        DB access functions
  api/routes/  FastAPI routers (auth, users, tasks)
  main.py      app factory, middleware, router wiring
alembic/       migration environment + versioned migrations
tests/         pytest suite
```

## Option A — Run locally with Docker (recommended)

```bash
cp .env.example .env
# edit .env and set a real SECRET_KEY

docker compose up --build
```

This starts Postgres and the API together. Once it's up, run the migration
inside the running container:

```bash
docker compose exec backend alembic upgrade head
```

API docs: http://localhost:8000/api/v1/docs
Health check: http://localhost:8000/health

## Option B — Run locally without Docker

Requires Python 3.12 and a local/ remote PostgreSQL instance.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements-dev.txt

cp .env.example .env
# edit .env: point DATABASE_URL at your local Postgres

alembic upgrade head
uvicorn app.main:app --reload
```

## Running tests

```bash
pytest -v
```

Tests use an isolated in-memory SQLite database via dependency override —
they don't touch Postgres and don't need Docker running.

## Creating a new migration after changing a model

```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

## API overview

| Method | Path                    | Auth | Description              |
|--------|--------------------------|------|---------------------------|
| POST   | /api/v1/auth/register    | No   | Create a new account      |
| POST   | /api/v1/auth/login       | No   | Get a JWT access token    |
| GET    | /api/v1/users/me         | Yes  | Current user's profile    |
| GET    | /api/v1/tasks            | Yes  | List your tasks           |
| POST   | /api/v1/tasks            | Yes  | Create a task              |
| GET    | /api/v1/tasks/{id}       | Yes  | Get one task               |
| PUT    | /api/v1/tasks/{id}       | Yes  | Update a task              |
| DELETE | /api/v1/tasks/{id}       | Yes  | Delete a task              |

Full interactive docs (Swagger UI) are always available at `/api/v1/docs`
once the server is running.
