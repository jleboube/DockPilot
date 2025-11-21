"""
Docker service for managing Docker Engine and Compose
"""
import docker
from docker.errors import DockerException, NotFound, APIError
from typing import List, Dict, Optional, Any
import structlog
import os
import yaml
from pathlib import Path

from app.models.compose import (
    ComposeApp, ServiceInfo, AppState, ContainerState,
    PortMapping, VolumeInfo, ResourceUsage, LogEntry
)
from app.core.config import settings

logger = structlog.get_logger()


class DockerService:
    """Service for interacting with Docker Engine"""

    def __init__(self):
        try:
            self.client = docker.from_env()
            self.api_client = docker.APIClient(base_url=settings.DOCKER_HOST)
            logger.info("docker_client_initialized")
        except DockerException as e:
            logger.error("docker_client_init_failed", error=str(e))
            raise

    def is_docker_available(self) -> bool:
        """Check if Docker engine is available"""
        try:
            self.client.ping()
            return True
        except Exception as e:
            logger.error("docker_ping_failed", error=str(e))
            return False

    def get_docker_info(self) -> Dict[str, Any]:
        """Get Docker engine information"""
        try:
            info = self.client.info()
            return {
                "version": self.client.version(),
                "info": {
                    "containers": info.get("Containers", 0),
                    "images": info.get("Images", 0),
                    "server_version": info.get("ServerVersion", "unknown"),
                    "operating_system": info.get("OperatingSystem", "unknown"),
                    "architecture": info.get("Architecture", "unknown"),
                    "memory_total": info.get("MemTotal", 0),
                    "cpus": info.get("NCPU", 0),
                }
            }
        except Exception as e:
            logger.error("docker_info_failed", error=str(e))
            raise

    def discover_compose_apps(self, search_paths: List[str] = None) -> List[ComposeApp]:
        """
        Discover Docker Compose applications in specified directories
        """
        if search_paths is None:
            search_paths = settings.SEARCH_PATHS

        discovered_apps = []

        for search_path in search_paths:
            path = Path(search_path).expanduser()
            if not path.exists():
                logger.debug("search_path_not_found", path=str(path))
                continue

            logger.info("scanning_directory", path=str(path))

            # Look for docker-compose files
            for compose_file in ["docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"]:
                for compose_path in path.rglob(compose_file):
                    try:
                        app = self._parse_compose_file(compose_path)
                        if app:
                            discovered_apps.append(app)
                            logger.info("compose_app_discovered", name=app.name, path=str(compose_path))
                    except Exception as e:
                        logger.error("compose_parse_failed", path=str(compose_path), error=str(e))

        return discovered_apps

    def _parse_compose_file(self, compose_path: Path) -> Optional[ComposeApp]:
        """Parse a docker-compose.yml file"""
        try:
            with open(compose_path, 'r') as f:
                compose_data = yaml.safe_load(f)

            if not compose_data or 'services' not in compose_data:
                return None

            app_dir = compose_path.parent
            app_name = app_dir.name
            app_id = str(app_dir).replace("/", "_").replace("\\", "_")

            # Get current state by checking containers
            services = []
            app_state = AppState.STOPPED
            total_cpu = 0.0
            total_memory = 0.0

            for service_name, service_config in compose_data.get('services', {}).items():
                service_info = self._get_service_info(app_name, service_name, service_config)
                services.append(service_info)

                if service_info.state == ContainerState.RUNNING:
                    if app_state == AppState.STOPPED:
                        app_state = AppState.PARTIALLY_HEALTHY
                    elif app_state == AppState.PARTIALLY_HEALTHY:
                        pass
                    total_cpu += service_info.cpu_percent
                    total_memory += service_info.memory_mb

            if all(s.state == ContainerState.RUNNING for s in services if s.container_id):
                app_state = AppState.RUNNING
            elif all(s.state != ContainerState.RUNNING for s in services):
                app_state = AppState.STOPPED

            # Extract networks and volumes
            networks = list(compose_data.get('networks', {}).keys())
            volumes = list(compose_data.get('volumes', {}).keys())

            return ComposeApp(
                id=app_id,
                name=app_name,
                path=str(app_dir),
                compose_file=compose_path.name,
                state=app_state,
                services=services,
                networks=networks,
                volumes=volumes,
                cpu_percent=total_cpu,
                memory_mb=total_memory
            )

        except Exception as e:
            logger.error("parse_compose_file_failed", path=str(compose_path), error=str(e))
            return None

    def _get_service_info(self, project_name: str, service_name: str, service_config: Dict) -> ServiceInfo:
        """Get information about a service"""
        # Try to find running container
        container = self._find_container(project_name, service_name)

        image = service_config.get('image', 'unknown')
        ports = []
        volumes = []
        environment = {}

        # Parse port mappings
        port_config = service_config.get('ports', [])
        for port in port_config:
            if isinstance(port, str) and ':' in port:
                parts = port.split(':')
                if len(parts) >= 2:
                    ports.append(PortMapping(
                        host_port=int(parts[0]),
                        container_port=int(parts[-1].split('/')[0]),
                        protocol=parts[-1].split('/')[1] if '/' in parts[-1] else 'tcp'
                    ))

        # Parse environment variables
        env_config = service_config.get('environment', {})
        if isinstance(env_config, dict):
            environment = env_config
        elif isinstance(env_config, list):
            for env in env_config:
                if '=' in env:
                    key, value = env.split('=', 1)
                    environment[key] = value

        if container:
            return ServiceInfo(
                name=service_name,
                image=image,
                container_id=container.id,
                state=ContainerState(container.status),
                ports=ports,
                volumes=volumes,
                environment=environment,
                cpu_percent=0.0,  # Will be updated by stats
                memory_mb=0.0,
                health_status=container.attrs.get('State', {}).get('Health', {}).get('Status')
            )
        else:
            return ServiceInfo(
                name=service_name,
                image=image,
                state=ContainerState.CREATED,
                ports=ports,
                environment=environment
            )

    def _find_container(self, project_name: str, service_name: str) -> Optional[Any]:
        """Find a container by project and service name"""
        try:
            containers = self.client.containers.list(
                all=True,
                filters={
                    'label': [
                        f'com.docker.compose.project={project_name}',
                        f'com.docker.compose.service={service_name}'
                    ]
                }
            )
            return containers[0] if containers else None
        except Exception as e:
            logger.error("find_container_failed", project=project_name, service=service_name, error=str(e))
            return None

    def get_container_stats(self, container_id: str) -> Optional[ResourceUsage]:
        """Get resource usage statistics for a container"""
        try:
            container = self.client.containers.get(container_id)
            stats = container.stats(stream=False)

            # Calculate CPU percentage
            cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                       stats['precpu_stats']['cpu_usage']['total_usage']
            system_delta = stats['cpu_stats']['system_cpu_usage'] - \
                          stats['precpu_stats']['system_cpu_usage']
            cpu_percent = (cpu_delta / system_delta) * len(stats['cpu_stats']['cpu_usage']['percpu_usage']) * 100.0

            # Calculate memory
            memory_mb = stats['memory_stats']['usage'] / (1024 * 1024)
            memory_limit = stats['memory_stats']['limit'] / (1024 * 1024)
            memory_percent = (memory_mb / memory_limit) * 100.0

            # Network stats
            networks = stats.get('networks', {})
            network_rx_mb = sum(net['rx_bytes'] for net in networks.values()) / (1024 * 1024)
            network_tx_mb = sum(net['tx_bytes'] for net in networks.values()) / (1024 * 1024)

            return ResourceUsage(
                cpu_percent=round(cpu_percent, 2),
                memory_mb=round(memory_mb, 2),
                memory_percent=round(memory_percent, 2),
                disk_read_mb=0.0,  # Requires additional calculation
                disk_write_mb=0.0,
                network_rx_mb=round(network_rx_mb, 2),
                network_tx_mb=round(network_tx_mb, 2)
            )
        except Exception as e:
            logger.error("get_container_stats_failed", container_id=container_id, error=str(e))
            return None

    def get_container_logs(self, container_id: str, tail: int = 100, follow: bool = False) -> List[LogEntry]:
        """Get logs from a container"""
        try:
            container = self.client.containers.get(container_id)
            logs = container.logs(
                tail=tail,
                stream=follow,
                timestamps=True,
                stdout=True,
                stderr=True
            )

            entries = []
            if follow:
                # For streaming, return generator
                return logs
            else:
                # For non-streaming, parse logs
                for line in logs.decode('utf-8').split('\n'):
                    if line.strip():
                        # Parse timestamp and message
                        parts = line.split(' ', 1)
                        if len(parts) == 2:
                            entries.append(LogEntry(
                                timestamp=parts[0],
                                service=container.name,
                                message=parts[1],
                                stream='stdout'
                            ))

            return entries
        except Exception as e:
            logger.error("get_container_logs_failed", container_id=container_id, error=str(e))
            return []


docker_service = DockerService()
