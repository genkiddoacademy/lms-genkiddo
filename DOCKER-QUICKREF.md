# LMS Genkiddo - Quick Reference

## 🚀 Common Commands

```bash
# Development
cd docker
docker compose up -d              # Start
./sync-code.sh                    # Sync code
./check-version.sh dev            # Check version
docker compose logs -f frappe     # View logs
docker compose restart frappe     # Restart

# Production
./build-prod.sh v1.0.0           # Build
./check-version.sh prod          # Verify
docker compose -f docker-compose.prod.yml up  # Test local
```

## 📁 Important Files

```
docker/
├── DOCKER.md              # Full documentation
├── sync-code.sh          # Dev: sync code
├── build-prod.sh         # Prod: build image
├── check-version.sh      # Check versions
├── docker-compose.yml    # Dev config
└── docker-compose.prod.yml  # Prod config
```

## 🔄 Workflow

### Development

```bash
1. Edit code
2. ./sync-code.sh
3. Test
4. git commit & push
```

### Release

```bash
1. git tag v1.0.0
2. ./build-prod.sh v1.0.0
3. Test & deploy
```

## 📖 Full Documentation

See [`docker/DOCKER.md`](docker/DOCKER.md) for complete guide.

## 🐛 Issues?

-   Check logs: `docker compose logs frappe`
-   Restart: `docker compose restart frappe`
-   Version: `./check-version.sh dev`
