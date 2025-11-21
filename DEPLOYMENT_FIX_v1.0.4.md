# DockPilot v1.0.4 Deployment Fix

## Issue Summary
Backend container failing to start with error:
```
docker.errors.DockerException: Error while fetching server API version: Not supported URL scheme http+docker
```

## Root Cause
Your remote VM has a `DOCKER_HOST` environment variable set to a malformed value (likely `http+docker://...`). This was being inherited by the container despite our explicit settings in docker-compose.yml.

## Solution Applied
1. **Added URL validation and sanitization** in `backend/app/services/docker_service.py`
   - Explicitly rejects URLs containing "http+docker" scheme
   - Validates that only proper schemes are used (unix://, tcp://, http://, https://)
   - Falls back to `unix:///var/run/docker.sock` for any invalid values
   - Logs warnings when invalid values are detected

2. **Changed docker-compose.yml environment syntax**
   - Changed from array syntax: `- DOCKER_HOST=value`
   - To key:value syntax: `DOCKER_HOST: "value"`
   - This provides stronger override of host environment variables

## Deployment Steps

### On Your Remote VM:

```bash
# 1. Navigate to DockPilot directory
cd ~/DockPilot  # (or wherever you cloned it)

# 2. Stop running containers
docker compose down

# 3. Pull latest changes from git
git pull origin main

# 4. Rebuild and start containers
docker compose up -d --build

# 5. Check backend logs for validation warnings
docker compose logs backend | grep -E "(docker_host|warning)"

# 6. Verify backend is healthy
docker compose ps
curl http://localhost:48391/health

# 7. Access the application
# Open browser to: http://localhost:38572
```

## Verification

After deployment, check the backend logs. You should see:

**If the host DOCKER_HOST was malformed:**
```
invalid_docker_host_detected original=http+docker://... using_default=unix:///var/run/docker.sock
docker_client_initialized base_url=unix:///var/run/docker.sock
```

**If everything is clean:**
```
docker_client_initialized base_url=unix:///var/run/docker.sock
```

## Optional: Clean Up Host Environment

If you want to prevent this issue at the source, you can check and unset the malformed DOCKER_HOST on your host:

```bash
# Check current value
echo $DOCKER_HOST

# If it shows something like "http+docker://...", unset it
unset DOCKER_HOST

# Or set it correctly
export DOCKER_HOST=unix:///var/run/docker.sock

# Make it permanent (add to ~/.bashrc or ~/.profile)
echo 'export DOCKER_HOST=unix:///var/run/docker.sock' >> ~/.bashrc
```

## Troubleshooting

### If backend still fails:
1. Check the backend logs: `docker compose logs backend`
2. Verify Docker socket is mounted: `docker compose exec backend ls -la /var/run/docker.sock`
3. Check if Docker socket has correct permissions: `ls -la /var/run/docker.sock` on host
4. Ensure your user is in the docker group: `groups $USER | grep docker`

### If frontend can't reach backend:
1. Verify backend is healthy: `docker compose ps`
2. Test backend directly: `curl http://localhost:48391/health`
3. Check backend logs: `docker compose logs backend`

## Expected Result

After successful deployment:
- Backend container status: **healthy**
- Frontend container status: **healthy**
- Application accessible at: **http://localhost:38572**
- Backend API accessible at: **http://localhost:48391**

## Files Changed in v1.0.4

1. `backend/app/services/docker_service.py` - Added URL validation
2. `docker-compose.yml` - Changed environment variable syntax
3. `CHANGELOG.md` - Documented the fix

## Version Information

- **Current Version**: v1.0.4
- **Date**: 2024-11-21
- **Git Commit**: Check with `git log -1 --oneline`

## Support

If issues persist after deployment, please provide:
1. Full backend logs: `docker compose logs backend > backend-logs.txt`
2. Docker environment: `docker compose exec backend env | grep DOCKER`
3. Host DOCKER_HOST value: `echo $DOCKER_HOST`
