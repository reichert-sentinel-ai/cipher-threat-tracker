# Cipher Threat Intelligence - Architecture

**Date**: December 2024  
**Repository**: Cipher Threat Intelligence  
**Version**: 1.0

**IMPORTANT**: This is a portfolio demonstration project using sample/threat intelligence data for demonstration purposes only.

## System Overview

Cipher is a comprehensive cyber threat intelligence platform that collects, analyzes, and visualizes threat indicators from multiple sources. The system uses machine learning for anomaly detection and threat classification, and graph databases for threat actor attribution and campaign correlation.

---

## Architecture Components

### 1. IOC Collection Pipeline

**Collectors:**
- `OTXCollector`: AlienVault OTX API integration
- `AbuseCollector`: Abuse.ch feeds (MalwareBazaar, URLhaus)
- `PhishTankCollector`: Phishing URL database
- `NVDCollector`: NIST National Vulnerability Database (CVEs)

**Orchestration:**
- `IOCOrchestrator`: Coordinates collection from all sources
- `BaseCollector`: Base class with normalization logic
- `IOCDeduplicator`: Deduplicates IOCs across sources

### 2. Data Storage

**Elasticsearch:**
- IOC index with full-text search
- Threat type, confidence, and metadata filtering
- Real-time indexing and querying

**Neo4j:**
- Threat actor network graph
- Campaign relationships
- IOC-actor associations

### 3. Machine Learning Models

**Anomaly Detection:**
- `TrafficAutoencoder`: PyTorch autoencoder for zero-day detection
- `IsolationForestDetector`: Behavioral anomaly detection
- `AnomalyDetector`: Wrapper for autoencoder threshold fitting

**Classification:**
- `IOCClassifier`: XGBoost classifier for threat type prediction
- Feature extraction from IOC metadata

**Correlation:**
- `ThreatCorrelationEngine`: Links related IOCs into campaigns
- Network graph construction using NetworkX

### 4. API Layer

**FastAPI Application:**
- RESTful API with OpenAPI documentation
- Endpoints for IOC lookup, threat analysis, detection, and visualization
- CORS middleware for frontend integration

**Routers:**
- `/api/v1/ioc/*`: IOC lookup and collection
- `/api/v1/threats/*`: Threat analysis and statistics
- `/api/v1/actors/*`: Threat actor information
- `/api/v1/campaigns/*`: Campaign correlation
- `/api/v1/detect/*`: Anomaly detection and classification
- `/api/v1/timeline/*`: IOC timeline visualization
- `/api/v1/network/*`: Threat network graph

### 5. Dashboard

**Streamlit Application:**
- Interactive dashboard with multiple pages
- Real-time threat visualization
- IOC lookup interface
- Timeline and network graph views

---

## Data Flow

```
┌─────────────┐
│ IOC Sources │
│ (OTX, etc.) │
└──────┬──────┘
       │
       ▼
┌──────────────┐
│  Collectors  │
│ (Normalize)  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│Deduplicator  │
└──────┬───────┘
       │
       ├─────────────────┐
       │                 │
       ▼                 ▼
┌──────────────┐  ┌──────────────┐
│Elasticsearch │  │    Neo4j     │
│  (IOC Index) │  │(Threat Graph)│
└──────┬───────┘  └──────┬───────┘
       │                 │
       │                 │
       ▼                 ▼
┌──────────────┐  ┌──────────────┐
│   FastAPI    │  │Correlation   │
│     API      │  │   Engine     │
└──────┬───────┘  └──────┬───────┘
       │                 │
       └────────┬────────┘
                │
                ▼
         ┌──────────────┐
         │   Streamlit  │
         │  Dashboard   │
         └──────────────┘
```

---

## IOC Data Model

```python
{
    "ioc_value": str,           # IOC value (IP, URL, hash, etc.)
    "ioc_type": str,             # Normalized type (ip, url, hash, etc.)
    "ioc_id": str,               # Unique identifier (SHA256 hash)
    "source": str,               # Data source (otx, abuse_ch, etc.)
    "threat_type": str,          # Threat classification
    "first_seen": str,           # ISO 8601 timestamp
    "last_seen": str,            # ISO 8601 timestamp
    "confidence": float,         # Confidence score [0, 1]
    "tags": List[str],           # Tags and labels
    "metadata": Dict             # Additional metadata
}
```

---

## Threat Actor Network Model

**Neo4j Schema:**
```
(:ThreatActor)-[:USES]->(:IOC)
(:IOC)-[:FROM_CAMPAIGN]->(:Campaign)
(:Campaign)-[:USES_TECHNIQUE]->(:MITRETechnique)
(:ThreatActor)-[:ASSOCIATED_WITH]->(:ThreatActor)
```

---

## Model Architecture

### Autoencoder
```
Input (512) → Encoder (256) → Bottleneck (128) → Decoder (256) → Output (512)
```

**Purpose:** Detect anomalies in network traffic
**Threshold:** 95th percentile reconstruction error

### Isolation Forest
- **Contamination:** 0.05 (5% anomalies)
- **Features:** 50 behavioral indicators
- **Purpose:** Behavioral anomaly detection

### IOC Classifier
- **Algorithm:** XGBoost
- **Features:** 30+ IOC metadata features
- **Target:** Threat type classification
- **Performance:** 95% F1-score target

---

## API Endpoints

### IOC Management
- `POST /api/v1/ioc/check` - Check IOC
- `GET /api/v1/ioc/search` - Search IOCs
- `POST /api/v1/ioc/collect` - Trigger collection

### Threat Analysis
- `GET /api/v1/threats` - Get active threats
- `GET /api/v1/threats/stats` - Threat statistics

### Detection
- `POST /api/v1/detect/anomaly` - Anomaly detection
- `POST /api/v1/detect/classify` - IOC classification

### Visualization
- `GET /api/v1/timeline` - IOC timeline
- `GET /api/v1/network` - Threat network graph

---

## Deployment

### Docker Compose Services
1. **api**: FastAPI application
2. **elasticsearch**: IOC indexing
3. **neo4j**: Threat graph database
4. **dashboard**: Streamlit dashboard

### Environment Variables
- `ELASTICSEARCH_HOST`: Elasticsearch host
- `NEO4J_URI`: Neo4j connection URI
- `NEO4J_USER`: Neo4j username
- `NEO4J_PASSWORD`: Neo4j password
- `OTX_API_KEY`: OTX API key (optional)
- `NVD_API_KEY`: NVD API key (optional)

---

## Performance Targets

- **API Latency:** <100ms for IOC lookup
- **Collection Rate:** 100+ IOCs per source per minute
- **Anomaly Detection:** 95%+ accuracy
- **IOC Classification:** 95% F1-score
- **Dashboard Load Time:** <2 seconds

---

## Security Considerations

1. **API Authentication:** Implement API keys or OAuth2
2. **Rate Limiting:** Protect against abuse
3. **Data Encryption:** Encrypt sensitive IOC data
4. **Access Control:** Restrict access to threat intelligence data
5. **Audit Logging:** Log all IOC lookups and detections

---

## Future Enhancements

1. **MITRE ATT&CK Integration:** Full TTP mapping
2. **Real-time Streaming:** Kafka integration for live IOC feeds
3. **Advanced Visualizations:** Cytoscape.js network graphs
4. **Threat Actor Attribution:** ML-based attribution models
5. **Incident Response:** Automated response workflows

---

**Built for homeland security intelligence operations** 🔐

