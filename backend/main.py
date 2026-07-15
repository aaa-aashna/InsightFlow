from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.v1.router import router as v1_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.init_db import init_db
from app.models import User  # noqa: F401

configure_logging()
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "InsightFlow backend works"}


@app.on_event("startup")
def startup_event() -> None:
    init_db()