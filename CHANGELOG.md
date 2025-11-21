# Changelog

All notable changes to DockPilot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-20

### Added
- Initial release of DockPilot
- Docker Compose app discovery engine
- Dashboard with unified app management
- Real-time resource monitoring (CPU, memory, disk)
- System stats display
- App lifecycle management (start, stop, restart, rebuild)
- Service-level status tracking
- Container health monitoring
- Docker engine integration
- Modern dark mode UI with Tailwind CSS
- FastAPI backend with comprehensive API
- Next.js 14 frontend with TypeScript
- Docker Compose orchestration
- Health checks for all services
- Comprehensive documentation
- Quick start scripts
- Makefile with convenience commands

### Technical Details
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, Lucide Icons
- **Backend**: FastAPI, Python 3.11, Docker SDK
- **Infrastructure**: Docker, Docker Compose v2
- **Monitoring**: psutil for system metrics
- **Logging**: structlog for structured logging

### API Endpoints
- `GET /api/apps/` - List all apps
- `POST /api/apps/discover` - Discover apps
- `GET /api/apps/{id}` - Get app details
- `POST /api/apps/{id}/action` - Perform action
- `GET /api/apps/{id}/stats` - Get statistics
- `GET /api/apps/{id}/logs` - Get logs
- `GET /api/docker/info` - Docker info
- `GET /api/docker/status` - Docker status
- `GET /api/system/info` - System info
- `GET /api/system/ports` - Open ports
- `GET /health` - Health check

### Security
- Read-only Docker socket mounting
- Non-root container users
- CORS protection
- Local-first architecture
- No cloud dependencies

### Documentation
- README.md with comprehensive guide
- QUICKSTART.md for fast setup
- CONTRIBUTING.md with guidelines
- PROJECT_SUMMARY.md with technical details
- API documentation via Swagger UI

## [1.0.4] - 2024-11-21

### Fixed
- Fixed Docker client initialization error: "Not supported URL scheme http+docker"
- Changed from `docker.from_env()` to explicit `docker.DockerClient(base_url=...)`
- Added validation and sanitization for DOCKER_HOST environment variable
- Explicitly reject malformed URLs containing "http+docker" scheme
- Added scheme validation to ensure only valid Docker connection URLs
- Changed docker-compose.yml to use explicit key:value syntax to prevent host environment variable override
- Added warning logs when invalid DOCKER_HOST detected

### Technical Details
The Docker SDK was attempting to parse a malformed DOCKER_HOST environment variable from the host system, resulting in an invalid URL scheme (`http+docker`). This was happening because docker-compose was inheriting the host's DOCKER_HOST variable despite our explicit setting. By adding URL validation and sanitization logic, and changing the docker-compose syntax to use explicit key:value pairs instead of array syntax, we ensure the container always uses a valid Docker socket connection.

### Root Cause
The host system had a `DOCKER_HOST` environment variable set with a malformed value. Docker Compose's array-style environment syntax (`- VAR=value`) can still inherit host variables, while the key:value syntax (`VAR: "value"`) provides explicit override.

### Files Modified
- `backend/app/services/docker_service.py` - Added URL validation and sanitization (lines 24-56)
- `docker-compose.yml` - Changed environment syntax to explicit key:value format

## [1.0.3] - 2024-11-20

### Fixed
- Fixed Docker build error: "public directory not found"
- Added `mkdir -p public` in builder stage to ensure directory exists
- Created `frontend/public` directory with placeholder files
- Added favicon.ico and robots.txt to public directory

### Files Modified
- `frontend/Dockerfile` - Added public directory creation in builder
- `frontend/public/.gitkeep` - Ensures directory is tracked
- `frontend/public/favicon.ico` - Placeholder favicon
- `frontend/public/robots.txt` - Basic robots.txt

## [1.0.2] - 2024-11-20

### Changed
- **Security Enhancement**: Changed default ports to non-standard values
  - Frontend: `3000` → `38572`
  - Backend: `8000` → `48391`
- Updated all documentation with new port numbers
- Updated CORS configuration for new frontend port

### Rationale
Using non-standard ports reduces exposure to automated port scanning and common exploits targeting default application ports.

### Files Modified
- `docker-compose.yml` - Updated port mappings
- All `.env.example` files - New port configurations
- `backend/app/core/config.py` - Updated CORS origins
- `frontend/src/lib/api.ts` - Updated API base URL
- `start.sh`, `stop.sh`, `Makefile` - Updated port references
- All documentation files - Updated URLs

