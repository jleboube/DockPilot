# URGENT: DockPilot Container Rebuild Required

## Problem
The Docker SDK is internally reading a malformed `DOCKER_HOST` environment variable **even when we explicitly provide a base_url parameter**. This causes the "Not supported URL scheme http+docker" error.

## Root Cause Analysis (UPDATED)
1. Your host system has `DOCKER_HOST` set to a malformed value like `http+docker://...`
2. Docker Compose passes this malformed value to the container
3. Our Python code correctly reads `unix:///var/run/docker.sock` from settings
4. **BUT** the Docker SDK (docker-py) **ignores our base_url** and reads `DOCKER_HOST` from the environment internally
5. The Docker SDK fails when it tries to connect using the malformed environment variable

### Evidence from Latest Logs
```
docker_host_from_settings      type=str value=unix:///var/run/docker.sock
using_docker_host              base_url=unix:///var/run/docker.sock
docker_client_init_failed      base_url=unix:///var/run/docker.sock error=Error while fetching server API version: Not supported URL scheme http+docker
```

Our code is using the correct URL, but the Docker SDK is still trying `http+docker`!

## Solution
Added an **entrypoint script** that sanitizes the DOCKER_HOST environment variable **before** Python starts. This prevents the Docker SDK from reading the malformed value.

**Latest commit (a829d09)** includes:
- **entrypoint.sh** - Detects and unsets malformed DOCKER_HOST at container startup
- Comprehensive DOCKER_HOST validation in Python code
- Malformed URL detection and sanitization
- Fallback to `unix:///var/run/docker.sock`
- Extensive logging for debugging

## Deployment Steps (ON YOUR REMOTE VM)

```bash
# Step 1: Navigate to project directory
cd ~/DockPilot  # or wherever you have DockPilot

# Step 2: Stop containers
docker compose down

# Step 3: Pull latest code from git
git pull origin main

# You should see these new commits:
# - a829d09 "fix: Add entrypoint script to handle malformed DOCKER_HOST" (CRITICAL FIX)
# - 1ed9271 "feat: Add comprehensive logging and improved validation"
# - b3ad32f "Fix: Add validation and sanitization for DOCKER_HOST"

# Step 4: REBUILD the containers (this is critical!)
docker compose build --no-cache backend

# Step 5: Start containers
docker compose up -d

# Step 6: Check logs for validation messages
docker compose logs backend | head -50

# You should see new log messages like:
# - "docker_host_from_settings"
# - "docker_host_http_plus_docker_detected" (if malformed)
# - "using_docker_host"
# - "docker_client_initialized_successfully"

# Step 7: Verify backend is healthy
docker compose ps

# Step 8: Access the application
# Open browser: http://your-vm-ip:38572
```

## Expected Log Output (with fix applied)

**From entrypoint.sh** (before Python starts):
```
WARNING: Detected malformed DOCKER_HOST (http+docker://...), unsetting it
INFO: Set DOCKER_HOST to unix:///var/run/docker.sock
INFO: Starting application with DOCKER_HOST=unix:///var/run/docker.sock
```

**From Python application:**
```
docker_host_from_settings value=unix:///var/run/docker.sock type=str
using_docker_host base_url=unix:///var/run/docker.sock
docker_client_initialized_successfully base_url=unix:///var/run/docker.sock
```

## Verification Checklist

- [ ] Git pull completed successfully
- [ ] Backend container rebuilt with `--no-cache`
- [ ] Backend logs show "docker_host_from_settings" message
- [ ] Backend logs show "docker_client_initialized_successfully"
- [ ] Backend container status is "healthy"
- [ ] Frontend container status is "healthy"
- [ ] Can access application at http://your-vm-ip:38572

## If It Still Fails

If the backend still fails after rebuilding, provide:

1. **Exact rebuild command output:**
   ```bash
   docker compose build --no-cache backend 2>&1 | tee rebuild.log
   ```

2. **First 100 lines of backend logs:**
   ```bash
   docker compose logs backend | head -100 > backend-startup.log
   ```

3. **Environment variables in container:**
   ```bash
   docker compose exec backend env | grep -i docker
   ```

4. **Host DOCKER_HOST value:**
   ```bash
   echo "Host DOCKER_HOST: $DOCKER_HOST"
   ```

## Why Rebuild Is Required

The error shows:
```
File "/app/app/services/docker_service.py", line 51, in __init__
    self.client = docker.DockerClient(base_url=base_url)
```

But the current code has validation from lines 24-67. This means the container is running OLD code from a previous build. You must rebuild to get the new validation logic.

## Key Points

1. **Just pulling code is not enough** - You must **rebuild the image**
2. Use `--no-cache` to ensure Docker doesn't use cached layers
3. The new code will **automatically detect and fix** the malformed DOCKER_HOST
4. After rebuild, the backend should start successfully

## Alternative: Run Without DOCKER_HOST

If you want to prevent this issue at the source, you can unset DOCKER_HOST on the host:

```bash
# Check current value
echo $DOCKER_HOST

# Unset it
unset DOCKER_HOST

# Or add to docker-compose.yml:
environment:
  DOCKER_HOST: "unix:///var/run/docker.sock"
```

But the code fix should handle this automatically now.

---

**Created:** 2024-11-21
**Version:** v1.0.4 (with enhanced validation)
**Commit:** 1ed9271
