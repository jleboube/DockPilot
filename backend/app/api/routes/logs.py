"""
API routes for log management
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List
import structlog

from app.models.compose import LogEntry
from app.services.docker_service import docker_service

logger = structlog.get_logger()

router = APIRouter()


@router.get("/container/{container_id}")
async def get_container_logs(
    container_id: str,
    tail: int = Query(100, ge=1, le=10000)
) -> List[LogEntry]:
    """Get logs from a specific container"""
    try:
        logs = docker_service.get_container_logs(container_id, tail=tail)
        return logs
    except Exception as e:
        logger.error("get_container_logs_failed", container_id=container_id, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
