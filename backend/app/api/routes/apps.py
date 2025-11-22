"""
API routes for Docker Compose application management
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import structlog

from app.models.compose import ComposeApp, AppActionRequest, ResourceUsage, DiscoverAppsRequest
from app.services.docker_service import docker_service
from app.services.compose_service import compose_service

logger = structlog.get_logger()

router = APIRouter()

# In-memory storage (will be replaced with persistent storage in v1.1)
discovered_apps: dict[str, ComposeApp] = {}


@router.get("/", response_model=List[ComposeApp])
async def list_apps():
    """List all discovered Docker Compose applications"""
    try:
        # Return cached apps (empty if not discovered yet)
        # User must click "Discover Apps" button to scan
        return list(discovered_apps.values())
    except Exception as e:
        logger.error("list_apps_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/discover")
async def refresh_apps(request: DiscoverAppsRequest = DiscoverAppsRequest()):
    """Discover/refresh Docker Compose applications"""
    try:
        logger.info("discovering_apps", search_paths=request.search_paths)
        apps = docker_service.discover_compose_apps(request.search_paths)

        # Update cache
        discovered_apps.clear()
        for app in apps:
            discovered_apps[app.id] = app

        logger.info("apps_discovered", count=len(apps))
        return {
            "status": "success",
            "count": len(apps),
            "apps": apps
        }
    except Exception as e:
        logger.error("discover_apps_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{app_id}", response_model=ComposeApp)
async def get_app(app_id: str):
    """Get details of a specific application"""
    if app_id not in discovered_apps:
        raise HTTPException(status_code=404, detail=f"App {app_id} not found")

    return discovered_apps[app_id]


@router.post("/{app_id}/action")
async def perform_action(app_id: str, request: AppActionRequest):
    """Perform an action on an application (start, stop, restart, rebuild)"""
    if app_id not in discovered_apps:
        raise HTTPException(status_code=404, detail=f"App {app_id} not found")

    app = discovered_apps[app_id]
    action = request.action.lower()

    try:
        if action == "start":
            result = await compose_service.start_app(app)
        elif action == "stop":
            result = await compose_service.stop_app(app)
        elif action == "restart":
            result = await compose_service.restart_app(app)
        elif action == "rebuild":
            result = await compose_service.rebuild_app(app)
        elif action == "pull":
            result = await compose_service.pull_images(app)
        else:
            raise HTTPException(status_code=400, detail=f"Invalid action: {action}")

        # Refresh app state after action
        await refresh_apps()

        return result
    except Exception as e:
        logger.error("action_failed", app_id=app_id, action=action, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{app_id}/stats")
async def get_app_stats(app_id: str):
    """Get resource usage statistics for an application"""
    if app_id not in discovered_apps:
        raise HTTPException(status_code=404, detail=f"App {app_id} not found")

    app = discovered_apps[app_id]

    try:
        stats = []
        for service in app.services:
            if service.container_id:
                service_stats = docker_service.get_container_stats(service.container_id)
                if service_stats:
                    stats.append({
                        "service": service.name,
                        "stats": service_stats
                    })

        return {
            "app_id": app_id,
            "app_name": app.name,
            "stats": stats
        }
    except Exception as e:
        logger.error("get_stats_failed", app_id=app_id, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{app_id}/logs")
async def get_app_logs(
    app_id: str,
    tail: int = Query(100, ge=1, le=10000),
    follow: bool = False
):
    """Get logs for an application"""
    if app_id not in discovered_apps:
        raise HTTPException(status_code=404, detail=f"App {app_id} not found")

    app = discovered_apps[app_id]

    try:
        result = await compose_service.get_app_logs(app, tail=tail, follow=follow)
        return result
    except Exception as e:
        logger.error("get_logs_failed", app_id=app_id, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
