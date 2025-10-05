# 🐳 Docker Setup - Dev & Production

## Quick Start

### Development

```bash
# Start containers
cd docker && docker compose up -d

# Edit code, then sync
./sync-code.sh                    # Sync all
./sync-code.sh lms/lms/api.py    # Sync single file

# Check version
./check-version.sh dev
```

### Production

```bash
# Build from git
./build-prod.sh v1.0.0

# Test locally
docker compose -f docker-compose.prod.yml up

# Deploy
docker tag lms-genkiddo:v1.0.0 your-registry/lms-genkiddo:v1.0.0
docker push your-registry/lms-genkiddo:v1.0.0
```

---

## Scripts

| Script             | Description                | Example                            |
| ------------------ | -------------------------- | ---------------------------------- |
| `sync-code.sh`     | Sync local → dev container | `./sync-code.sh [file] [--force]`  |
| `check-version.sh` | Check running version      | `./check-version.sh dev` or `prod` |
| `build-prod.sh`    | Build production image     | `./build-prod.sh v1.0.0`           |

---

## Key Differences

### Development

-   ✅ Hot-reload with `sync-code.sh`
-   ✅ Fast iteration
-   ⚠️ Warns on uncommitted changes
-   📁 Uses local files

### Production

-   ✅ Built from git commit
-   ✅ Immutable image
-   ✅ Version tracked
-   🔒 No code changes at runtime

---

## Workflow

### Daily Dev

```bash
1. Edit code
2. ./sync-code.sh              # Sync & test
3. git commit && git push      # Commit when stable
```

### Release

```bash
1. git tag v1.0.0 && git push --tags
2. ./build-prod.sh v1.0.0      # Build from tag
3. ./check-version.sh prod     # Verify
4. docker push ...             # Deploy
```

---

## Version Tracking

Every container/image has `.version` file:

```bash
# Dev
docker exec lms-frappe-1 cat /home/frappe/frappe-bench/apps/lms/.version

# Prod
docker run --rm lms-genkiddo:v1.0.0 cat /home/frappe/frappe-bench/apps/lms/.version
```

Shows:

-   Git branch
-   Git commit hash
-   Build/sync time

---

## Troubleshooting

### "Uncommitted changes" warning

```bash
# Option 1: Commit first (recommended)
git add . && git commit -m "..."

# Option 2: Force sync (not recommended)
./sync-code.sh --force
```

### Dev/Prod version mismatch

```bash
# Check versions
./check-version.sh dev
./check-version.sh prod lms-genkiddo:v1.0.0

# Sync dev to prod commit
git checkout <prod-commit>
./sync-code.sh
```

### Container not starting

```bash
# Check logs
docker compose logs frappe --tail=50

# Restart
docker compose restart frappe
```

---

## Best Practices

### ✅ DO

-   Commit before deploying to prod
-   Use semantic versioning (`v1.0.0`)
-   Test in dev before prod build
-   Check version after deploy

### ❌ DON'T

-   Deploy uncommitted code
-   Edit code in prod container
-   Use `--force` in production
-   Skip version checks

---

## Files

```
docker/
├── docker-compose.yml       # Development
├── docker-compose.prod.yml  # Production
├── Dockerfile.prod          # Production image
├── sync-code.sh            # Dev sync tool
├── check-version.sh        # Version checker
└── build-prod.sh           # Prod builder
```

---

## Environment Variables

### Production

Create `.env` file:

```bash
DB_PASSWORD=your-secret-password
REGISTRY_URL=your-registry.com
```

### Development

Uses defaults from `docker-compose.yml`

---

## CI/CD Integration

See `.github/workflows/deploy.yml` for automated:

-   Build on push
-   Test before deploy
-   Auto-tag versions
-   Deploy to staging/prod

---

**🎯 Golden Rule:** Dev = fast iteration, Prod = git commits only!
