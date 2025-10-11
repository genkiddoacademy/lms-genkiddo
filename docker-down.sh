#!/bin/bash
# Script untuk menghentikan docker compose dari root directory
cd "$(dirname "$0")/docker" && docker compose down
