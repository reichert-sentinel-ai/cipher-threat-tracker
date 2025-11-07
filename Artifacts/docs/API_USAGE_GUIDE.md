# Criminal Intelligence Database Star Rating Portfolio Optimizer - API Usage Guide

**Version:** 2.0.0  
**Base URL:** `http://localhost:8000/api/v1`  
**Authentication:** API Key (X-API-Key header)

---

## 🚀 Quick Start

### 1. Start the API

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
python -m uvicorn src.api.main:app --reload

# API will be available at: http://localhost:8000
# Interactive docs: http://localhost:8000/docs
```

### 2. Authenticate

All endpoints (except health checks) require an API key:

```bash
# Development key (default)
export API_KEY="dev-key-12345"
```

Include the API key in all requests:
```bash
curl -H "X-API-Key: dev-key-12345" http://localhost:8000/api/v1/measures
```

---

## 📋 Available Endpoints

### Health & Status

```bash
# Basic health check
GET /health

# Readiness check (for Kubernetes)
GET /health/ready

# Liveness check
GET /health/live
```

### Measures

```bash
# List all 12 HEDIS measures
GET /api/v1/measures

# Get details for specific measure
GET /api/v1/measures/{measure_code}

# Get performance metrics
GET /api/v1/measures/{measure_code}/performance
```

### Predictions

```bash
# Single member prediction
POST /api/v1/predict/{measure_code}

# Batch prediction (up to 1000 members)
POST /api/v1/predict/batch/{measure_code}

# Portfolio prediction (all 12 measures for one member)
POST /api/v1/predict/portfolio
```

### Portfolio Analytics

```bash
# Portfolio summary
GET /api/v1/portfolio/summary

# Gap list with filters
POST /api/v1/portfolio/gaps

# Priority member list
GET /api/v1/portfolio/priority-list

# Optimize interventions
POST /api/v1/portfolio/optimize
```

### Analytics

```bash
# Calculate Star Rating
POST /api/v1/analytics/star-rating

# Run scenario simulation
POST /api/v1/analytics/simulate

# Calculate ROI
GET /api/v1/analytics/roi
```

---

## 💡 Usage Examples

### Example 1: Single Member Prediction

```python
import requests

url = "http://localhost:8000/api/v1/predict/GSD"
headers = {"X-API-Key": "dev-key-12345"}
data = {
    "member_id": "M123456",
    "measurement_year": 2025,
    "include_shap": True
}

response = requests.post(url, json=data, headers=headers)
result = response.json()

print(f"Risk Score: {result['risk_score']:.2f}")
print(f"Risk Tier: {result['risk_tier']}")
print(f"Recommendation: {result['recommendation']}")
```

### Example 2: Batch Prediction

```python
url = "http://localhost:8000/api/v1/predict/batch/GSD"
headers = {"X-API-Key": "dev-key-12345"}
data = {
    "member_ids": ["M001", "M002", "M003"],
    "measurement_year": 2025,
    "include_shap": False
}

response = requests.post(url, json=data, headers=headers)
result = response.json()

print(f"Processed: {result['total_processed']}")
print(f"High Risk: {result['total_high_risk']}")
```

### Example 3: Portfolio Prediction

```python
url = "http://localhost:8000/api/v1/predict/portfolio"
headers = {"X-API-Key": "dev-key-12345"}
data = {
    "member_id": "M123456",
    "measures": ["GSD", "KED", "EED", "BPD"],  # Or omit for all 12
    "include_shap": True
}

response = requests.post(url, json=data, headers=headers)
result = response.json()

print(f"Total Gaps: {result['total_gaps']}")
print(f"Priority Score: {result['priority_score']:.1f}")
print(f"Estimated Value: ${result['estimated_value']:,.0f}")
print(f"Interventions: {result['recommended_interventions']}")
```

### Example 4: Star Rating Simulation

```python
url = "http://localhost:8000/api/v1/analytics/simulate"
headers = {"X-API-Key": "dev-key-12345"}
data = {
    "baseline_rates": {
        "GSD": 0.70,
        "KED": 0.65,
        "EED": 0.68,
        "BPD": 0.72
    },
    "closure_scenarios": [0.1, 0.2, 0.3, 0.5],
    "strategy": "balanced",
    "plan_size": 100000,
    "intervention_cost": 150.0
}

response = requests.post(url, json=data, headers=headers)
result = response.json()

print(f"Baseline Stars: {result['baseline_stars']}")
print(f"Optimal Closure Rate: {result['optimal_closure_rate']*100:.0f}%")
print(f"Max ROI: {result['max_roi_scenario']['roi']:.1f}%")
```

---

## ⚡ Rate Limits

- **Limit:** 100 requests per minute per API key
- **Headers:** Check `X-RateLimit-Remaining` header
- **Exceeded:** Returns 429 with `Retry-After` header

---

## 🔒 Security

- **PHI Protection:** All member IDs are hashed (SHA-256)
- **Logging:** PHI-safe structured logging
- **HIPAA Compliance:** No PII exposed in responses or logs

---

## 📊 Response Times

- Single prediction: < 50ms (p95)
- Batch (100 members): < 500ms (p95)
- Portfolio (12 measures): < 200ms (p95)
- Portfolio summary: < 1000ms (p95)

---

## 🛠️ Error Handling

All errors return structured JSON:

```json
{
  "error": "Error Type",
  "detail": "Detailed message",
  "status_code": 404,
  "request_id": "abc-123",
  "timestamp": 1698172800.0
}
```

**Common Status Codes:**
- `200` - Success
- `401` - Invalid/missing API key
- `404` - Resource not found
- `422` - Validation error
- `429` - Rate limit exceeded
- `500` - Internal server error
- `503` - Service unavailable (models not loaded)

---

## 📖 Interactive Documentation

Visit `http://localhost:8000/docs` for:
- **Swagger UI** - Try out endpoints interactively
- **Schema definitions** - See all request/response models
- **Examples** - Copy-paste ready examples

---

## 🆘 Support

- **GitHub:** https://github.com/StarGuardAi
- **Email:** bobareichert@gmail.com
- **Documentation:** See `docs/` directory
- **Issues:** Open a GitHub issue

---

## 🎯 Measure Codes Reference

**Tier 1 (Diabetes) - Triple-weighted:**
- `GSD` - Glycemic Status Assessment (3x) [Production]
- `KED` - Kidney Health Evaluation (3x) [NEW 2025]

**Tier 1 (Diabetes) - Standard:**
- `EED` - Eye Exam for Diabetes
- `PDC-DR` - Medication Adherence (Diabetes)
- `BPD` - Blood Pressure Control [NEW 2025]

**Tier 2 (Cardiovascular):**
- `CBP` - High Blood Pressure Control (3x)
- `SUPD` - Statin Therapy
- `PDC-RASA` - Med Adherence (HTN)
- `PDC-STA` - Med Adherence (Cholesterol)

**Tier 3 (Cancer Screening):**
- `BCS` - Breast Cancer Screening
- `COL` - Colorectal Cancer Screening

**Tier 4 (Health Equity):**
- `HEI` - Health Equity Index

---

**API Version:** 2.0.0  
**Last Updated:** October 24, 2025



---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
