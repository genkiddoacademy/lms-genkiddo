#!/bin/bash

# Build and Run Frappe LMS Docker Container
# Usage: ./build-and-run.sh

set -e

echo "🐳 Building Frappe LMS Docker Image..."

# Build the Docker image
docker build -t lms-genkiddo:latest .

echo "✅ Build completed successfully!"

echo "🚀 Starting services with docker-compose..."

# Start services using docker-compose
docker-compose -f docker-compose.standalone.yml up -d

echo "✅ Services started successfully!"
echo ""
echo "📋 Service Information:"
echo "  - LMS Application: http://localhost:8000"
echo "  - LMS Socket.IO: http://localhost:9000"
echo "  - MariaDB: localhost:3306"
echo "  - Redis: localhost:6379"
echo ""
echo "🔑 Default Credentials:"
echo "  - Username: Administrator"
echo "  - Password: admin"
echo ""
echo "📜 Useful Commands:"
echo "  - View logs: docker-compose -f docker-compose.standalone.yml logs -f lms-app"
echo "  - Stop services: docker-compose -f docker-compose.standalone.yml down"
echo "  - Rebuild: docker-compose -f docker-compose.standalone.yml up --build"
echo ""
echo "⏳ Please wait 2-3 minutes for the application to initialize completely..."
