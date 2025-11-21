# DockPilot Quick Start Guide

Get DockPilot up and running in under 5 minutes!

## Prerequisites

Ensure you have these installed:
- ✅ Docker Engine (24.x or later)
- ✅ Docker Compose v2

Check your versions:
```bash
docker --version
docker compose version
```

## Installation

### Option 1: Quick Start (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/DockPilot.git
cd DockPilot

# Run the start script
./start.sh
```

That's it! The script will:
- Check Docker is running
- Create `.env` from template
- Build and start all services
- Wait for health checks
- Show you the URLs to access

### Option 2: Using Make

```bash
# Clone the repository
git clone https://github.com/yourusername/DockPilot.git
cd DockPilot

# Setup and start
make setup
make start
```

### Option 3: Manual Start

```bash
# Clone the repository
git clone https://github.com/yourusername/DockPilot.git
cd DockPilot

# Create environment file
cp .env.example .env

# Build and start
docker-compose up -d --build

# Check status
docker-compose ps
```

## Access DockPilot

Once started, access:
- **Frontend**: http://localhost:38572
- **Backend API**: http://localhost:48391
- **API Docs**: http://localhost:48391/docs

## First Steps

1. **Open DockPilot** at http://localhost:38572

2. **Discover Apps**
   - Click the "Discover Apps" button in the header
   - DockPilot will scan default directories for Docker Compose apps
   - Default search paths:
     - `~/docker`
     - `~/Docker`
     - `/opt/apps`

3. **Manage Apps**
   - View all discovered apps in the dashboard
   - Start, stop, restart, or rebuild any app with one click
   - Monitor resource usage in real-time

## Configuration

### Custom Search Paths

Edit `.env` to add your own directories:

```bash
SEARCH_PATHS=${HOME}/docker,${HOME}/projects,/opt/myapps
```

Then restart:
```bash
docker-compose restart backend
```

### Environment Variables

Key settings in `.env`:

```bash
# API URLs
NEXT_PUBLIC_API_URL=http://localhost:48391
BACKEND_URL=http://backend:8000

# Docker socket
DOCKER_HOST=unix:///var/run/docker.sock

# Search paths (comma-separated)
SEARCH_PATHS=${HOME}/docker,${HOME}/Docker,/opt/apps
```

## Common Commands

```bash
# View logs
make logs                    # All services
make logs-backend           # Backend only
make logs-frontend          # Frontend only
docker-compose logs -f      # Alternative

# Stop DockPilot
make stop
# or
./stop.sh
# or
docker-compose down

# Restart
make restart

# Check status
make ps
docker-compose ps

# Check health
make health
```

## Troubleshooting

### Docker not running
```bash
# Start Docker Desktop or Docker daemon
# macOS: Open Docker Desktop
# Linux: sudo systemctl start docker
```

### Permission denied (Docker socket)
```bash
# Add your user to docker group (Linux)
sudo usermod -aG docker $USER
# Then log out and back in
```

### Backend can't connect to Docker
```bash
# Check Docker socket permissions
ls -la /var/run/docker.sock

# Verify Docker is accessible
docker ps
```

### Port already in use
```bash
# Check what's using the configured ports
lsof -i :38572  # Frontend
lsof -i :48391  # Backend

# Change ports in docker-compose.yml if needed
```

### Apps not discovered
1. Check search paths in `.env`
2. Ensure compose files exist and are named correctly:
   - `docker-compose.yml`
   - `docker-compose.yaml`
   - `compose.yml`
   - `compose.yaml`
3. Check backend logs: `make logs-backend`

## Development Mode

For development with hot reload:

```bash
# Terminal 1: Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 48391

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

## Next Steps

- [Read the full README](README.md)
- [Check the API documentation](http://localhost:48391/docs)
- [Contribute to DockPilot](CONTRIBUTING.md)
- [Report issues](https://github.com/yourusername/DockPilot/issues)

## Useful Make Commands

```bash
make help          # Show all available commands
make setup         # Initial setup
make start         # Start DockPilot
make stop          # Stop DockPilot
make restart       # Restart services
make logs          # View logs
make clean         # Remove everything
make discover      # Trigger app discovery
make docker-info   # Get Docker information
make system-info   # Get system information
```

## Getting Help

- Check [Troubleshooting](#troubleshooting) section
- View logs: `make logs`
- Read the [README](README.md)
- Open an [issue](https://github.com/yourusername/DockPilot/issues)

---

**Happy Docker management! 🐳**
