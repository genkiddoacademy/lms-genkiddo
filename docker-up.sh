#!/bin/bash
# Script untuk menjalankan docker compose dari root directory
cd "$(dirname "$0")/docker" && docker compose up -d
