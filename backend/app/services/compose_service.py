"""
Docker Compose management service
"""
import subprocess
import os
from pathlib import Path
from typing import Dict, List, Optional
import structlog
import asyncio

from app.models.compose import ComposeApp, AppState

logger = structlog.get_logger()


class ComposeService:
    """Service for managing Docker Compose applications"""

    def __init__(self):
        self.compose_cmd = self._find_compose_command()
        logger.info("compose_service_initialized", command=self.compose_cmd)

    def _find_compose_command(self) -> str:
        """Find the docker compose command (v2 preferred)"""
        # Try docker compose (v2) first - this is the modern standard
        try:
            result = subprocess.run(
                ["docker", "compose", "version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info("docker_compose_v2_detected")
                return "docker compose"
        except Exception as e:
            logger.debug("docker_compose_v2_not_found", error=str(e))

        # Fall back to docker-compose (v1) - legacy
        try:
            result = subprocess.run(
                ["docker-compose", "version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.warning("using_legacy_docker_compose_v1")
                return "docker-compose"
        except Exception as e:
            logger.debug("docker_compose_v1_not_found", error=str(e))

        # Default to docker compose (v2)
        logger.info("defaulting_to_docker_compose_v2")
        return "docker compose"

    async def start_app(self, app: ComposeApp) -> Dict[str, str]:
        """Start a Docker Compose application"""
        try:
            logger.info("starting_app", name=app.name, path=app.path)

            cmd = f"{self.compose_cmd} -f {app.compose_file} up -d"
            result = await self._run_compose_command(cmd, app.path)

            if result["success"]:
                logger.info("app_started", name=app.name)
                return {"status": "success", "message": f"Started {app.name}"}
            else:
                logger.error("app_start_failed", name=app.name, error=result["error"])
                return {"status": "error", "message": result["error"]}

        except Exception as e:
            logger.error("start_app_exception", name=app.name, error=str(e))
            return {"status": "error", "message": str(e)}

    async def stop_app(self, app: ComposeApp) -> Dict[str, str]:
        """Stop a Docker Compose application"""
        try:
            logger.info("stopping_app", name=app.name, path=app.path)

            cmd = f"{self.compose_cmd} -f {app.compose_file} down"
            result = await self._run_compose_command(cmd, app.path)

            if result["success"]:
                logger.info("app_stopped", name=app.name)
                return {"status": "success", "message": f"Stopped {app.name}"}
            else:
                logger.error("app_stop_failed", name=app.name, error=result["error"])
                return {"status": "error", "message": result["error"]}

        except Exception as e:
            logger.error("stop_app_exception", name=app.name, error=str(e))
            return {"status": "error", "message": str(e)}

    async def restart_app(self, app: ComposeApp) -> Dict[str, str]:
        """Restart a Docker Compose application"""
        try:
            logger.info("restarting_app", name=app.name, path=app.path)

            cmd = f"{self.compose_cmd} -f {app.compose_file} restart"
            result = await self._run_compose_command(cmd, app.path)

            if result["success"]:
                logger.info("app_restarted", name=app.name)
                return {"status": "success", "message": f"Restarted {app.name}"}
            else:
                logger.error("app_restart_failed", name=app.name, error=result["error"])
                return {"status": "error", "message": result["error"]}

        except Exception as e:
            logger.error("restart_app_exception", name=app.name, error=str(e))
            return {"status": "error", "message": str(e)}

    async def rebuild_app(self, app: ComposeApp) -> Dict[str, str]:
        """Rebuild and restart a Docker Compose application"""
        try:
            logger.info("rebuilding_app", name=app.name, path=app.path)

            cmd = f"{self.compose_cmd} -f {app.compose_file} up -d --build --force-recreate"
            result = await self._run_compose_command(cmd, app.path)

            if result["success"]:
                logger.info("app_rebuilt", name=app.name)
                return {"status": "success", "message": f"Rebuilt {app.name}"}
            else:
                logger.error("app_rebuild_failed", name=app.name, error=result["error"])
                return {"status": "error", "message": result["error"]}

        except Exception as e:
            logger.error("rebuild_app_exception", name=app.name, error=str(e))
            return {"status": "error", "message": str(e)}

    async def pull_images(self, app: ComposeApp) -> Dict[str, str]:
        """Pull latest images for an application"""
        try:
            logger.info("pulling_images", name=app.name, path=app.path)

            cmd = f"{self.compose_cmd} -f {app.compose_file} pull"
            result = await self._run_compose_command(cmd, app.path)

            if result["success"]:
                logger.info("images_pulled", name=app.name)
                return {"status": "success", "message": f"Pulled images for {app.name}"}
            else:
                logger.error("pull_images_failed", name=app.name, error=result["error"])
                return {"status": "error", "message": result["error"]}

        except Exception as e:
            logger.error("pull_images_exception", name=app.name, error=str(e))
            return {"status": "error", "message": str(e)}

    async def get_app_logs(self, app: ComposeApp, tail: int = 100, follow: bool = False) -> Dict[str, str]:
        """Get logs for a Docker Compose application"""
        try:
            cmd = f"{self.compose_cmd} -f {app.compose_file} logs --tail={tail}"
            if follow:
                cmd += " -f"

            result = await self._run_compose_command(cmd, app.path)

            if result["success"]:
                return {"status": "success", "logs": result["output"]}
            else:
                return {"status": "error", "message": result["error"]}

        except Exception as e:
            logger.error("get_logs_exception", name=app.name, error=str(e))
            return {"status": "error", "message": str(e)}

    async def _run_compose_command(self, command: str, working_dir: str, timeout: int = 120) -> Dict:
        """Run a docker compose command"""
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                cwd=working_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )

                output = stdout.decode('utf-8') if stdout else ""
                error = stderr.decode('utf-8') if stderr else ""

                success = process.returncode == 0

                return {
                    "success": success,
                    "output": output,
                    "error": error if not success else "",
                    "return_code": process.returncode
                }

            except asyncio.TimeoutError:
                process.kill()
                return {
                    "success": False,
                    "output": "",
                    "error": f"Command timed out after {timeout} seconds",
                    "return_code": -1
                }

        except Exception as e:
            logger.error("run_compose_command_failed", command=command, error=str(e))
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "return_code": -1
            }


compose_service = ComposeService()
