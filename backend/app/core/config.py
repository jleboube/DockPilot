"""
Configuration management for DockPilot
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_V1_PREFIX: str = "/api"
    PROJECT_NAME: str = "DockPilot"
    VERSION: str = "1.0.0"

    # CORS Settings - Allow all origins for easier deployment
    # In production, you should restrict this to specific domains
    CORS_ORIGINS: List[str] = ["*"]

    # Docker Settings
    DOCKER_HOST: str = os.getenv("DOCKER_HOST", "unix:///var/run/docker.sock")

    # App Discovery Settings
    SEARCH_PATHS: List[str] = [
        "/host/Development",
        "/host/Trying_out",
        "/host/docker",
        "/host/Docker",
        "/opt/apps",
        "/opt/docker",
    ]

    # Resource Monitoring
    RESOURCE_POLL_INTERVAL: int = 2  # seconds

    # Log Settings
    LOG_RETENTION_DAYS: int = 7
    MAX_LOG_LINES: int = 1000

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
