#!/bin/bash

# Script to sync course statistics for existing data
# This should be run ONCE after the hooks are added

echo "=================================================="
echo "  LMS Course Statistics Sync Script"
echo "=================================================="
echo ""
echo "This will update enrollments and ratings for all courses"
echo ""

# Check if we're in docker or local setup
if [ -f "docker/docker-compose.yml" ]; then
    echo "🐳 Detected Docker setup"
    echo ""
    read -p "Enter your site name (e.g., lms-genkiddo): " SITE_NAME

    if [ -z "$SITE_NAME" ]; then
        echo "❌ Site name is required!"
        exit 1
    fi

    echo ""
    echo "Running sync in Docker container..."
    cd docker
    docker compose exec frappe bench --site "$SITE_NAME" execute lms.lms.doctype.lms_enrollment.lms_enrollment.sync_all_courses
else
    echo "💻 Detected Local setup"
    echo ""
    read -p "Enter your site name (e.g., lms-genkiddo): " SITE_NAME

    if [ -z "$SITE_NAME" ]; then
        echo "❌ Site name is required!"
        exit 1
    fi

    echo ""
    echo "Running sync..."
    bench --site "$SITE_NAME" execute lms.lms.doctype.lms_enrollment.lms_enrollment.sync_all_courses
fi

echo ""
echo "=================================================="
echo "  Sync Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Check the output above for any errors"
echo "2. Refresh your browser to see updated statistics"
echo "3. Try enrolling in a new course - it should update instantly now!"
echo ""
