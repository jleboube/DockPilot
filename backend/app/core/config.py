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

    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:38572",
        "http://127.0.0.1:38572",
    ]

    # Docker Settings
    DOCKER_HOST: str = os.getenv("DOCKER_HOST", "unix:///var/run/docker.sock")

    # App Discovery Settings
    SEARCH_PATHS: List[str] = [
        os.path.expanduser("~/docker"),
        os.path.expanduser("~/Docker"),
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
