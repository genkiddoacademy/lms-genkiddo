#!/bin/bash

echo "=== Starting Frappe LMS Backup ==="

SITE="lms.genkiddo.id"
DB_NAME="_19515679fbb86e2b"
DB_USER="_19515679fbb86e2b"
DB_PASSWORD="yxFLPE9qJxktDNdo"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="./backups/${TIMESTAMP}"
mkdir -p "$BACKUP_DIR"

echo "[1/3] Backing up database..."
docker exec lms-mariadb-1 sh -c \
"mysqldump -u${DB_USER} -p${DB_PASSWORD} ${DB_NAME}" \
> "${BACKUP_DIR}/db.sql"

echo "[2/3] Backing up site files..."
CONTAINER_ID=$(docker ps -q -f name=lms-frappe-1)
docker cp "${CONTAINER_ID}:/home/frappe/frappe-bench/sites/${SITE}" "${BACKUP_DIR}/site"

echo "[3/3] Backup completed successfully."
echo "Backup saved to: ${BACKUP_DIR}"
