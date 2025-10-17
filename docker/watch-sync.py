#!/usr/bin/env python3
"""
Auto-sync file changes to Docker container with hot reload.
Preserves Frappe authentication while providing fast development workflow.
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LMSFileHandler(FileSystemEventHandler):
    def __init__(self, sync_script_path):
        self.sync_script_path = sync_script_path
        self.last_sync = {}
        self.debounce_delay = 1  # seconds
        
    def should_sync(self, file_path):
        """Check if file should be synced."""
        # Skip temporary files, cache, etc.
        skip_patterns = [
            '__pycache__',
            '.pyc',
            '.git/',
            'node_modules/',
            '.DS_Store',
            '.version',
            'package-lock.json'
        ]
        
        return not any(pattern in str(file_path) for pattern in skip_patterns)
    
    def debounce_sync(self, file_path):
        """Debounce rapid file changes."""
        now = time.time()
        if file_path in self.last_sync:
            if now - self.last_sync[file_path] < self.debounce_delay:
                return False
        self.last_sync[file_path] = now
        return True
    
    def sync_file(self, file_path):
        """Sync single file to container."""
        try:
            # Convert to relative path
            rel_path = os.path.relpath(file_path)
            print(f"📡 Auto-syncing: {rel_path}")
            
            # Run sync script for specific file
            subprocess.run([
                sys.executable, 
                self.sync_script_path, 
                rel_path
            ], check=True)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Sync failed for {file_path}: {e}")
        except Exception as e:
            print(f"⚠️  Error syncing {file_path}: {e}")
    
    def on_modified(self, event):
        if event.is_directory:
            return
            
        if not self.should_sync(event.src_path):
            return
            
        if not self.debounce_sync(event.src_path):
            return
            
        self.sync_file(event.src_path)
    
    def on_created(self, event):
        self.on_modified(event)

def main():
    # Get paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    sync_script = script_dir / "sync-code.py"
    
    if not sync_script.exists():
        print(f"❌ Sync script not found: {sync_script}")
        sys.exit(1)
    
    # Change to project root
    os.chdir(project_root)
    
    # Setup file watcher
    event_handler = LMSFileHandler(str(sync_script))
    observer = Observer()
    
    # Watch directories
    watch_dirs = ['lms', 'frontend']
    for watch_dir in watch_dirs:
        if os.path.exists(watch_dir):
            observer.schedule(event_handler, watch_dir, recursive=True)
            print(f"👀 Watching: {watch_dir}/")
        else:
            print(f"⚠️  Directory not found: {watch_dir}/")
    
    # Start watching
    observer.start()
    print("🚀 Auto-sync started! Press Ctrl+C to stop...")
    print("💡 Tip: Frappe auth is preserved, only files are hot-reloaded")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping auto-sync...")
        observer.stop()
    
    observer.join()
    print("✅ Auto-sync stopped")

if __name__ == "__main__":
    main()