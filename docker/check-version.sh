#!/bin/bash
# Check running version in dev or prod
# Usage: ./check-version.sh [dev|prod] [image_name]

ENV=${1:-dev}
IMAGE=${2:-lms-genkiddo:latest}
CONTAINER="lms-frappe-1"

if [[ "$ENV" == "dev" ]]; then
    echo "🔍 Development Version:"
    docker exec $CONTAINER cat /home/frappe/frappe-bench/apps/lms/.version 2>/dev/null || echo "No version file"
    echo ""
    echo "📝 Local Git:"
    git log -1 --oneline
    [[ -n "$(git status --short)" ]] && echo "⚠️  Uncommitted changes!" && git status --short
elif [[ "$ENV" == "prod" ]]; then
    echo "🔍 Production Image: $IMAGE"
    docker run --rm $IMAGE cat /home/frappe/frappe-bench/apps/lms/.version 2>/dev/null || echo "No version file"
    echo ""
    docker inspect $IMAGE --format='{{range $k,$v := .Config.Labels}}{{if or (eq $k "git.commit") (eq $k "version")}}{{$k}}: {{$v}}{{"\n"}}{{end}}{{end}}'
else
    echo "Usage: ./check-version.sh [dev|prod] [image_name]"
    exit 1
fi
