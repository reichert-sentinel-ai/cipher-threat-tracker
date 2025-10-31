# Criminal Intelligence Database Portfolio Optimizer - Docker Guide

**Last Updated:** October 25, 2025  
**Docker Version:** 24.0+  
**Docker Compose Version:** 2.20+

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Docker Files](#docker-files)
5. [Development Setup](#development-setup)
6. [Production Setup](#production-setup)
7. [Common Commands](#common-commands)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

The Criminal Intelligence Database Portfolio Optimizer uses Docker for:
- **Consistent environments** across development, staging, and production
- **Simplified deployment** with containerization
- **Easy local development** with docker-compose
- **Scalability** with orchestration platforms (ECS, Kubernetes)

### Architecture

```
┌─────────────────┐
│   Load Balancer │
│   (ALB/Nginx)   │
└────────┬────────┘
         │
    ┌────┴────┐
    │   API   │ (Port 8000)
    │Container│
    └────┬────┘
         │
    ┌────┴────────────────┐
    │                     │
┌───┴────┐        ┌──────┴──────┐
│   DB   │        │    Redis    │
│(Postgres)│      │   (Cache)   │
└────────┘        └─────────────┘
```

---

## 🔧 Prerequisites

###

 Required Software
- **Docker:** Version 24.0+ ([Install](https://docs.docker.com/get-docker/))
- **Docker Compose:** Version 2.20+ (included with Docker Desktop)
- **Git:** For cloning the repository

### System Requirements
- **RAM:** Minimum 4GB, Recommended 8GB+
- **Disk Space:** 10GB free space
- **OS:** Linux, macOS, or Windows (with WSL2)

### Verify Installation

```bash
# Check Docker version
docker --version
# Output: Docker version 24.0.0, build...

# Check Docker Compose version
docker-compose --version
# Output: Docker Compose version v2.20.0

# Test Docker is running
docker run hello-world
```

---

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended for Local Development)

```bash
# 1. Navigate to project directory
cd HEDIS-MA-Top-12-w-HEI-Prep

# 2. Start all services
bash scripts/docker-compose-up.sh dev

# 3. Access API
open http://localhost:8000/docs

# 4. Stop services
bash scripts/docker-compose-down.sh dev
```

### Option 2: Standalone Docker Container

```bash
# 1. Build image
bash scripts/docker-build.sh

# 2. Run container
bash scripts/docker-run.sh

# 3. Test API
curl http://localhost:8000/api/v1/health

# 4. Stop container
docker stop hedis_api_standalone
```

---

## 📁 Docker Files

### Dockerfile
**Purpose:** Production-ready multi-stage build

**Key Features:**
- Multi-stage build for smaller image size
- Non-root user for security
- Health checks built-in
- Optimized layer caching

**Stages:**
1. **Builder:** Compile Python packages
2. **Runtime:** Final lightweight image

**Expected Size:** ~500MB

### docker-compose.yml
**Purpose:** Local development environment

**Services:**
- `api`: FastAPI application
- `db`: PostgreSQL 15 database
- `redis`: Redis cache
- `pgadmin`: Database management UI (optional)

**Features:**
- Hot reload for code changes
- Volume mounts for development
- Health checks for all services
- Isolated network

### docker-compose.prod.yml
**Purpose:** Production-like environment

**Differences from dev:**
- No volume mounts
- Read-only containers
- Resource limits
- AWS CloudWatch logging
- Security optimizations

### .dockerignore
**Purpose:** Exclude files from Docker build context

**Excludes:**
- Test files
- Documentation
- Data files
- IDE configurations
- Git history

---

## 🔧 Development Setup

### 1. Start Development Environment

```bash
# Start all services
bash scripts/docker-compose-up.sh dev

# Or with pgAdmin (database UI)
bash scripts/docker-compose-up.sh dev tools
```

### 2. Verify Services

```bash
# Check running containers
docker-compose ps

# Expected output:
# NAME        STATUS       PORTS
# hedis_api   Up (healthy) 0.0.0.0:8000->8000/tcp
# hedis_db    Up (healthy) 0.0.0.0:5432->5432/tcp
# hedis_redis Up (healthy) 0.0.0.0:6379->6379/tcp
```

### 3. Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| API Docs | http://localhost:8000/docs | None |
| API Health | http://localhost:8000/api/v1/health | None |
| Database | localhost:5432 | hedis_api / dev_password |
| Redis | localhost:6379 | None |
| pgAdmin | http://localhost:5050 | admin@hedis.local / admin |

### 4. View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api

# Last 100 lines
docker-compose logs --tail=100 api
```

### 5. Run Database Migrations

```bash
# Access API container
docker-compose exec api bash

# Run migrations
alembic upgrade head

# Exit container
exit
```

### 6. Run Tests Inside Container

```bash
# Run all tests
docker-compose exec api pytest

# Run with coverage
docker-compose exec api pytest --cov=src tests/

# Run specific test file
docker-compose exec api pytest tests/database/test_models.py
```

### 7. Hot Reload

Code changes in `src/` are automatically detected and the API reloads. No need to restart!

---

## 🚀 Production Setup

### 1. Build Production Image

```bash
# Set environment variables
export IMAGE_TAG=$(git rev-parse --short HEAD)
export BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')

# Build image
docker build -t hedis-portfolio-api:$IMAGE_TAG .
```

### 2. Run Production Container

```bash
# Load environment variables
export DATABASE_URL="postgresql://user:pass@rds-endpoint:5432/hedis"
export API_KEY_HASH="production_key_hash"
export REDIS_URL="redis://elasticache-endpoint:6379"

# Run container
docker run -d \
  --name hedis_api_prod \
  -p 8000:8000 \
  -e DATABASE_URL="$DATABASE_URL" \
  -e API_KEY_HASH="$API_KEY_HASH" \
  -e REDIS_URL="$REDIS_URL" \
  -e ENVIRONMENT=production \
  -e LOG_LEVEL=INFO \
  --restart unless-stopped \
  hedis-portfolio-api:$IMAGE_TAG
```

### 3. Push to ECR (AWS)

```bash
# Authenticate with ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin $ECR_REGISTRY

# Tag image
docker tag hedis-portfolio-api:$IMAGE_TAG \
  $ECR_REGISTRY/hedis-portfolio-api:$IMAGE_TAG

# Push to ECR
docker push $ECR_REGISTRY/hedis-portfolio-api:$IMAGE_TAG
```

---

## 🛠️ Common Commands

### Building

```bash
# Build image
docker build -t hedis-portfolio-api .

# Build without cache
docker build --no-cache -t hedis-portfolio-api .

# Build with specific target stage
docker build --target builder -t hedis-builder .
```

### Running

```bash
# Run in background
docker run -d -p 8000:8000 hedis-portfolio-api

# Run with environment variables
docker run -d -p 8000:8000 \
  -e LOG_LEVEL=DEBUG \
  hedis-portfolio-api

# Run with volume mount
docker run -d -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  hedis-portfolio-api

# Run interactively
docker run -it hedis-portfolio-api bash
```

### Inspecting

```bash
# View running containers
docker ps

# View all containers
docker ps -a

# View container logs
docker logs -f hedis_api

# Execute command in container
docker exec -it hedis_api bash

# Inspect container
docker inspect hedis_api

# View container resource usage
docker stats hedis_api
```

### Cleaning Up

```bash
# Stop container
docker stop hedis_api

# Remove container
docker rm hedis_api

# Remove image
docker rmi hedis-portfolio-api

# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune -a

# Remove everything (use with caution!)
docker system prune -a --volumes
```

---

## 🔍 Troubleshooting

### Issue: Container Fails to Start

**Symptoms:**
```bash
docker-compose up
# Error: Exited with code 1
```

**Solutions:**
```bash
# Check logs
docker-compose logs api

# Common causes:
# 1. Database not ready → Wait for health check
# 2. Missing environment variables → Check .env file
# 3. Port already in use → Stop conflicting service
lsof -i :8000
```

### Issue: Database Connection Failed

**Symptoms:**
```
OperationalError: could not connect to server
```

**Solutions:**
```bash
# 1. Check database container is running
docker-compose ps db

# 2. Check database logs
docker-compose logs db

# 3. Verify connection string
docker-compose exec api env | grep DATABASE_URL

# 4. Test connection manually
docker-compose exec db psql -U hedis_api -d hedis_portfolio
```

### Issue: Image Size Too Large

**Symptoms:**
```bash
docker images
# hedis-portfolio-api  latest  2.5GB
```

**Solutions:**
```bash
# 1. Check what's taking space
docker history hedis-portfolio-api

# 2. Ensure .dockerignore is working
docker build --progress=plain . | grep "Sending build context"

# 3. Use multi-stage builds (already implemented)

# 4. Remove unnecessary dependencies
```

### Issue: Hot Reload Not Working

**Symptoms:**
- Code changes not reflected in API

**Solutions:**
```bash
# 1. Ensure volume mounts are correct
docker-compose config

# 2. Check if using dev docker-compose file
# Should see: --reload flag in command

# 3. Restart API service
docker-compose restart api
```

### Issue: Out of Disk Space

**Symptoms:**
```
Error response from daemon: no space left on device
```

**Solutions:**
```bash
# Check disk usage
docker system df

# Remove unused containers
docker container prune

# Remove unused images
docker image prune -a

# Remove volumes (careful!)
docker volume prune

# Clean everything
docker system prune -a --volumes
```

---

## 📊 Performance Tuning

### 1. Optimize Image Build

```dockerfile
# Use build cache effectively
# Copy requirements first (changes less often)
COPY requirements-full.txt .
RUN pip install -r requirements-full.txt

# Copy code after (changes more often)
COPY . .
```

### 2. Resource Limits

```yaml
# In docker-compose.yml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
```

### 3. Connection Pooling

```python
# Already configured in src/database/connection.py
pool_size=5,              # Min connections
max_overflow=15,          # Max additional
pool_timeout=30,          # Wait time
pool_recycle=3600         # Recycle after 1 hour
```

---

## 🔐 Security Best Practices

### 1. Use Non-Root User
✅ Already implemented in Dockerfile

### 2. Scan for Vulnerabilities

```bash
# Using Docker Scout (built-in)
docker scout cves hedis-portfolio-api:latest

# Using Trivy
trivy image hedis-portfolio-api:latest
```

### 3. Keep Base Images Updated

```bash
# Update base image
docker pull python:3.11-slim

# Rebuild with latest base
docker build --pull -t hedis-portfolio-api .
```

### 4. Use Secrets Management

```bash
# Don't hardcode secrets in Dockerfile
# Use environment variables or Docker secrets

# For Docker Compose
docker-compose --env-file .env.production up
```

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)

---

## ✅ Docker Setup Checklist

- [ ] Docker and Docker Compose installed
- [ ] Repository cloned
- [ ] Docker images build successfully
- [ ] All services start with docker-compose
- [ ] API responds to health checks
- [ ] Database connection working
- [ ] Tests pass in container
- [ ] Logs accessible
- [ ] Image size optimized (< 1GB)
- [ ] Security scan passed
- [ ] Documentation reviewed

---

**Need help?** Check the troubleshooting section or contact the development team.





---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
