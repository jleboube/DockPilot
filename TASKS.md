# DockPilot Development Tasks & Changes

## Session Summary (2025-11-21)

### Issue 1: Docker SDK "Not supported URL scheme http+docker" Error

**Root Cause**: Library version incompatibility between docker-py and requests>=2.32.0

The docker-py library's `UnixHTTPAdapter` didn't override the new `get_connection_with_tls_context()` method added in requests 2.32.0, causing Unix socket connections to fail.

**Solution**: Downgraded library versions in `backend/requirements.txt`:
- `requests<2.32.0` (uses 2.31.0)
- `urllib3<2.0.0` (uses 1.26.20)

### Issue 2: Remote Deployment Issues

**Issue 2a - Backend Healthcheck**: Backend marked unhealthy
- Fixed healthcheck to use Python instead of curl (curl not installed in container)

**Issue 2b - Network Error**: Frontend couldn't connect from remote browser
- Made API URL dynamic using `window.location.hostname` instead of hardcoded localhost

**Issue 2c - CORS Blocking**: OPTIONS preflight requests returning 400
- Changed `CORS_ORIGINS` from localhost-only to `["*"]` to allow all origins

### Issue 3: Discover Apps Returns 422 Error

**Root Cause**: FastAPI request validation failure

The frontend was sending `search_paths` in the request body, but the backend endpoint defined it as a default parameter (which FastAPI treats as a query parameter).

**Solution**: Created Pydantic model for request body
- Added `DiscoverAppsRequest` model to `backend/app/models/compose.py`
- Updated `/api/apps/discover` endpoint to accept request body parameter

### Changes Made

1. **backend/requirements.txt**
   - Added version constraints for requests and urllib3
   - Ensures compatibility with docker-py 6.1.3

2. **docker-compose.yml**
   - Fixed backend healthcheck to use Python instead of curl
   - Changed from: `["CMD", "curl", "-f", "http://localhost:8000/health"]`
   - Changed to: `["CMD", "python", "-c", "import requests; exit(0 if requests.get('http://localhost:8000/health').status_code == 200 else 1)"]`

3. **frontend/src/lib/api.ts**
   - Made API base URL dynamic based on `window.location.hostname`
   - Allows remote access without hardcoding localhost

4. **backend/app/core/config.py**
   - Changed `CORS_ORIGINS` from `["http://localhost:*", "http://127.0.0.1:*"]` to `["*"]`
   - Allows requests from any origin

5. **backend/app/models/compose.py**
   - Added `DiscoverAppsRequest` Pydantic model
   - Properly defines request body structure for discover endpoint

6. **backend/app/api/routes/apps.py**
   - Updated `/discover` endpoint to accept `DiscoverAppsRequest` body parameter
   - Changed from query parameter to request body parameter

### Testing Results
   - ✅ Backend starts successfully
   - ✅ Docker client initializes without errors
   - ✅ All API endpoints respond correctly
   - ✅ Both containers are healthy
   - ✅ Frontend connects to backend successfully from remote browser
   - ✅ Statistics displaying correctly
   - ✅ Discover Apps endpoint fixed (422 error resolved)

## Previous Session Tasks

### v1.0.4 - Docker Client Initialization Fix
- Added entrypoint script for environment sanitization
- Changed Docker client initialization from `from_env()` to explicit `base_url`
- Added comprehensive logging for debugging

### v1.0.3 - Docker Build Fix
- Fixed "public directory not found" error
- Created frontend/public directory with placeholder files

### v1.0.2 - Port Security Enhancement
- Changed default ports to non-standard values:
  - Frontend: 3000 → 38572
  - Backend: 8000 → 48391

### v1.0.1 - Docker Compose v2 Compatibility
- Removed deprecated `version` field from docker-compose.yml
- Updated all commands to use `docker compose` (v2 syntax)
- Fixed Next.js build with `--legacy-peer-deps` flag

### v1.0.0 - Initial Release
- Full Docker Compose management application
- FastAPI backend with Python 3.11
- Next.js 14 frontend with TypeScript
- Real-time resource monitoring
- App lifecycle management (start/stop/restart/rebuild)
- Health checks for all services

## Deployment Instructions

On your remote VM:

```bash
cd ~/DockPilot

# Stop containers
docker compose down

# Pull latest changes
git pull origin main

# Rebuild backend with updated dependencies
docker compose build --no-cache backend

# Start containers
docker compose up -d

# Verify
docker compose ps
docker compose logs backend | head -30
```

Expected output should show:
```
docker_client_initialized_successfully base_url=unix:///var/run/docker.sock
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## Known Issues

None currently. Application is fully functional.

## Future Improvements

1. **Library Upgrades**: Monitor docker-py repository for fixes to UnixHTTPAdapter
2. **Frontend Discovery**: Implement Docker Compose app auto-discovery
3. **Real-time Logs**: Add WebSocket support for live log streaming
4. **Resource Monitoring**: Add historical data for CPU/memory usage
