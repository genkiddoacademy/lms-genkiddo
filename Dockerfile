# Multi-stage Dockerfile for Frappe LMS
FROM node:18-bullseye as frontend-builder

# Set working directory
WORKDIR /app

# Copy frontend source
COPY frontend/ ./frontend/
COPY package.json yarn.lock ./

# Install dependencies and build frontend
RUN yarn install --frozen-lockfile
RUN cd frontend && yarn install --check-files
RUN cd frontend && yarn build

# Main application stage
FROM frappe/bench:latest

# Install system dependencies
USER root
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    libffi-dev \
    libjpeg-dev \
    libpng-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Switch back to frappe user
USER frappe
WORKDIR /home/frappe

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FRAPPE_USER=frappe
ENV BENCH_PATH=/home/frappe/frappe-bench

# Copy application source
COPY --chown=frappe:frappe . /home/frappe/lms-source/
COPY --from=frontend-builder --chown=frappe:frappe /app/lms/public/frontend/ /home/frappe/lms-source/lms/public/frontend/
COPY --from=frontend-builder --chown=frappe:frappe /app/lms/www/lms.html /home/frappe/lms-source/lms/www/lms.html

# Create bench and install LMS
RUN mkdir -p /home/frappe/frappe-bench

# Initialize bench if it doesn't exist
RUN if [ ! -d "/home/frappe/frappe-bench/apps/frappe" ]; then \
        export PATH="${NVM_DIR}/versions/node/v${NODE_VERSION_DEVELOP}/bin/:${PATH}" && \
        bench init --skip-redis-config-generation frappe-bench && \
        cd frappe-bench && \
        bench set-mariadb-host mariadb && \
        bench set-redis-cache-host redis://redis:6379 && \
        bench set-redis-queue-host redis://redis:6379 && \
        bench set-redis-socketio-host redis://redis:6379 && \
        sed -i '/redis/d' ./Procfile && \
        sed -i '/watch/d' ./Procfile; \
    fi

WORKDIR /home/frappe/frappe-bench

# Create symbolic link to LMS source
RUN ln -sf /home/frappe/lms-source ./apps/lms

# Create startup script
COPY --chown=frappe:frappe <<EOF /home/frappe/start.sh
#!/bin/bash
set -e

cd /home/frappe/frappe-bench

# Wait for database to be ready
echo "Waiting for MariaDB to be ready..."
while ! nc -z mariadb 3306; do
    sleep 1
done

# Install LMS if site doesn't exist
if [ ! -d "./sites/lms.localhost" ]; then
    echo "Creating new site..."
    bench new-site lms.localhost \
        --force \
        --mariadb-root-password 123 \
        --admin-password admin \
        --no-mariadb-socket

    bench --site lms.localhost install-app lms
    bench build
    bench --site lms.localhost set-config developer_mode 1
    bench --site lms.localhost clear-cache
    bench use lms.localhost
fi

# Start the application
exec bench start
EOF

RUN chmod +x /home/frappe/start.sh

# Expose ports
EXPOSE 8000 9000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000 || exit 1

# Start the application
CMD ["/home/frappe/start.sh"]
