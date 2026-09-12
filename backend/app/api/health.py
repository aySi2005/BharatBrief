"""Health check endpoint."""
from fastapi import APIRouter
from app.services.model_service import model_service

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model_service.is_loaded,
        "version": "1.0.0",
    }
