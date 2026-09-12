"""Briefly API — FastAPI application entry point."""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db
from app.services.model_service import model_service
from app.api import health, summarize, auth, history

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup and shutdown."""
    settings = get_settings()
    
    # Startup
    logger.info("=" * 60)
    logger.info("  Briefly API — Starting up")
    logger.info("=" * 60)
    
    # Initialize database
    logger.info("Initializing database...")
    await init_db()
    logger.info("Database ready")
    
    # Load ML model
    logger.info("Loading T5 summarization model...")
    model_service.load_model()
    model_service.warmup()
    logger.info("Model loaded and warmed up")
    
    logger.info("=" * 60)
    logger.info(f"  Briefly API v{settings.APP_VERSION} — Ready")
    logger.info(f"  Docs: http://{settings.HOST}:{settings.PORT}/docs")
    logger.info("=" * 60)
    
    yield
    
    # Shutdown
    logger.info("Briefly API — Shutting down")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="AI-powered news article summarization API. Powered by a fine-tuned T5-small model.",
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(health.router, prefix="/api")
    app.include_router(summarize.router, prefix="/api")
    app.include_router(auth.router, prefix="/api")
    app.include_router(history.router, prefix="/api")

    return app


app = create_app()
