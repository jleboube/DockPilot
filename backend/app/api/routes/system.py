"""
API routes for system information and resources
"""
from fastapi import APIRouter, HTTPException
import psutil
import structlog
from typing import Dict, Any

logger = structlog.get_logger()

router = APIRouter()


@router.get("/info")
async def get_system_info() -> Dict[str, Any]:
    """Get system information"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        return {
            "cpu": {
                "count": psutil.cpu_count(),
                "percent": cpu_percent,
            },
            "memory": {
                "total_mb": memory.total / (1024 * 1024),
                "available_mb": memory.available / (1024 * 1024),
                "used_mb": memory.used / (1024 * 1024),
                "percent": memory.percent,
            },
            "disk": {
                "total_gb": disk.total / (1024 * 1024 * 1024),
                "used_gb": disk.used / (1024 * 1024 * 1024),
                "free_gb": disk.free / (1024 * 1024 * 1024),
                "percent": disk.percent,
            },
            "platform": psutil.os.name,
        }
    except Exception as e:
        logger.error("get_system_info_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ports")
async def get_open_ports():
    """Get list of open network ports"""
    try:
        connections = psutil.net_connections(kind='inet')
        ports = set()

        for conn in connections:
            if conn.laddr and conn.status == 'LISTEN':
                ports.add(conn.laddr.port)

        return {
            "ports": sorted(list(ports)),
            "count": len(ports)
        }
    except Exception as e:
        logger.error("get_open_ports_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
