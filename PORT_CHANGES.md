# Port Configuration Changes - v1.0.2

## Overview

DockPilot has been updated to use non-standard, obscure port numbers for enhanced security. This reduces exposure to automated port scanning and common exploits targeting default application ports.

## Port Changes

| Service  | Old Port | New Port | Purpose |
|----------|----------|----------|---------|
| Frontend | 3000     | **38572** | Web UI |
| Backend  | 8000     | **48391** | API Server |

## Why Non-Standard Ports?

### Security Benefits

1. **Reduces Attack Surface**: Automated scanners typically target common ports (80, 443, 3000, 8000, 8080)
2. **Obscurity Layer**: Makes it harder for attackers to identify services
3. **Less Noise**: Fewer automated attacks and vulnerability scans
4. **Defense in Depth**: Additional security layer alongside authentication and firewalls

### Port Selection Criteria

The chosen ports (38572, 48391) were selected because:
- They are in the dynamic/private port range (49152-65535 or high registered range)
- They don't conflict with common services
- They are unlikely to be targeted by automated scans
- They are easy to remember (consecutive digits pattern)

## Access URLs

After upgrading to v1.0.2:

- **Frontend UI**: http://localhost:38572
- **Backend API**: http://localhost:48391
- **API Docs**: http://localhost:48391/docs

## Configuration Files Updated

All port references have been updated in:

### Application Files
- ✅ `docker-compose.yml` - Port mappings
- ✅ `frontend/src/lib/api.ts` - API client base URL
- ✅ `frontend/next.config.js` - Rewrite rules
- ✅ `backend/app/core/config.py` - CORS origins

### Environment Files
- ✅ `.env.example` - Root environment template
- ✅ `frontend/.env.example` - Frontend environment
- ✅ `backend/.env.example` - Backend environment

### Scripts & Tools
- ✅ `start.sh` - Startup script
- ✅ `stop.sh` - Stop script
- ✅ `Makefile` - All commands and health checks

### Documentation
- ✅ `README.md` - Main documentation
- ✅ `QUICKSTART.md` - Quick start guide
- ✅ `CONTRIBUTING.md` - Development guide
- ✅ `PROJECT_SUMMARY.md` - Technical summary
- ✅ `CHANGELOG.md` - Version history

## Migration Steps

If upgrading from v1.0.1 or earlier:

```bash
# 1. Stop current containers
docker compose down

# 2. Pull latest changes (or copy updated files)
git pull

# 3. Update your .env file (if it exists)
nano .env

# Change these lines:
# OLD:
NEXT_PUBLIC_API_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# NEW:
NEXT_PUBLIC_API_URL=http://localhost:48391
CORS_ORIGINS=http://localhost:38572,http://127.0.0.1:38572

# 4. Rebuild and start
docker compose up -d --build

# 5. Verify services are running
make health

# 6. Access DockPilot at the new URLs
# Frontend: http://localhost:38572
# Backend:  http://localhost:48391
```

## Reverting to Standard Ports

If you need to use standard ports for compatibility:

**Edit `docker-compose.yml`:**

```yaml
services:
  backend:
    ports:
      - "8000:8000"  # Change back from 48391:8000

  frontend:
    ports:
      - "3000:3000"  # Change back from 38572:3000
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Update `.env`:**

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Update `backend/app/core/config.py`:**

```python
CORS_ORIGINS: List[str] = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

Then rebuild:
```bash
docker compose down
docker compose up -d --build
```

## Firewall Configuration

If using a firewall, ensure the new ports are allowed:

### UFW (Ubuntu/Debian)
```bash
sudo ufw allow 38572/tcp  # Frontend
sudo ufw allow 48391/tcp  # Backend
```

### Firewalld (RHEL/CentOS/Fedora)
```bash
sudo firewall-cmd --permanent --add-port=38572/tcp
sudo firewall-cmd --permanent --add-port=48391/tcp
sudo firewall-cmd --reload
```

### iptables
```bash
sudo iptables -A INPUT -p tcp --dport 38572 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 48391 -j ACCEPT
sudo iptables-save > /etc/iptables/rules.v4
```

### macOS (pf)
```bash
# Edit /etc/pf.conf and add:
pass in proto tcp from any to any port 38572
pass in proto tcp from any to any port 48391

# Reload pf
sudo pfctl -f /etc/pf.conf
```

## Reverse Proxy Configuration

If using a reverse proxy (Nginx, Caddy, Traefik):

### Nginx Example
```nginx
server {
    listen 80;
    server_name dockpilot.example.com;

    location / {
        proxy_pass http://localhost:38572;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://localhost:48391;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Caddy Example
```caddy
dockpilot.example.com {
    reverse_proxy localhost:38572
    handle /api/* {
        reverse_proxy localhost:48391
    }
}
```

## Troubleshooting

### Port Already in Use

Check what's using the ports:
```bash
lsof -i :38572
lsof -i :48391
```

Kill process if needed:
```bash
kill -9 <PID>
```

### Can't Access Application

1. Verify containers are running:
```bash
docker compose ps
```

2. Check logs:
```bash
docker compose logs frontend
docker compose logs backend
```

3. Test ports:
```bash
curl http://localhost:48391/health
curl http://localhost:38572
```

### Browser Shows Old Port

Clear browser cache or use incognito mode.

## Additional Notes

- Internal container ports (3000, 8000) remain unchanged
- Only host-exposed ports have changed
- Docker network communication uses container names, not ports
- Health checks use internal container ports

## Questions?

For issues or questions about the port changes:
- Check the [CHANGELOG](CHANGELOG.md)
- Review [QUICKSTART](QUICKSTART.md) for updated access URLs
- Open an issue on GitHub

---

**Version**: 1.0.2
**Date**: November 20, 2024
**Impact**: Breaking change - requires configuration update
