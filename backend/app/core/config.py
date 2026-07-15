from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "InsightFlow"
    app_version: str = "1.0.0"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"
    cors_origins: List[str] = ["http://localhost:3000"]
    database_url: str = "sqlite:///./insightflow.db"
    jwt_secret_key: str = "dev-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7
    rate_limit_per_minute: int = 60

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
    }


@lru_cache()
def get_settings() -> Settings:
    return Settings()
