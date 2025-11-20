#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "Usage: bash restore.sh <backup_folder>"
  exit 1
fi

BACKUP_DIR="$1"
SITE_NAME="lms.genkiddo.id"
DB_ROOT_PASSWORD="123"
DB_CONTAINER="lms-mariadb-1"

echo "=== RESTORE PROCESS ==="

if [ ! -f "$BACKUP_DIR/db.sql" ]; then
    echo "db.sql not found!"
    exit 1
fi

echo "[1/7] Stopping all containers..."
docker compose -f docker/docker-compose.yml down -v

echo "[2/7] Starting DB & Redis..."
docker compose -f docker/docker-compose.yml up -d mariadb redis
sleep 12

# Generate new DB name from timestamp
TIMESTAMP=$(basename "$BACKUP_DIR")
DB_NAME="_${TIMESTAMP//[!0-9]/}"
DB_PASSWORD=$(openssl rand -hex 12)

echo "[3/7] Using DB_NAME=$DB_NAME"
echo "Generated DB_PASSWORD=$DB_PASSWORD"

# Create empty database manually
docker exec $DB_CONTAINER sh -c "
mysql -u root -p$DB_ROOT_PASSWORD -e \"
DROP DATABASE IF EXISTS $DB_NAME;
CREATE DATABASE $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
\"
"

echo "[4/7] Starting frappe container..."
docker compose -f docker/docker-compose.yml up -d frappe
sleep 12

echo "[5/7] Creating fresh site folder..."
docker compose -f docker/docker-compose.yml exec frappe bash -c "
cd frappe-bench/sites
rm -rf $SITE_NAME
mkdir -p $SITE_NAME
"

echo "[6/7] Restoring site_config.json..."
cat > site_config_temp.json <<EOF
{
  "db_name": "$DB_NAME",
  "db_password": "$DB_PASSWORD",
  "db_type": "mariadb",
  "db_host": "mariadb",
  "developer_mode": 1,
  "ignore_csrf": 1
}
EOF

docker cp site_config_temp.json lms-frappe-1:/home/frappe/frappe-bench/sites/$SITE_NAME/site_config.json
rm site_config_temp.json

echo "[7/7] Restoring files & database..."
docker cp "$BACKUP_DIR/site/public" lms-frappe-1:/home/frappe/frappe-bench/sites/$SITE_NAME/
docker cp "$BACKUP_DIR/site/private" lms-frappe-1:/home/frappe/frappe-bench/sites/$SITE_NAME/

docker cp "$BACKUP_DIR/db.sql" $DB_CONTAINER:/db.sql
docker exec $DB_CONTAINER sh -c "
mysql -u root -p$DB_ROOT_PASSWORD $DB_NAME < /db.sql
"

echo "[DONE] Running migrations..."
docker compose -f docker/docker-compose.yml exec frappe bash -c "
cd frappe-bench
bench --site $SITE_NAME migrate
bench clear-cache
bench build
"

echo "=== RESTORE COMPLETED SUCCESSFULLY ==="
