# 🐳 TownPass Docker Guide

Complete Docker setup and troubleshooting guide for TownPass frontend and backend.

**Status**: ✅ Production Ready  
**Last Updated**: 2025-11-09

---

## 📋 Table of Contents

1. [Quick Start](#-quick-start)
2. [Prerequisites](#-prerequisites)
3. [Project Structure](#-project-structure)
4. [Usage Guide](#-usage-guide)
5. [Build & Deploy](#-build--deploy)
6. [Configuration](#-configuration)
7. [Troubleshooting](#-troubleshooting)
8. [Performance](#-performance)
9. [Advanced Topics](#-advanced-topics)

---

## 🚀 Quick Start

### Production (Recommended)
```bash
# Start both frontend (Nginx) and backend (Flask)
docker-compose up -d

# Access:
# Frontend: http://localhost
# Backend:  http://localhost:5000

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Development (with hot reload)
```bash
# Start development servers
docker-compose -f docker-compose.dev.yml up -d

# Access:
# Frontend: http://localhost:5173 (Vite dev server)
# Backend:  http://localhost:5000 (Flask debug mode)

# View logs
docker-compose -f docker-compose.dev.yml logs -f
```

---

## 📋 Prerequisites

### 1. Install Docker Desktop
Download and install from: https://www.docker.com/products/docker-desktop

### 2. Set up Backend Environment
```bash
# Create backend/.env with your MongoDB URI
cd backend
cp .env.example .env
# Edit .env and add your MONGODB_URI
```

Example `.env`:
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/townpass?retryWrites=true&w=majority
FLASK_ENV=production
```

### 3. Verify Installation
```bash
docker --version
docker-compose --version
```

---

## 📁 Project Structure

```
townpass-dev/
├── docker-compose.yml              # Production orchestration
├── docker-compose.dev.yml          # Development orchestration
│
├── backend/
│   ├── Dockerfile                  # Backend production image
│   ├── .dockerignore
│   ├── app.py
│   ├── database.py
│   ├── requirements.txt
│   └── .env                        # MongoDB config
│
└── frontend/
    ├── Dockerfile                  # Frontend production (multi-stage)
    ├── Dockerfile.dev              # Frontend development
    ├── nginx.conf                  # Nginx configuration
    ├── .dockerignore
    ├── vite.config.js              # Updated for Docker
    └── package.json
```

---

## 📖 Usage Guide

### Common Commands

```bash
# Build all images
docker-compose build

# Build specific service
docker-compose build frontend
docker-compose build backend

# Start services in background
docker-compose up -d

# Start services with logs
docker-compose up

# View logs
docker-compose logs -f           # All services
docker-compose logs -f frontend  # Frontend only
docker-compose logs -f backend   # Backend only

# Stop services (keeps containers)
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes
docker-compose down -v

# Restart a service
docker-compose restart frontend
docker-compose restart backend

# Check service status
docker-compose ps

# Execute command in running container
docker-compose exec backend bash
docker-compose exec frontend sh

# View resource usage
docker stats
```

### Access Points

#### Production
- **Frontend**: http://localhost (port 80)
- **Backend API**: http://localhost:5000
- **Backend Health**: http://localhost:5000/health
- **Backend API Docs**: http://localhost:5000/

#### Development
- **Frontend Dev**: http://localhost:5173 (Vite dev server)
- **Backend Dev**: http://localhost:5000 (Flask debug)

---

## 🏗️ Build & Deploy

### Build Images

```bash
# Build all services
docker-compose build

# Build with no cache (clean build)
docker-compose build --no-cache

# Build individually
docker build -t townpass-frontend:latest -f frontend/Dockerfile frontend/
docker build -t townpass-backend:latest -f backend/Dockerfile backend/
```

### Image Information

```bash
# List images
docker images | grep townpass

# Expected output:
# townpass-frontend    latest    53.6 MB  ✅
# townpass-backend     latest    ~200 MB  ✅

# Inspect image
docker inspect townpass-frontend:latest

# Image history
docker history townpass-frontend:latest
```

### Push to Registry

```bash
# Tag for registry
docker tag townpass-frontend:latest your-registry.com/townpass-frontend:v1.0.0
docker tag townpass-backend:latest your-registry.com/townpass-backend:v1.0.0

# Push to registry
docker push your-registry.com/townpass-frontend:v1.0.0
docker push your-registry.com/townpass-backend:v1.0.0
```

---

## ⚙️ Configuration

### Frontend (Nginx)

**Production** (`frontend/Dockerfile`):
- Multi-stage build
- Stage 1: Node.js 20 build
- Stage 2: Nginx Alpine serve
- Final size: ~53.6 MB

**Development** (`frontend/Dockerfile.dev`):
- Vite dev server with hot reload
- Volume mounting for live changes
- Port 5173 exposed

**Nginx Config** (`frontend/nginx.conf`):
- SPA routing support (try_files)
- Asset caching (1 year for static assets)
- Gzip compression
- Security headers
- Health check endpoint

### Backend (Flask)

**Production**:
- Python 3.11 slim
- Gunicorn WSGI server
- Port 8080 (Cloud Run compatible)
- MongoDB Atlas connection
- Health check endpoint

**Environment Variables**:
```env
MONGODB_URI=<your-mongodb-connection-string>
FLASK_ENV=production
```

### Docker Compose

**Production** (`docker-compose.yml`):
- Backend: port 5000 → 8080 (container)
- Frontend: port 80 → 80 (container)
- Bridge network for inter-service communication
- Health checks enabled
- Auto-restart enabled

**Development** (`docker-compose.dev.yml`):
- Backend: Flask debug mode
- Frontend: Vite dev server
- Volume mounting for live reload
- Hot reload enabled

---

## 🔧 Troubleshooting

### Issue 1: Frontend Build Fails with Rollup Error

**Error**:
```
Error: Cannot find module @rollup/rollup-linux-arm64-gnu
npm has a bug related to optional dependencies
```

**Cause**:
- Architecture mismatch between local machine and Docker container
- `package-lock.json` generated on Mac (ARM64) but Docker building for different architecture
- Rollup's optional native dependencies causing conflicts

**Solution** ✅:
The `frontend/Dockerfile` already handles this by removing `package-lock.json` and running fresh `npm install`:

```dockerfile
# Remove package-lock and do fresh install to avoid architecture mismatch
RUN rm -f package-lock.json && npm install
```

This lets npm resolve correct binaries for the container architecture.

### Issue 2: Port Already in Use

**Error**:
```
Error: port is already allocated
```

**Solution**:
```bash
# Check what's using the port
lsof -i :80      # Frontend
lsof -i :5000    # Backend

# Stop existing services
docker-compose down

# Or change ports in docker-compose.yml
ports:
  - "8080:80"    # Use port 8080 instead of 80
```

### Issue 3: MongoDB Connection Failed

**Error**:
```
MongoDB connection failed - ride persistence disabled
```

**Solution**:
1. Check your `.env` file has valid `MONGODB_URI`
2. Verify MongoDB Atlas allows connections from your IP
3. Test connection string:
   ```bash
   docker-compose exec backend python -c "from database import init_database; print(init_database())"
   ```

### Issue 4: Frontend Shows 404 for Routes

**Cause**: Nginx not configured for SPA routing

**Solution**: Verify `nginx.conf` has:
```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

### Issue 5: Docker Build is Slow

**Solutions**:
```bash
# Use BuildKit for faster builds
export DOCKER_BUILDKIT=1
docker-compose build

# Build with multiple workers
docker-compose build --parallel

# Clean up unused resources
docker system prune -a
```

### Issue 6: Container Won't Start

**Diagnosis**:
```bash
# Check container logs
docker-compose logs backend
docker-compose logs frontend

# Check container status
docker-compose ps

# Inspect container
docker inspect townpass-backend

# Check for port conflicts
docker-compose down
docker-compose up
```

### Issue 7: Hot Reload Not Working in Dev Mode

**Solution**:
Ensure `vite.config.js` has:
```javascript
server: {
  host: true,
  watch: {
    usePolling: true  // Needed for Docker volumes
  }
}
```

---

## 📊 Performance

### Image Sizes

| Service | Size | Notes |
|---------|------|-------|
| Frontend | 53.6 MB | Multi-stage build, Nginx Alpine |
| Backend | ~200 MB | Python 3.11 slim |
| **Total** | **~254 MB** | Optimized for production |

### Build Times

| Build Type | Time | Notes |
|------------|------|-------|
| Cold Build | ~40s | First time, no cache |
| Cached Build | ~10s | With Docker layer cache |
| Frontend Only | ~15s | Multi-stage build |
| Backend Only | ~20s | Python dependencies |

### Runtime Performance

- **Frontend**: Nginx serves static files with caching
- **Backend**: Gunicorn with 1 worker, 8 threads
- **Health Checks**: 30s intervals
- **Auto-restart**: Enabled for both services

---

## 🚀 Advanced Topics

### Multi-Stage Build (Frontend)

The frontend uses a multi-stage build to minimize image size:

**Stage 1 (Builder)**:
```dockerfile
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN rm -f package-lock.json && npm install
COPY . .
RUN npm run build
```

**Stage 2 (Production)**:
```dockerfile
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /app/dist /usr/share/nginx/html
```

Result: Only the built files are in the final image (53.6 MB vs ~500 MB with node_modules).

### Docker Compose Networking

Services communicate through `townpass-network` bridge:

```yaml
networks:
  townpass-network:
    driver: bridge
```

This allows:
- Backend → MongoDB Atlas (external)
- Frontend → Backend (via service name: `http://backend:8080`)
- Frontend → Browser (via localhost)

### Health Checks

**Backend**:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

**Frontend**:
```yaml
healthcheck:
  test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:80/"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 10s
```

### Volume Mounting (Development)

```yaml
volumes:
  - ./frontend/src:/app/src:ro        # Read-only source
  - ./backend:/app                     # Read-write backend
```

Enables hot reload without rebuilding images.

### Environment Variables

**Priority** (highest to lowest):
1. `docker-compose.yml` `environment` section
2. `docker-compose.yml` `env_file` section
3. `.env` file in project root
4. Service-specific `.env` files

### Cloud Deployment

#### Google Cloud Run

```bash
# Build for Cloud Run (already configured)
docker build -t gcr.io/your-project/townpass-backend ./backend
docker build -t gcr.io/your-project/townpass-frontend ./frontend

# Push to Google Container Registry
docker push gcr.io/your-project/townpass-backend
docker push gcr.io/your-project/townpass-frontend

# Deploy
gcloud run deploy townpass-backend \
  --image gcr.io/your-project/townpass-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

gcloud run deploy townpass-frontend \
  --image gcr.io/your-project/townpass-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### AWS ECS / Fargate

```bash
# Tag for ECR
docker tag townpass-backend:latest aws_account_id.dkr.ecr.region.amazonaws.com/townpass-backend:latest
docker tag townpass-frontend:latest aws_account_id.dkr.ecr.region.amazonaws.com/townpass-frontend:latest

# Push to ECR
docker push aws_account_id.dkr.ecr.region.amazonaws.com/townpass-backend:latest
docker push aws_account_id.dkr.ecr.region.amazonaws.com/townpass-frontend:latest
```

#### Docker Hub

```bash
# Tag
docker tag townpass-backend:latest your-username/townpass-backend:latest
docker tag townpass-frontend:latest your-username/townpass-frontend:latest

# Push
docker push your-username/townpass-backend:latest
docker push your-username/townpass-frontend:latest
```

### Security Best Practices

1. **Use non-root user** (already implemented in Dockerfiles)
2. **Don't include secrets in images** (use environment variables)
3. **Use .dockerignore** (already configured)
4. **Scan images for vulnerabilities**:
   ```bash
   docker scan townpass-frontend:latest
   docker scan townpass-backend:latest
   ```
5. **Keep base images updated**:
   ```bash
   docker pull node:20-slim
   docker pull python:3.11-slim
   docker pull nginx:alpine
   ```

### Monitoring & Logging

```bash
# View real-time logs
docker-compose logs -f --tail=100

# Export logs to file
docker-compose logs > logs.txt

# View resource usage
docker stats

# Monitor specific service
docker stats townpass-frontend townpass-backend
```

---

## ✅ Verification Checklist

Before deploying, verify:

- [ ] Both images build successfully
- [ ] Backend health check returns 200
- [ ] Frontend loads in browser
- [ ] Backend API endpoints work
- [ ] MongoDB connection successful
- [ ] Environment variables set correctly
- [ ] No port conflicts
- [ ] Logs show no errors
- [ ] Hot reload works in dev mode (if using dev setup)

### Quick Verification Commands

```bash
# Check images
docker images | grep townpass

# Test backend
curl http://localhost:5000/health
curl http://localhost:5000/

# Test frontend
curl -I http://localhost/

# Check services
docker-compose ps

# View logs
docker-compose logs --tail=50
```

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Vite Documentation](https://vitejs.dev/)

---

## 🎯 Summary

**Docker Setup Status**: ✅ **COMPLETE & PRODUCTION READY**

### What's Included
- ✅ Frontend: Multi-stage build with Nginx (53.6 MB)
- ✅ Backend: Python + Flask + Gunicorn (~200 MB)
- ✅ Production: docker-compose.yml (optimized)
- ✅ Development: docker-compose.dev.yml (hot reload)
- ✅ Health checks for both services
- ✅ Networking between services
- ✅ Architecture-independent builds
- ✅ Security best practices
- ✅ Documentation (this file)

### Quick Reference

| Command | Purpose |
|---------|---------|
| `docker-compose up -d` | Start production |
| `docker-compose -f docker-compose.dev.yml up -d` | Start development |
| `docker-compose logs -f` | View logs |
| `docker-compose ps` | Check status |
| `docker-compose down` | Stop services |
| `docker-compose build` | Rebuild images |

---

**Build Date**: 2025-11-09  
**Status**: ✅ Production Ready  
**Total Build Time**: ~40 seconds (cold), ~10 seconds (cached)  
**Total Stack Size**: ~254 MB
