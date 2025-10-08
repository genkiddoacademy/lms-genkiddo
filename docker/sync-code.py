#!/usr/bin/env python3
"""
Dev sync script - Auto-sync code to container with git tracking
Usage: python sync-code.py [file_path] [--force]
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime

def run_command(cmd, capture_output=False):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=capture_output, text=True)
        return result.stdout.strip() if capture_output else None
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {cmd}")
        print(f"Error: {e}")
        sys.exit(1)

def check_container_running(container_name):
    """Check if the container is running."""
    result = run_command(f"docker ps -q -f name={container_name}", capture_output=True)
    return bool(result.strip())

def get_git_info():
    """Get git branch, commit, and status."""
    branch = run_command("git rev-parse --abbrev-ref HEAD", capture_output=True)
    commit = run_command("git rev-parse --short HEAD", capture_output=True)
    status = run_command("git status --short", capture_output=True)
    return branch, commit, status

def sync_files(container_name, app_path, file_path=None):
    """Sync files to the container."""
    if file_path and file_path != "--force":
        # Sync specific file
        if os.path.exists(file_path):
            run_command(f"docker cp {file_path} {container_name}:{app_path}/{file_path}")
            print(f"📄 Synced file: {file_path}")
        else:
            print(f"❌ File not found: {file_path}")
            sys.exit(1)
    else:
        # Sync entire directories
        for directory in ["lms", "frontend"]:
            if os.path.exists(directory):
                run_command(f"docker cp {directory}/ {container_name}:{app_path}/")
                print(f"📁 Synced directory: {directory}/")
            else:
                print(f"⚠️  Directory not found: {directory}/")

def write_version_file(container_name, app_path, branch, commit):
    """Write version information to the container."""
    version_content = f"""BRANCH={branch}
COMMIT={commit}
TIME={datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}
"""
    # Create a temporary file
    with open('.version', 'w') as f:
        f.write(version_content)

    run_command(f"docker cp .version {container_name}:{app_path}/.version")
    os.remove('.version')

def main():
    # Configuration
    CONTAINER_NAME = "lms-frappe-1"
    APP_PATH = "/home/frappe/frappe-bench/apps/lms"
    FORCE = False

    # Change to project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, "..")
    os.chdir(project_root)

    # Parse arguments
    file_path = None
    for arg in sys.argv[1:]:
        if arg == "--force":
            FORCE = True
        else:
            file_path = arg

    # Check container
    if not check_container_running(CONTAINER_NAME):
        print("❌ Container not running. Start with: docker compose up -d")
        sys.exit(1)

    # Get git info
    branch, commit, status = get_git_info()

    # Warn about uncommitted changes
    if status and not FORCE:
        print("⚠️  Uncommitted changes detected:")
        print("\n".join(status.split("\n")[:5]))
        response = input("Continue? (y/N) ").strip().lower()
        if response not in ['y', 'yes']:
            sys.exit(1)

    print(f"📦 Syncing: {branch}@{commit}")

    # Sync files
    sync_files(CONTAINER_NAME, APP_PATH, file_path)

    # Write version
    write_version_file(CONTAINER_NAME, APP_PATH, branch, commit)

    print(f"✅ Synced: {branch}@{commit}")

    # Restart bench
    try:
        run_command(f"docker exec {CONTAINER_NAME} bench restart", capture_output=True)
    except:
        print("⚠️  Manual restart may be needed")

if __name__ == "__main__":
    main()