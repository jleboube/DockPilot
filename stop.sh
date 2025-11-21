#!/bin/bash

# DockPilot Stop Script

echo "🛑 Stopping DockPilot..."
docker compose down

echo "✅ DockPilot stopped"
echo ""
echo "To remove volumes as well, run: docker compose down -v"
