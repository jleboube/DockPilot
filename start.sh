#!/bin/bash

# DockPilot Quick Start Script

set -e

echo "🚀 Starting DockPilot..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running"
    echo "Please start Docker and try again"
    exit 1
fi

echo "✅ Docker is running"

# Check if .env exists, if not copy from example
if [ ! -f .env ]; then
    echo "📝 Creating .env file from example..."
    cp .env.example .env
    echo "✅ .env file created"
    echo "   You may want to edit it to customize search paths"
fi

echo ""
echo "🏗️  Building and starting DockPilot..."
echo ""

# Build and start services
docker compose up -d --build

echo ""
echo "⏳ Waiting for services to be healthy..."

# Wait for backend to be healthy
timeout=60
elapsed=0
while [ $elapsed -lt $timeout ]; do
    if docker compose ps | grep -q "dockpilot-backend.*healthy"; then
        echo "✅ Backend is healthy"
        break
    fi
    sleep 2
    elapsed=$((elapsed + 2))
done

if [ $elapsed -ge $timeout ]; then
    echo "⚠️  Backend health check timed out"
fi

# Wait for frontend to be healthy
elapsed=0
while [ $elapsed -lt $timeout ]; do
    if docker compose ps | grep -q "dockpilot-frontend.*healthy"; then
        echo "✅ Frontend is healthy"
        break
    fi
    sleep 2
    elapsed=$((elapsed + 2))
done

if [ $elapsed -ge $timeout ]; then
    echo "⚠️  Frontend health check timed out"
fi

echo ""
echo "✨ DockPilot is running!"
echo ""
echo "📍 Access DockPilot at:"
echo "   Frontend: http://localhost:38572"
echo "   Backend API: http://localhost:48391"
echo "   API Docs: http://localhost:48391/docs"
echo ""
echo "📊 View logs with: docker compose logs -f"
echo "🛑 Stop with: docker compose down"
echo ""
