.PHONY: help start stop restart logs shell sync dev bench clean status

help: ## Show this help
	@echo "🚀 LMS Development Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

start: ## Start all services
	@echo "🚀 Starting LMS..."
	cd docker && docker compose up -d
	@echo "✅ Services started!"
	@echo "⏳ Wait 5-10 mins for first init, then run: make sync"
	@echo "📍 Backend: http://localhost:8000"
	@echo "📍 Frontend: http://localhost:9000 (after 'make dev')"

stop: ## Stop all services
	@echo "🛑 Stopping services..."
	cd docker && docker compose down

restart: stop start ## Restart services

logs: ## Show live logs
	@echo "📄 Showing logs (Ctrl+C to exit)..."
	docker logs -f lms-frappe-1

shell: ## Open bash shell in container
	@echo "🐚 Opening shell..."
	docker exec -it lms-frappe-1 bash

sync: ## Sync code changes to container
	@echo "🔄 Syncing code..."
	python3 docker/sync-code.py
	@echo "✅ Code synced!"

dev: ## Start frontend dev server (with HMR)
	@echo "🎨 Starting frontend dev server..."
	@echo "💡 Frontend will be available at http://localhost:8080"
	yarn dev

bench: ## Run bench command (usage: make bench CMD="migrate")
	@if [ -z "$(CMD)" ]; then \
		echo "❌ Usage: make bench CMD=\"your-command\""; \
		exit 1; \
	fi
	docker exec -it lms-frappe-1 bash -c "cd /home/frappe/frappe-bench && bench $(CMD)"

clean: ## Stop and remove everything (including data)
	@echo "⚠️  WARNING: This will delete all data!"
	echo "🗑️  Removing everything..."; \
	cd docker && docker compose down -v; \
	echo "✅ Cleaned!"; \

status: ## Show container status
	@echo "📊 Container Status:"
	@cd docker && docker compose ps

watch-restart: ## Watch and auto-restart if container dies
	@echo "👀 Watching container... (Ctrl+C to stop)"
	@while true; do \
		if ! docker ps | grep -q lms-frappe-1; then \
			echo "⚠️  Container died! Restarting..."; \
			cd docker && docker compose up -d frappe; \
			sleep 5; \
		fi; \
		sleep 2; \
	done

# Quick shortcuts
s: sync ## Shortcut for sync
d: dev  ## Shortcut for dev
l: logs ## Shortcut for logs