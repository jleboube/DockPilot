# DockPilot

**A native macOS and Linux application for managing Docker Compose applications**

DockPilot provides a management and orchestration layer between your host OS and Docker Compose-based applications. It offers a clean GUI that eliminates CLI complexity while enabling automation, operational workflows, and safe management of OS-level resources.

![DockPilot Dashboard](https://via.placeholder.com/800x400?text=DockPilot+Dashboard)

## 🎯 Features

### MVP (v1.0)
- ✅ **App Discovery**: Automatically scan directories for Docker Compose applications
- ✅ **Unified Dashboard**: Single pane of glass for all your Compose apps
- ✅ **Lifecycle Management**: Start, stop, restart, and rebuild apps with a click
- ✅ **Resource Monitoring**: Real-time CPU, memory, and network usage
- ✅ **System Stats**: Monitor host system resources
- ✅ **Service Status**: View individual container states and health
- ✅ **Modern UI**: Dark mode with responsive design

### Coming Soon (v1.1)
- 🔄 Systemd/Launchd integration for auto-start
- 📝 Compose file editor with validation
- 🔐 Environment variable management with secret masking
- 📊 Enhanced resource monitoring with history
- 🔄 Image update management with rollback
- 📋 Real-time log streaming

## 🏗️ Architecture

```
┌─────────────────────────────────┐
│      Frontend (Next.js 14)      │
│  TypeScript + Tailwind CSS      │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   Backend API (FastAPI)         │
│  Python + Docker SDK            │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Docker Engine + Compose        │
└─────────────────────────────────┘
```

## 📋 Prerequisites

- **Docker Engine** >= 24.x
- **Docker Compose** v2
- **Node.js** >= 20.x (for development)
- **Python** >= 3.11 (for development)
- **macOS** Monterey+ or **Linux** (Ubuntu 22.04+, Debian, Fedora, Arch)

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/DockPilot.git
cd DockPilot
```

2. **Create environment file**
```bash
cp .env.example .env
# Edit .env if needed to customize search paths
```

3. **Build and run**
```bash
docker-compose up -d
```

4. **Access the application**
- Frontend: http://localhost:38572
- Backend API: http://localhost:48391
- API Docs: http://localhost:48391/docs

### Development Setup

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 48391
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## 📁 Project Structure

```
DockPilot/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   │   └── routes/     # Route modules
│   │   ├── core/           # Configuration
│   │   ├── models/         # Pydantic models
│   │   └── services/       # Business logic
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # Next.js app router
│   │   ├── components/    # React components
│   │   ├── lib/           # Utilities and API client
│   │   └── types/         # TypeScript types
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml      # Docker Compose configuration
├── .env.example           # Environment variables template
└── README.md
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:48391
BACKEND_URL=http://backend:8000

# Docker Configuration
DOCKER_HOST=unix:///var/run/docker.sock

# Search Paths (comma-separated)
SEARCH_PATHS=${HOME}/docker,${HOME}/Docker,/opt/apps

# Resource Monitoring
RESOURCE_POLL_INTERVAL=2

# Log Settings
LOG_RETENTION_DAYS=7
MAX_LOG_LINES=1000
```

### Custom Search Paths

Edit your `.env` file to add custom directories where DockPilot should look for Docker Compose apps:

```bash
SEARCH_PATHS=/path/to/your/apps,/another/path,${HOME}/docker
```

These paths will be automatically mounted in the backend container.

## 🎮 Usage

### Discovering Applications

1. Click **"Discover Apps"** in the header
2. DockPilot will scan configured directories for `docker-compose.yml` files
3. Found applications will appear in the dashboard

### Managing Applications

Each application card provides:
- **Start**: Launch all services
- **Stop**: Shutdown all services
- **Restart**: Restart all services
- **Rebuild**: Rebuild images and restart

### Monitoring

The dashboard shows:
- System resource usage (CPU, Memory, Disk)
- Per-app resource consumption
- Service states and health
- Container counts

## 🔒 Security

- **Local-only**: No cloud dependencies or external connections
- **Read-only Docker socket**: Backend mounts Docker socket in read-only mode
- **Non-root containers**: Both frontend and backend run as non-root users
- **Health checks**: Built-in health monitoring for all services

## 📊 API Documentation

Once running, visit http://localhost:48391/docs for interactive API documentation (Swagger UI).

### Key Endpoints

- `GET /api/apps/` - List all discovered apps
- `POST /api/apps/discover` - Discover/refresh apps
- `POST /api/apps/{app_id}/action` - Perform action (start/stop/restart/rebuild)
- `GET /api/apps/{app_id}/stats` - Get resource statistics
- `GET /api/system/info` - Get system information
- `GET /api/docker/info` - Get Docker engine information

## 🐛 Troubleshooting

### Backend can't connect to Docker

**Error**: "Docker engine is not available"

**Solution**:
```bash
# Check Docker is running
docker ps

# Verify Docker socket exists
ls -la /var/run/docker.sock

# Ensure user has Docker permissions
sudo usermod -aG docker $USER
# Then log out and back in
```

### Frontend can't connect to backend

**Error**: "Network error" or "Failed to fetch"

**Solution**:
1. Check backend is running: `curl http://localhost:48391/health`
2. Verify `NEXT_PUBLIC_API_URL` in `.env`
3. Check CORS settings in `backend/app/core/config.py`

### Apps not being discovered

**Solution**:
1. Verify search paths in `.env`
2. Ensure compose files are named correctly (`docker-compose.yml`, `compose.yml`, etc.)
3. Check backend logs: `docker-compose logs backend`

## 🛣️ Roadmap

### v1.1 (Next Release)
- [ ] Systemd/Launchd integration for auto-start on boot
- [ ] Compose file editor with syntax validation
- [ ] Environment variable editor with secret masking
- [ ] Image update notifications and management
- [ ] Enhanced logging with real-time streaming
- [ ] Port conflict detection and resolution

### v2.0 (Future)
- [ ] Remote Docker host management via SSH
- [ ] GitOps-style sync
- [ ] Application templates
- [ ] Backup and restore
- [ ] Plugin system
- [ ] CLI companion tool

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Next.js](https://nextjs.org/), [FastAPI](https://fastapi.tiangolo.com/), and [Docker SDK for Python](https://docker-py.readthedocs.io/)
- Icons by [Lucide](https://lucide.dev/)
- Inspired by Docker Desktop, Portainer, and the need for better Compose management

## 📧 Contact

**Author**: Joe LeBoube
**Project Link**: https://github.com/yourusername/DockPilot

---

Built with ❤️ using Claude Code
