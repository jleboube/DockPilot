"""
DockPilot Backend - FastAPI Application
Main entry point for the Docker Compose orchestration API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog

from app.core.config import settings
from app.api.routes import apps, docker, system, logs

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()

# Create FastAPI app
app = FastAPI(
    title="DockPilot API",
    description="Docker Compose orchestration and management API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(apps.router, prefix="/api/apps", tags=["apps"])
app.include_router(docker.router, prefix="/api/docker", tags=["docker"])
app.include_router(system.router, prefix="/api/system", tags=["system"])
app.include_router(logs.router, prefix="/api/logs", tags=["logs"])


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # TODO: Add Docker engine connectivity check
        return JSONResponse(
            content={
                "status": "healthy",
                "version": "1.0.0",
                "services": {
                    "docker": "unknown"
                }
            }
        )
    except Exception as e:
        logger.error("health_check_failed", error=str(e))
        return JSONResponse(
            content={
                "status": "unhealthy",
                "error": str(e)
            },
            status_code=503
        )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "DockPilot API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
