#!/bin/bash
# Dev sync script - Auto-sync code to container with git tracking
# Usage: ./sync-code.sh [file_path] [--force]

set -e
cd "$(dirname "$0")/.."

CONTAINER_NAME="lms-frappe-1"
APP_PATH="/home/frappe/frappe-bench/apps/lms"
FORCE=false

# Parse args
for arg in "$@"; do
    [[ "$arg" == "--force" ]] && FORCE=true
done

# Check container
if ! docker ps -q -f name=$CONTAINER_NAME | grep -q .; then
    echo "❌ Container not running. Start with: docker compose up -d"
    exit 1
fi

# Git tracking
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
GIT_COMMIT=$(git rev-parse --short HEAD)
GIT_STATUS=$(git status --short)

# Warn uncommitted changes
if [[ -n "$GIT_STATUS" ]] && [[ "$FORCE" == false ]]; then
    echo "⚠️  Uncommitted changes detected:"
    echo "$GIT_STATUS" | head -5
    read -p "Continue? (y/N) " -n 1 -r; echo
    [[ ! $REPLY =~ ^[Yy]$ ]] && exit 1
fi

echo "📦 Syncing: $GIT_BRANCH@$GIT_COMMIT"

# Sync files
if [[ -n "$1" ]] && [[ "$1" != "--force" ]]; then
    docker cp "$1" "$CONTAINER_NAME:$APP_PATH/$1"
else
    docker cp lms/ "$CONTAINER_NAME:$APP_PATH/"
    docker cp frontend/ "$CONTAINER_NAME:$APP_PATH/"
fi

# Write version
docker exec $CONTAINER_NAME bash -c "cat > $APP_PATH/.version << EOF
BRANCH=$GIT_BRANCH
COMMIT=$GIT_COMMIT
TIME=$(date -u +%Y-%m-%dT%H:%M:%SZ)
EOF"

echo "✅ Synced: $GIT_BRANCH@$GIT_COMMIT"
docker exec $CONTAINER_NAME bench restart >/dev/null 2>&1 || echo "⚠️  Manual restart may be needed"