## [1.0.1] - 2024-11-20

### Fixed
- Removed deprecated `version` field from docker-compose.yml
- Updated all commands to use `docker compose` (v2 syntax without hyphen)
- Fixed Next.js build issue in Docker by ensuring proper package.json copy
- Added `--legacy-peer-deps` flag to npm ci for better compatibility
- Updated compose service to prefer Docker Compose v2

### Changed
- All scripts now use `docker compose` instead of `docker-compose`
- Improved Docker Compose command detection with better logging
- Enhanced build reliability with package.json copied to builder stage

### Files Modified
- `docker-compose.yml` - Removed version field
- `frontend/Dockerfile` - Fixed build process, added legacy-peer-deps flag
- `start.sh` - Updated to use docker compose
- `stop.sh` - Updated to use docker compose
- `Makefile` - Updated all compose commands
- `backend/app/services/compose_service.py` - Improved command detection

---

## Upcoming (v1.1)

### Planned Features
- Systemd/Launchd integration for auto-start on boot
- Real-time log streaming with WebSockets
- Compose file editor with YAML validation
- Environment variable editor with secret masking
- Image update notifications and management
- Port conflict detection and automatic resolution
- Volume management and relocation
- Enhanced resource monitoring with historical data

### Planned Improvements
- Persistent storage for app metadata (SQLite/PostgreSQL)
- User preferences and settings persistence
- Custom notification preferences
- Multi-language support
- Keyboard shortcuts
- Dark/light mode toggle
- Export app configurations

---

## Future (v2.0)

### Long-term Roadmap
- Remote Docker host management via SSH
- Multi-host orchestration
- GitOps-style sync with Git repositories
- Application template marketplace
- Backup and restore functionality
- Plugin system for extensions
- CLI companion tool (`dockpilot-cli`)
- Desktop application packaging (Electron/Tauri)
- Mobile companion app
- Team collaboration features
- RBAC and user management
- Audit logging
- Prometheus metrics export
- Grafana dashboard templates

---

## Version History

- **v1.0.4** (2024-11-21) - Fixed Docker client initialization error
- **v1.0.3** (2024-11-20) - Fixed Docker build error with public directory
- **v1.0.2** (2024-11-20) - Security: Changed to non-standard ports
- **v1.0.1** (2024-11-20) - Bug fixes for Docker Compose v2 compatibility
- **v1.0.0** (2024-11-20) - Initial release with core MVP features

---

## Migration Guides

### Upgrading from v1.0.1 to v1.0.2

Port numbers have changed for security:

```bash
# Stop current version
docker compose down

# Pull latest changes
git pull

# Update your .env file if you created one
# Change:
#   NEXT_PUBLIC_API_URL=http://localhost:8000
#   CORS_ORIGINS=http://localhost:3000,...
# To:
#   NEXT_PUBLIC_API_URL=http://localhost:48391
#   CORS_ORIGINS=http://localhost:38572,...

# Rebuild and start
docker compose up -d --build

# Access new URLs:
# - Frontend: http://localhost:38572
# - Backend: http://localhost:48391
```

### Upgrading from v1.0.0 to v1.0.1

No migration steps required. Simply pull the latest changes and rebuild:

```bash
# Stop current version
docker compose down

# Pull latest changes
git pull

# Rebuild and start
docker compose up -d --build
```

---

## Breaking Changes

### v1.0.2
- **Port Numbers Changed**: Default ports have changed for security
  - Frontend: `3000` → `38572`
  - Backend: `8000` → `48391`
  - Update any bookmarks, scripts, or configurations that reference the old ports

### v1.0.1
- None - This is a backward-compatible bug fix release

### v1.0.0
- Initial release - No breaking changes

---

## Known Issues

### v1.0.1
- Logs are not streaming in real-time (polling-based, 5s refresh)
- No persistence for app metadata between restarts
- Auto-start on boot not implemented
- Single host support only
- No user authentication

---

## Contributors

- Joe LeBoube (@joeleboube) - Initial development
- Built with assistance from Claude Code by Anthropic

---

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/yourusername/DockPilot/issues
- Documentation: See README.md
- Quick Start: See QUICKSTART.md
- Contributing: See CONTRIBUTING.md
