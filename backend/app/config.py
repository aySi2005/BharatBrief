"""Application configuration using pydantic-settings."""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Briefly API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Model
    MODEL_PATH: str = str(Path(__file__).resolve().parent.parent / "model" / "fine_tuned_t5_small")
    MODEL_PREFIX: str = "summarize:"
    MODEL_MAX_INPUT_LENGTH: int = 1024
    MODEL_MAX_OUTPUT_LENGTH: int = 128
    MODEL_DEFAULT_BEAMS: int = 4
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./briefly.db"
    
    # JWT Auth
    JWT_SECRET_KEY: str = "briefly-dev-secret-change-in-production-2024"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    
    # CORS
# CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://bharat-brief-psi.vercel.app",
    ]
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 30

    # External Fact Checking
    EXTERNAL_FACT_CHECK_ENABLED: bool = True
    EXTERNAL_FACT_CHECK_PROVIDER: str = "openalex"
    EXTERNAL_FACT_CHECK_TIMEOUT_SECONDS: float = 5.0
    
    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: list[str] = [".txt", ".pdf", ".docx"]
    
    # Redis (production)
    REDIS_URL: str = ""
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


@lru_cache()
def get_settings() -> Settings:
    return Settings()
