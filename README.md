# InsightFlow

InsightFlow is an AI-powered creator intelligence platform for analyzing captions before publication. It combines NLP, heuristic scoring, and a production-oriented FastAPI backend to help creators improve visibility, engagement, and conversion.

## Overview

The platform currently supports:
- Caption sentiment analysis
- Virality and engagement prediction
- Readability and hook analysis
- CTA detection and rewrite suggestions
- Authenticated analysis history
- A versioned API foundation suitable for SaaS expansion

## Architecture

```text
Client -> FastAPI API -> Service Layer -> Repository Layer -> SQLite/Postgres
                           |                |
                           v                v
                     AI Services       SQLAlchemy Models
```

## Folder Structure

```text
backend/
  app/
    ai/               # AI analysis and rewrite logic
    api/              # API routers and dependencies
    core/             # Config, logging, exceptions
    db/               # Database session and initialization
    repositories/     # Persistence abstractions
    services/         # Business logic layer
    models.py         # SQLAlchemy models
  main.py            # FastAPI application entrypoint
  tests/             # API and integration tests
```

## Features

### AI Insights
- Content quality scoring
- Virality prediction
- Hook and readability analysis
- Emotional analysis
- Hashtag recommendations

### Platform APIs
- Health endpoint
- Auth registration and login
- Caption analysis endpoint
- Analysis history endpoint

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Testing

```bash
cd backend && pytest -q
```

## Deployment

Docker and Docker Compose are included for containerized deployment:

```bash
docker compose up --build
```

## Roadmap

- PostgreSQL production database
- Google OAuth integration
- Project and workspace APIs
- Dashboard analytics and export pipelines
- Advanced transformer-based ranking models
