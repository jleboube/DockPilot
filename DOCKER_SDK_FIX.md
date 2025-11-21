# Docker SDK Fix - "Not supported URL scheme http+docker"

## Problem Summary

The application was failing to start with the error:
```
docker.errors.DockerException: Error while fetching server API version: Not supported URL scheme http+docker
```

## Root Cause

The issue was caused by an **incompatibility between docker-py and newer versions of the requests library**.

### Technical Details

1. **Docker SDK Behavior**: The `docker-py` library uses a custom `UnixHTTPAdapter` to handle Unix socket connections via the `http+docker://` URL scheme.

2. **Requests Library Change**: In `requests>=2.32.0`, a new method `get_connection_with_tls_context()` was added to the `HTTPAdapter` class.

3. **Missing Override**: The `UnixHTTPAdapter` in docker-py did not override this new method, causing it to fall back to the parent class implementation which doesn't understand the `http+docker://` scheme.

4. **Error Chain**:
   - Docker SDK converts `unix:///var/run/docker.sock` → `http+docker://localhost`
   - Mounts `UnixHTTPAdapter` to handle `http+docker://` URLs
   - When making requests, the adapter's `send()` method calls `get_connection_with_tls_context()`
   - Since `UnixHTTPAdapter` doesn't override this method, it uses the parent class version
   - The parent class tries to parse `http+docker://` as a standard HTTP URL
   - `urllib3` rejects the unknown scheme → error

## The Fix

Downgrade `requests` and `urllib3` to versions before this breaking change:

```txt
# In requirements.txt
requests<2.32.0  # Use 2.31.0
urllib3<2.0.0    # Use 1.26.x
```

### Why This Works

- `requests 2.31.0` and earlier don't have the `get_connection_with_tls_context()` method
- The Docker SDK's existing `get_connection()` override in `UnixHTTPAdapter` works correctly with these versions
- `urllib3 1.26.x` is compatible with this requests version

## Implementation in DockPilot

### Files Modified

1. **backend/requirements.txt**
   - Added version constraints for `requests` and `urllib3`
   - Ensures compatibility with docker-py

### What Was NOT the Issue

Despite extensive troubleshooting, these were NOT the root cause:
- ❌ Environment variables (DOCKER_HOST, HTTP_PROXY, etc.)
- ❌ Docker Compose environment syntax
- ❌ entrypoint.sh sanitization
- ❌ Explicit base_url in Docker SDK initialization

All of these were red herrings. The real issue was purely a library version compatibility problem.

## Verification

After the fix, the backend logs show:
```
docker_client_initialized_successfully base_url=unix:///var/run/docker.sock
```

And the health endpoint responds successfully:
```bash
$ curl http://localhost:48391/health
{"status":"healthy","version":"1.0.0","services":{"docker":"unknown"}}
```

## Long-term Solution

This is a temporary fix. The proper long-term solutions are:

1. **Wait for docker-py update**: The docker-py maintainers need to update `UnixHTTPAdapter` to override `get_connection_with_tls_context()`

2. **Track the issue**: Monitor https://github.com/docker/docker-py for updates

3. **Test before upgrading**: Before removing version constraints, test with newer library versions

## References

- docker-py GitHub: https://github.com/docker/docker-py
- requests GitHub: https://github.com/psf/requests
- Related change in requests: https://github.com/psf/requests/pull/6714

## Date

- **Discovered**: 2025-11-21
- **Fixed**: 2025-11-21
- **docker-py version**: 6.1.3
- **requests version**: 2.31.0 (downgraded from 2.32.5)
- **urllib3 version**: 1.26.20 (downgraded from 2.5.0)
