#!/bin/bash
# Build production image from current git state
# Usage: ./build-prod.sh [version_tag]

set -e
cd "$(dirname "$0")/.."

VERSION=${1:-$(git describe --tags --always)}
BRANCH=$(git rev-parse --abbrev-ref HEAD)
COMMIT=$(git rev-parse HEAD)

echo "🏗️  Building Production Image"
echo "📌 Version: $VERSION | Branch: $BRANCH | Commit: ${COMMIT:0:7}"

# Check uncommitted changes
if [[ -n "$(git status --short)" ]]; then
    echo "⚠️  WARNING: Uncommitted changes!"
    git status --short | head -5
    read -p "Build anyway? (y/N) " -n 1 -r; echo
    [[ ! $REPLY =~ ^[Yy]$ ]] && exit 1
fi

# Build
docker build \
    -f docker/Dockerfile.prod \
    --build-arg GIT_BRANCH=$BRANCH \
    --build-arg GIT_COMMIT=$COMMIT \
    --label "git.commit=$COMMIT" \
    --label "version=$VERSION" \
    -t lms-genkiddo:$VERSION \
    -t lms-genkiddo:latest \
    .

echo ""
echo "✅ Build Complete!"
echo "📦 Image: lms-genkiddo:$VERSION"
echo "📌 Commit: ${COMMIT:0:7}"
echo ""
echo "Next steps:"
echo "  Test:   docker compose -f docker/docker-compose.prod.yml up"
echo "  Check:  ./check-version.sh prod lms-genkiddo:$VERSION"
echo "  Deploy: docker push your-registry/lms-genkiddo:$VERSION"
