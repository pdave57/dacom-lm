# Dacom-LM

**Learn Independently. Practise Continuously. Build Real Solutions.**

Dacom-LM is a self-paced software engineering learning and competency assessment platform combining structured learning pathways, AI-powered lesson explanations, isolated coding playgrounds (Frontend, Python, PostgreSQL), practical coding assessments (**Trials**), real-world Gitea-backed software projects (**Raids**), remote Code Mentorship, verifiable certification, and a Back Office administration portal.

## Backend Structure

The backend is built with **Python + FastAPI** using a modular monolithic architecture supported by independent **Celery** background workers:

- `backend/app/main.py` — FastAPI application entry point (`/api/v1`)
- `backend/app/core/` — Configuration, JWT/OAuth2 security, RBAC dependencies, exceptions
- `backend/app/database/` — SQLAlchemy base models, mixins, and database session management
- `backend/app/shared/` — Shared pagination, response schemas, and domain enums
- `backend/app/modules/` — 21 domain modules (auth, users, roles, programmes, learning_paths, courses, lessons, progress, ai_tutor, playground, trials, python_execution, sql_execution, raids, gitea, inspection, evaluation, mentorship, certification, analytics, administration)
- `backend/app/workers/` — Independent Celery workers for AI, Python, SQL, Frontend, Raid inspection, evaluation, and notifications
- `backend/alembic/` — Database migrations
- `backend/tests/` — Automated pytest suite

## Quick Start

```bash
# Copy environment variables
cp .env.example .env

# Start services with Docker Compose
docker compose up --build
```

Or run the FastAPI server locally:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API documentation is available at `http://localhost:8000/docs`.
# dacom-lm
