#!/bin/bash
set -e

echo "=== Docker Environment Sanitization ==="

# Print all DOCKER_* and proxy-related env vars for debugging
echo "Before sanitization:"
env | grep -iE "(docker|proxy)" || echo "No Docker/proxy env vars found"

# Unset DOCKER_HOST if it contains the malformed http+docker scheme
if [[ "$DOCKER_HOST" == *"http+docker"* ]]; then
    echo "WARNING: Detected malformed DOCKER_HOST ($DOCKER_HOST), unsetting it"
    unset DOCKER_HOST
fi

# Clear all proxy variables that might interfere
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy
unset ALL_PROXY all_proxy FTP_PROXY ftp_proxy
unset NO_PROXY no_proxy

# Clear other Docker-related env vars that might cause issues
unset DOCKER_CERT_PATH DOCKER_TLS_VERIFY DOCKER_CONFIG DOCKER_CONTEXT

# Force DOCKER_HOST to unix socket
export DOCKER_HOST="unix:///var/run/docker.sock"
echo "INFO: Set DOCKER_HOST to unix:///var/run/docker.sock"

# Print final state
echo "After sanitization:"
echo "DOCKER_HOST=$DOCKER_HOST"
env | grep -iE "(docker|proxy)" || echo "No other Docker/proxy env vars"

echo "=== Starting Application ==="

# Execute the CMD from Dockerfile
exec "$@"
