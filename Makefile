.PHONY: help start stop restart build logs clean dev-backend dev-frontend test

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

start: ## Start DockPilot (build and run)
	@./start.sh

stop: ## Stop DockPilot
	@docker compose down

restart: ## Restart DockPilot
	@docker compose restart

build: ## Build Docker images
	@docker compose build

logs: ## View logs (follow mode)
	@docker compose logs -f

logs-backend: ## View backend logs
	@docker compose logs -f backend

logs-frontend: ## View frontend logs
	@docker compose logs -f frontend

clean: ## Stop and remove containers, volumes, and images
	@docker compose down -v --rmi all
	@echo "Cleaned up DockPilot containers, volumes, and images"

dev-backend: ## Run backend in development mode
	@cd backend && \
	source venv/bin/activate && \
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Run frontend in development mode
	@cd frontend && npm run dev

dev: ## Run both backend and frontend in development mode
	@echo "Run 'make dev-backend' in one terminal and 'make dev-frontend' in another"

test-backend: ## Run backend tests
	@cd backend && \
	source venv/bin/activate && \
	pytest tests/ -v

test-frontend: ## Run frontend tests
	@cd frontend && npm test

ps: ## Show running containers
	@docker compose ps

health: ## Check health of services
	@echo "Backend health:"
	@curl -s http://localhost:8000/health | python -m json.tool || echo "Backend not responding"
	@echo ""
	@echo "Frontend health:"
	@curl -s http://localhost:3000 > /dev/null && echo "Frontend is up" || echo "Frontend not responding"

setup: ## Initial setup (create .env, install dependencies)
	@echo "Setting up DockPilot..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env file"; fi
	@if [ ! -f backend/.env ]; then cp backend/.env.example backend/.env; echo "Created backend/.env file"; fi
	@if [ ! -f frontend/.env.local ]; then cp frontend/.env.example frontend/.env.local; echo "Created frontend/.env.local file"; fi
	@echo "Setup complete! Run 'make start' to launch DockPilot"

install-backend: ## Install backend dependencies
	@cd backend && \
	python -m venv venv && \
	source venv/bin/activate && \
	pip install -r requirements.txt

install-frontend: ## Install frontend dependencies
	@cd frontend && npm install

install: install-backend install-frontend ## Install all dependencies

discover: ## Trigger app discovery
	@curl -X POST http://localhost:8000/api/apps/discover | python -m json.tool

docker-info: ## Get Docker info
	@curl -s http://localhost:8000/api/docker/info | python -m json.tool

system-info: ## Get system info
	@curl -s http://localhost:8000/api/system/info | python -m json.tool
