# Debug Instructions for Docker SDK Issue

The Docker SDK is still trying to connect to `http+docker` even though `DOCKER_HOST` is correctly set to `unix:///var/run/docker.sock`.

## Run These Commands on Your Remote VM

```bash
# 1. Check ALL environment variables in the container
docker compose exec backend env | sort

# 2. Check for Docker config files
docker compose exec backend ls -la ~/.docker/
docker compose exec backend cat ~/.docker/config.json 2>/dev/null || echo "No config file"

# 3. Check docker context (if any)
docker compose exec backend sh -c "which docker && docker context ls" 2>/dev/null || echo "docker CLI not installed in container"

# 4. Check if there are any other DOCKER_* environment variables
docker compose exec backend env | grep -i docker

# 5. Check Python's docker module configuration
docker compose exec backend python -c "import docker; import os; print('DOCKER_HOST:', os.environ.get('DOCKER_HOST')); print('HOME:', os.environ.get('HOME'))"

# 6. Start the backend interactively to see all entrypoint output
docker compose run --rm backend bash
# Then inside the container:
env | grep -i docker
ls -la ~/.docker/
cat /entrypoint.sh
exit
```

## Send Me These Outputs

1. Full environment variables from step 1
2. Any Docker config files from step 2
3. Output from step 4 (DOCKER_* variables)
4. Output from step 5 (Python check)

This will help me identify where the `http+docker` value is coming from.

## Possible Causes

1. **Docker context configuration** - Docker CLI contexts can override DOCKER_HOST
2. **~/.docker/config.json** - May contain host configuration
3. **Another environment variable** - Like DOCKER_CERT_PATH, DOCKER_TLS_VERIFY, etc.
4. **Cached Docker SDK state** - The SDK might be caching configuration
5. **Python requests configuration** - The requests library might have proxy settings

## Quick Test

Try this to completely override everything:

```bash
# Edit docker-compose.yml and add to backend environment:
environment:
  DOCKER_HOST: "unix:///var/run/docker.sock"
  DOCKER_CERT_PATH: ""
  DOCKER_TLS_VERIFY: ""
  NO_PROXY: "*"
  HTTP_PROXY: ""
  HTTPS_PROXY: ""

# Then rebuild and restart
docker compose down
docker compose build --no-cache backend
docker compose up -d
docker compose logs backend | head -100
```
