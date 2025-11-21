"""
Models for Docker Compose applications
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum


class AppState(str, Enum):
    """Application states"""
    RUNNING = "running"
    STOPPED = "stopped"
    PARTIALLY_HEALTHY = "partially_healthy"
    ERROR = "error"
    UNKNOWN = "unknown"


class ContainerState(str, Enum):
    """Container states"""
    RUNNING = "running"
    EXITED = "exited"
    PAUSED = "paused"
    RESTARTING = "restarting"
    DEAD = "dead"
    CREATED = "created"
    REMOVING = "removing"


class PortMapping(BaseModel):
    """Port mapping information"""
    host_port: int
    container_port: int
    protocol: str = "tcp"


class VolumeInfo(BaseModel):
    """Volume information"""
    name: str
    source: str
    destination: str
    mode: str = "rw"
    size_mb: Optional[float] = None


class ServiceInfo(BaseModel):
    """Docker Compose service information"""
    name: str
    image: str
    container_id: Optional[str] = None
    state: ContainerState = ContainerState.CREATED
    ports: List[PortMapping] = []
    volumes: List[VolumeInfo] = []
    environment: Dict[str, str] = {}
    cpu_percent: float = 0.0
    memory_mb: float = 0.0
    memory_limit_mb: Optional[float] = None
    health_status: Optional[str] = None


class ComposeApp(BaseModel):
    """Docker Compose application"""
    id: str
    name: str
    path: str
    compose_file: str
    state: AppState
    services: List[ServiceInfo] = []
    networks: List[str] = []
    volumes: List[str] = []
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    auto_start: bool = False
    cpu_percent: float = 0.0
    memory_mb: float = 0.0


class ComposeAppCreate(BaseModel):
    """Create a new compose app"""
    path: str
    compose_file: str = "docker-compose.yml"
    name: Optional[str] = None


class ComposeAppUpdate(BaseModel):
    """Update compose app settings"""
    auto_start: Optional[bool] = None
    environment: Optional[Dict[str, str]] = None


class AppActionRequest(BaseModel):
    """Request to perform an action on an app"""
    action: str = Field(..., description="Action to perform: start, stop, restart, rebuild")


class ResourceUsage(BaseModel):
    """Resource usage information"""
    cpu_percent: float
    memory_mb: float
    memory_percent: float
    disk_read_mb: float
    disk_write_mb: float
    network_rx_mb: float
    network_tx_mb: float


class LogEntry(BaseModel):
    """Log entry"""
    timestamp: str
    service: str
    message: str
    stream: str = "stdout"  # stdout or stderr


class HealthCheck(BaseModel):
    """Health check status"""
    service: str
    status: str
    last_check: str
    failures: int = 0
