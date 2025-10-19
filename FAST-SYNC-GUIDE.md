# Fast Development Sync Guide

## 🚀 Optimized Development Workflow

Workflow baru ini memungkinkan development yang lebih cepat tanpa perlu restart container yang lama.

### 📋 Setup Requirements

1. Install watchdog untuk auto-sync (opsional):
```bash
pip install watchdog
```

### 🔄 Sync Options

#### 1. Manual Sync (Improved)
```bash
# Sync specific file (hot reload jika memungkinkan)
python docker/sync-code.py lms/lms/api.py

# Sync semua (akan restart)
python docker/sync-code.py

# Force sync
python docker/sync-code.py --force
```

#### 2. Auto Sync (Recommended)
```bash
# Start auto-sync watcher
python docker/watch-sync.py
```

### ⚡ Hot Reload Behavior

#### Files yang HOT RELOAD (tanpa restart):
- `.py` files (most Python code)
- `.js`, `.vue` files (handled by Vite HMR)
- `.css`, `.html` files
- Template files

#### Files yang PERLU RESTART:
- `hooks.py` (app configuration)
- `install.py`, `modules.txt` (app structure)
- `patches.txt` (database patches)
- `__init__.py` files (module initialization)
- `fixtures/` folder (data fixtures)
- `doctype/` folder (database schema)

### 🔐 Authentication Safety

✅ **Frappe auth tetap utuh:**
- Login/logout flow tidak berubah
- Session management tetap original
- CSRF fixes hanya untuk development
- Production auth tidak terpengaruh

### 🛠️ Development Commands

```bash
# Start containers
docker compose up -d

# Start auto-sync (terminal baru)
python docker/watch-sync.py

# Development server akan running di:
# - Frontend: http://localhost:8081
# - Backend: http://localhost:8080
```

### 🐛 Troubleshooting

#### Jika file tidak ter-sync:
```bash
# Manual sync specific file
python docker/sync-code.py path/to/file.py

# Force full sync
python docker/sync-code.py --force
```

#### Jika authentication bermasalah:
```bash
# Check container logs
docker logs lms-frappe-1

# Manual restart jika perlu
docker exec lms-frappe-1 bench restart
```

### ⚠️ Notes

- **Auto-sync membutuhkan `watchdog`** - install dengan `pip install watchdog`
- **Frontend auto-reload** via Vite HMR untuk `.vue`, `.js` files
- **Backend hot-reload** untuk most Python files
- **Restart otomatis** hanya untuk configuration files
- **Authentication flow** tetap menggunakan Frappe original

### 📊 Performance Improvement

| Method | Time | Description |
|--------|------|-------------|
| Old: `docker compose down && up` | ~2-3 minutes | Full restart |
| New: Hot reload | ~1-2 seconds | File-specific sync |
| New: Smart restart | ~10-15 seconds | Only when needed |

---

**💡 Tip:** Gunakan `watch-sync.py` untuk development daily, simpan `sync-code.py` untuk troubleshooting manual.