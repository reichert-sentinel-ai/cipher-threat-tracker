# Live Demo Deployment Guide

**Repository**: Cipher Threat Intelligence  
**Date**: December 2024  
**Status**: Complete

---

## Quick Deploy to Streamlit Cloud

### Step 1: Prepare Repository

```bash
cd project/repo-cipher

# Ensure requirements.txt includes:
# streamlit>=1.28.0
# fastapi>=0.104.0
# torch>=2.0.0
# elasticsearch>=8.0.0
# neo4j>=5.0.0
# etc.

# Ensure streamlit_app.py exists in root
```

### Step 2: Deploy

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Repository: `reichert-sentinel-ai/cipher-threat-tracker`
5. Main file: `streamlit_app.py`
6. Branch: `main`
7. Click "Deploy"

### Step 3: Configure Environment

Add environment variables in Streamlit Cloud:
- `CIPHER_ES_URL`: Elasticsearch URL
- `CIPHER_NEO4J_URL`: Neo4j connection string
- `OTX_API_KEY`: AlienVault OTX API key
- `ABUSE_CH_API_KEY`: Abuse.ch API key (optional)

### Step 4: Access Demo

URL: `https://cipher-threat-tracker.streamlit.app`

---

## Docker Deployment

```bash
# Build
docker build -t cipher:latest .

# Run with docker-compose (includes Elasticsearch & Neo4j)
docker-compose up -d
```

---

## Environment Variables

```bash
CIPHER_ES_URL=http://localhost:9200
CIPHER_NEO4J_URL=bolt://localhost:7687
CIPHER_NEO4J_USER=neo4j
CIPHER_NEO4J_PASS=password
OTX_API_KEY=your_otx_key_here
ABUSE_CH_API_KEY=your_abuse_ch_key_here
NVD_API_KEY=your_nvd_key_here
```

---

*See [Guardian Deployment Guide](../repo-guardian/docs/DEPLOYMENT_GUIDE.md) for detailed deployment options.*

