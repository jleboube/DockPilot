"""
API routes for Docker engine information
"""
from fastapi import APIRouter, HTTPException
import structlog

from app.services.docker_service import docker_service

logger = structlog.get_logger()

router = APIRouter()


@router.get("/info")
async def get_docker_info():
    """Get Docker engine information"""
    try:
        if not docker_service.is_docker_available():
            raise HTTPException(status_code=503, detail="Docker engine is not available")

        info = docker_service.get_docker_info()
        return info
    except Exception as e:
        logger.error("get_docker_info_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_docker_status():
    """Check if Docker engine is available"""
    try:
        available = docker_service.is_docker_available()
        return {
            "available": available,
            "status": "healthy" if available else "unavailable"
        }
    except Exception as e:
        logger.error("get_docker_status_failed", error=str(e))
        return {
            "available": False,
            "status": "error",
            "error": str(e)
        }
