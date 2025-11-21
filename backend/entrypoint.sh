#!/bin/bash
set -e

# Unset DOCKER_HOST if it contains the malformed http+docker scheme
# The Docker SDK reads this environment variable internally, overriding our base_url parameter
if [[ "$DOCKER_HOST" == *"http+docker"* ]]; then
    echo "WARNING: Detected malformed DOCKER_HOST ($DOCKER_HOST), unsetting it"
    unset DOCKER_HOST
fi

# If DOCKER_HOST is not set, set it to the unix socket
if [ -z "$DOCKER_HOST" ]; then
    export DOCKER_HOST="unix:///var/run/docker.sock"
    echo "INFO: Set DOCKER_HOST to unix:///var/run/docker.sock"
fi

echo "INFO: Starting application with DOCKER_HOST=$DOCKER_HOST"

# Execute the CMD from Dockerfile
exec "$@"
