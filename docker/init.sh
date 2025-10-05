#!/bin/bash

cd /home/frappe

# Initialize bench if not exists
if [ ! -d "frappe-bench/apps/frappe" ]; then
    echo "Initializing bench..."
    export PATH="${NVM_DIR}/versions/node/v${NODE_VERSION_DEVELOP}/bin/:${PATH}"
    bench init --skip-redis-config-generation frappe-bench
fi

cd frappe-bench

# Configure redis and mariadb
bench set-mariadb-host mariadb
bench set-redis-cache-host redis://redis:6379
bench set-redis-queue-host redis://redis:6379
bench set-redis-socketio-host redis://redis:6379

# Remove redis, watch from Procfile
sed -i '/redis/d' ./Procfile
sed -i '/watch/d' ./Procfile

# Get LMS app if not already present
if [ ! -d "apps/lms" ]; then
    echo "Getting LMS app..."
    bench get-app lms
fi

# Create site if it doesn't exist (sites directory is mounted from volume)
if [ ! -d "sites/lms.localhost" ]; then
    echo "Creating new site lms.localhost..."
    bench new-site lms.localhost \
    --force \
    --mariadb-root-password 123 \
    --admin-password admin \
    --no-mariadb-socket

    bench --site lms.localhost install-app lms
    bench --site lms.localhost set-config developer_mode 1
else
    echo "✓ Site lms.localhost already exists"
fi

bench --site lms.localhost clear-cache
bench use lms.localhost

echo "Starting bench..."
bench start
