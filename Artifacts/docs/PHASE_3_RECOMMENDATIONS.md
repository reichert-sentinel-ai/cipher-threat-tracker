# Phase 3: API Development - Detailed Recommendations & Suggestions

**Status:** 🚀 Ready to Start  
**Expected Duration:** 2-3 weeks  
**Complexity:** Medium  
**Recommended Start Date:** October 22, 2025

---

## 🎯 Executive Summary

Phase 3 focuses on creating a production-ready REST API that exposes your 91% AUC-ROC prediction model. This phase transforms your research code into a deployable service that healthcare organizations can integrate into their care management workflows.

### Key Decisions Needed
1. **API Framework:** FastAPI vs Flask (Recommendation: FastAPI)
2. **Authentication:** Yes/No, and which method (Recommendation: API Keys)
3. **Database:** Store predictions? (Recommendation: Optional, PostgreSQL)
4. **Deployment Target:** Cloud provider (Recommendation: AWS or Azure)
5. **Rate Limiting:** Implement now or Phase 4? (Recommendation: Now)

---

## 📊 Phase 3 Options Analysis

### Option A: Minimal API (Fastest - 1 week)
**What You Get:**
- Basic FastAPI with `/predict` endpoint
- Simple request/response schemas
- Health check endpoint
- Auto-generated Swagger docs
- No authentication
- No database

**Pros:**
- ✅ Fastest to deploy
- ✅ Proves concept quickly
- ✅ Minimal complexity

**Cons:**
- ❌ Not production-ready
- ❌ No audit trail
- ❌ Security concerns

**Recommendation:** ❌ Skip - Not suitable for healthcare

---

### Option B: Production-Lite API (Recommended - 2 weeks)
**What You Get:**
- Full FastAPI application
- Single + batch prediction endpoints
- Model info + health endpoints
- API key authentication
- Request/response logging (PHI-safe)
- Comprehensive testing
- OpenAPI documentation
- Performance optimization (< 100ms)

**Pros:**
- ✅ Production-ready for pilot
- ✅ HIPAA-compliant logging
- ✅ Good performance
- ✅ Complete documentation
- ✅ Testable and maintainable

**Cons:**
- ⚠️ No prediction history storage
- ⚠️ Limited to synchronous requests

**Recommendation:** ✅ **START HERE** - Best balance

---

### Option C: Enterprise API (Full-Featured - 3-4 weeks)
**What You Get:**
- Everything from Option B, plus:
- PostgreSQL database for prediction history
- OAuth2 authentication
- Asynchronous processing
- Redis caching
- Webhooks for batch completions
- Advanced rate limiting per client
- Detailed analytics dashboard

**Pros:**
- ✅ Enterprise-grade features
- ✅ Scalable architecture
- ✅ Complete audit trail

**Cons:**
- ❌ Longer development time
- ❌ More infrastructure complexity
- ❌ Higher operational costs

**Recommendation:** ⏳ Phase 5 - Add these features after deployment

---

## 🏗️ Recommended Architecture (Option B)

```
┌─────────────────────────────────────────────┐
│           Client Applications               │
│    (Care Management System, Dashboard)     │
└────────────────┬────────────────────────────┘
                 │
                 ├─── HTTP/HTTPS
                 │
┌────────────────▼────────────────────────────┐
│          FastAPI Application                │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  Endpoints Layer                    │   │
│  │  • /api/v1/predict                  │   │
│  │  • /api/v1/predict/batch            │   │
│  │  • /api/v1/model/info               │   │
│  │  • /health, /health/ready           │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  Middleware Layer                   │   │
│  │  • Authentication (API Keys)        │   │
│  │  • PHI-Safe Logging                 │   │
│  │  • Error Handling                   │   │
│  │  • CORS Configuration               │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  Business Logic Layer               │   │
│  │  • Model Loading (Singleton)        │   │
│  │  • Feature Validation               │   │
│  │  • SHAP Interpretation              │   │
│  │  • Batch Processing                 │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
                 │
                 ├─── Loads from disk
                 │
┌────────────────▼────────────────────────────┐
│        Model Artifacts                      │
│  • logistic_regression_final.pkl            │
│  • scaler.pkl                               │
│  • feature_names.txt                        │
└─────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack Recommendations

### Core Framework: FastAPI ✅ (Recommended)

**Why FastAPI over Flask/Django:**
- ✅ Built-in async support (future-proof)
- ✅ Auto-generated OpenAPI docs (Swagger UI)
- ✅ Pydantic validation (type safety)
- ✅ Fastest Python framework (~3x Flask)
- ✅ Modern, growing community
- ✅ Perfect for ML APIs

**Alternative:** Flask-RESTX
- ✅ Simpler, more familiar
- ❌ Slower performance
- ❌ Manual OpenAPI setup
- ❌ No async support

**Verdict:** FastAPI - Superior for ML APIs

---

### Authentication: API Keys ✅ (Recommended)

**Why API Keys over OAuth2:**
- ✅ Simpler to implement (1 day vs 3-4 days)
- ✅ Easier for clients to integrate
- ✅ Sufficient for pilot deployment
- ✅ Can upgrade to OAuth2 later
- ✅ Works with care management systems

**Implementation:**
```python
# Simple but effective
X-API-Key: hedis_gsd_key_abc123xyz

# Or bearer token
Authorization: Bearer hedis_gsd_key_abc123xyz
```

**Alternative:** OAuth2
- ✅ More secure for multi-tenant
- ❌ Overkill for pilot
- ❌ Complex setup

**Verdict:** API Keys for Phase 3, OAuth2 for Phase 5

---

### Database: Optional PostgreSQL

**For Phase 3:**
❌ **Skip database initially** - Focus on API functionality

**Reasons:**
- You can add logging without DB (file-based)
- Faster development
- Less infrastructure complexity
- Can add in Phase 4/5

**When to add database:**
- Need prediction history
- Multi-client usage tracking
- Regulatory audit requirements
- Analytics dashboard

**Recommended for Phase 5:**
```
PostgreSQL 15+ for:
- Prediction history
- Usage analytics
- Audit logs
- Client management
```

---

### Caching: Redis (Phase 5)

**For Phase 3:**
❌ **Skip Redis** - Model loads fast enough

**Reasons:**
- Model prediction < 10ms
- Adding Redis = complexity
- Can cache in-memory initially

**When to add Redis:**
- > 1000 requests/second
- Serving repeated predictions
- Need distributed caching

**Verdict:** Phase 5 optimization

---

## 📋 Detailed Implementation Recommendations

### 1. Project Structure (Recommended)

```
src/api/
├── __init__.py
├── main.py                 # FastAPI app + uvicorn config
├── config.py               # API configuration
├── dependencies.py         # Dependency injection
│
├── routers/                # Endpoint groups
│   ├── __init__.py
│   ├── prediction.py       # /predict endpoints
│   ├── model.py            # /model endpoints
│   └── health.py           # /health endpoints
│
├── schemas/                # Pydantic models
│   ├── __init__.py
│   ├── prediction.py       # Request/response models
│   ├── model.py
│   └── error.py
│
├── middleware/
│   ├── __init__.py
│   ├── auth.py             # API key validation
│   ├── logging.py          # PHI-safe logging
│   └── errors.py           # Error handlers
│
├── services/               # Business logic
│   ├── __init__.py
│   ├── predictor.py        # Model prediction logic
│   ├── validator.py        # Feature validation
│   └── interpreter.py      # SHAP interpretation
│
└── utils/
    ├── __init__.py
    ├── model_loader.py     # Singleton model loader
    └── constants.py        # API constants
```

**Why this structure:**
- ✅ Separates concerns
- ✅ Easy to test
- ✅ Scalable
- ✅ FastAPI best practice

---

### 2. API Endpoints (Recommended Set)

#### Core Endpoints (Must Have):

**1. Single Prediction**
```
POST /api/v1/predict
Content-Type: application/json
X-API-Key: {your_key}

Request:
{
  "member_id": "optional-tracking-id",
  "age_at_my_end": 65,
  "has_ckd": 1,
  "has_cvd": 0,
  ...
}

Response (< 100ms):
{
  "prediction": 1,
  "risk_score": 0.73,
  "risk_level": "high",
  "confidence": 0.91,
  "top_risk_factors": [
    {"feature": "has_ckd", "impact": 0.15},
    {"feature": "age_at_my_end", "impact": 0.12}
  ],
  "model_version": "1.0.0",
  "timestamp": "2025-10-22T10:30:00Z"
}
```

**2. Batch Prediction**
```
POST /api/v1/predict/batch
X-API-Key: {your_key}

Request:
{
  "members": [
    {"age_at_my_end": 65, ...},
    {"age_at_my_end": 45, ...}
  ],
  "include_shap": false  // Optional, speeds up response
}

Response:
{
  "predictions": [...],
  "total_processed": 100,
  "high_risk_count": 25,
  "processing_time_ms": 85
}
```

**3. Model Info**
```
GET /api/v1/model/info
X-API-Key: {your_key}

Response:
{
  "model_name": "HEDIS GSD Logistic Regression",
  "version": "1.0.0",
  "performance": {
    "auc_roc": 0.91,
    "sensitivity": 0.87,
    "specificity": 0.81
  },
  "features": [...],
  "hedis_specification": "MY2023 Volume 2"
}
```

**4. Health Checks**
```
GET /health                # Simple up/down
GET /health/ready          # Ready for requests
GET /health/live           # Liveness probe (K8s)
```

#### Nice-to-Have Endpoints (Phase 5):

**5. Feature Validation**
```
POST /api/v1/validate
# Test if features are valid before prediction
```

**6. Batch Status**
```
GET /api/v1/batch/{batch_id}/status
# For async batch processing
```

---

### 3. Authentication Implementation

**Recommended: Simple API Keys**

```python
# middleware/auth.py
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Store keys in environment variable or config
VALID_API_KEYS = {
    "hedis_gsd_pilot_key_001": "Pilot Client",
    "hedis_gsd_test_key_002": "Test Environment"
}

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )
    return VALID_API_KEYS[api_key]
```

**Usage:**
```python
@router.post("/predict")
async def predict(
    request: PredictionRequest,
    client: str = Depends(verify_api_key)
):
    # client = "Pilot Client"
    ...
```

---

### 4. Logging Strategy (HIPAA-Safe)

**What to LOG:**
```python
✅ Request timestamp
✅ Endpoint called
✅ HTTP method
✅ Response status code
✅ Processing time (ms)
✅ API key (hashed)
✅ Aggregate stats (e.g., "10 predictions made")
```

**What NOT to log:**
```python
❌ Request bodies (may contain PHI)
❌ Individual predictions
❌ Member IDs
❌ Feature values
❌ Full error stack traces with data
```

**Recommended Implementation:**
```python
# middleware/logging.py
import logging
from time import time

logger = logging.getLogger("hedis_api")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time()
    
    # Process request
    response = await call_next(request)
    
    # Log aggregate info only
    process_time = (time() - start_time) * 1000
    logger.info(
        f"method={request.method} "
        f"path={request.url.path} "
        f"status={response.status_code} "
        f"duration_ms={process_time:.2f}"
    )
    
    return response
```

---

### 5. Error Handling (User-Friendly)

**Custom Exception Classes:**
```python
class ModelNotLoadedError(Exception):
    """Model artifacts not loaded"""
    pass

class InvalidFeaturesError(Exception):
    """Invalid feature values provided"""
    pass

class BatchTooLargeError(Exception):
    """Batch size exceeds limit"""
    pass
```

**Global Error Handler:**
```python
@app.exception_handler(InvalidFeaturesError)
async def invalid_features_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": "INVALID_FEATURES",
                "message": str(exc),
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    )
```

---

### 6. Performance Optimization

**Target: < 100ms for single prediction**

**Strategies:**

1. **Model Singleton (Critical)**
```python
# Load model ONCE at startup, not per request
from functools import lru_cache

@lru_cache()
def get_model():
    model = joblib.load("models/logistic_regression_final.pkl")
    scaler = joblib.load("models/scaler.pkl")
    return model, scaler
```

2. **Async Endpoints**
```python
# Use async for I/O operations
@router.post("/predict")
async def predict(request: PredictionRequest):
    # Prediction itself is CPU-bound, keep sync
    result = await run_in_threadpool(make_prediction, request)
    return result
```

3. **Batch Optimization**
```python
# Vectorize batch predictions
def predict_batch(features_df):
    # Use pandas/numpy vectorization
    predictions = model.predict_proba(features_df)
    return predictions
```

4. **Response Compression**
```python
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

**Expected Performance:**
- Single prediction: 20-50ms
- Batch (100): 200-500ms
- Batch (1000): 2-5 seconds

---

## 🧪 Testing Strategy

### Test Levels:

**1. Unit Tests (60% of tests)**
```python
tests/api/
├── test_schemas.py         # Pydantic validation
├── test_predictor.py       # Prediction logic
├── test_auth.py            # API key validation
└── test_validators.py      # Feature validation
```

**2. Integration Tests (30% of tests)**
```python
tests/integration/
├── test_endpoints.py       # Full request/response
├── test_error_handling.py  # Error scenarios
└── test_batch_processing.py
```

**3. Performance Tests (10% of tests)**
```python
tests/performance/
├── test_response_time.py   # < 100ms target
├── test_concurrent.py      # 100 concurrent users
└── test_batch_throughput.py
```

### Testing with pytest + httpx:

```python
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_predict_endpoint():
    response = client.post(
        "/api/v1/predict",
        json={"age_at_my_end": 65, "has_ckd": 1, ...},
        headers={"X-API-Key": "test_key"}
    )
    assert response.status_code == 200
    assert "risk_score" in response.json()
    assert response.elapsed.total_seconds() < 0.1  # < 100ms
```

---

## 🚀 Deployment Recommendations

### Phase 3 Deployment (Pilot):

**Recommended: Docker + Cloud Run (Google)**
- ✅ Easiest serverless deployment
- ✅ Auto-scaling
- ✅ Pay per request
- ✅ No infrastructure management

**Alternative: AWS Lambda**
- ✅ Serverless
- ⚠️ Cold start issues with ML models
- ⚠️ Need API Gateway setup

**Alternative: Azure Container Apps**
- ✅ Good for healthcare (HIPAA compliance)
- ✅ Serverless containers
- ✅ Easy scaling

**Phase 4 Deployment (Production):**
- Kubernetes (EKS, GKE, AKS)
- Full CI/CD pipeline
- Blue/green deployments

---

## 📊 Success Metrics for Phase 3

### Functional Requirements ✅
- [ ] Single prediction works (< 100ms)
- [ ] Batch prediction works (> 1000/sec)
- [ ] Model info returns correct data
- [ ] Health checks operational
- [ ] API key authentication works
- [ ] All endpoints return valid JSON

### Performance Requirements ✅
- [ ] P50 latency < 50ms
- [ ] P95 latency < 100ms
- [ ] P99 latency < 200ms
- [ ] Can handle 100 concurrent requests
- [ ] No memory leaks after 10,000 requests

### Quality Requirements ✅
- [ ] 90%+ API test coverage
- [ ] All tests passing
- [ ] OpenAPI docs complete
- [ ] All code reviews passed
- [ ] No linting errors

### Healthcare Compliance ✅
- [ ] No PHI in logs
- [ ] API key authentication working
- [ ] HIPAA-safe error messages
- [ ] Audit logging (request count, timestamps)

---

## 💡 Cursor AI Recommendations for Phase 3

### Use Cursor AI For:

**1. Boilerplate Generation (80% time savings)**
```
Prompt: "Create FastAPI endpoint for batch predictions with Pydantic 
validation, API key auth, and HIPAA-safe logging"
```

**2. Test Generation (70% time savings)**
```
Prompt: "Generate pytest tests for prediction endpoint with valid/invalid 
inputs and performance assertions"
```

**3. Documentation (60% time savings)**
```
Prompt: "Generate OpenAPI documentation for HEDIS prediction API with 
healthcare examples"
```

**4. Error Handling (50% time savings)**
```
Prompt: "Create FastAPI exception handlers for model errors with 
user-friendly messages"
```

### Use Claude Sonnet For:

**1. Code Reviews**
```
Review this API endpoint for HIPAA compliance and security issues
```

**2. Architecture Decisions**
```
Should I use synchronous or asynchronous endpoints for ML predictions?
Explain trade-offs.
```

**3. Performance Optimization**
```
Review this batch processing code and suggest performance improvements
```

### Use ChatGPT-4 For:

**1. API Design Patterns**
```
What are best practices for ML model serving APIs in healthcare?
```

**2. OpenAPI Schema Design**
```
Help me design Pydantic schemas for healthcare prediction API requests
```

**3. Troubleshooting**
```
Why is my FastAPI endpoint returning 422 validation errors?
```

---

## ⏱️ Realistic Timeline with AI Tools

### Week 1 (Days 1-7): Foundation
- **Day 1-2:** FastAPI setup + schemas (Cursor AI: 1 day)
- **Day 3-4:** Prediction endpoints (Cursor AI: 1.5 days)
- **Day 5:** Authentication (Cursor AI: 0.5 days)
- **Day 6-7:** Error handling + middleware (Cursor AI: 1.5 days)

### Week 2 (Days 8-14): Testing & Documentation
- **Day 8-10:** Unit + integration tests (Cursor AI: 2 days)
- **Day 11-12:** Performance testing (Cursor AI: 1.5 days)
- **Day 13:** Documentation (Claude Sonnet: 0.5 days)
- **Day 14:** Code reviews (Claude Sonnet: 0.5 days)

### Week 3 (Days 15-18): Polish & Deploy
- **Day 15-16:** Fix issues from reviews (1.5 days)
- **Day 17:** Deployment setup (Docker) (0.5 days)
- **Day 18:** Final testing + demo (0.5 days)

**Total: 18 days with AI tools vs 30 days traditional**

---

## 🎯 My Specific Recommendations for You

### Priority 1: Start with Production-Lite (Option B)
- ✅ Best balance of features vs complexity
- ✅ Production-ready for pilot
- ✅ Can add database later if needed

### Priority 2: Use FastAPI + API Keys
- ✅ Modern, fast, well-documented
- ✅ Simple auth for pilot
- ✅ Easy to upgrade later

### Priority 3: Skip Database for Now
- ✅ Faster development
- ✅ Less infrastructure
- ✅ Add in Phase 5 when needed

### Priority 4: Leverage Cursor AI Heavily
- ✅ Generate boilerplate endpoints
- ✅ Create comprehensive tests
- ✅ Generate OpenAPI docs
- ✅ Use Claude for code reviews

### Priority 5: Focus on Performance
- ✅ < 100ms is achievable
- ✅ Will differentiate your API
- ✅ Good for healthcare use cases

---

## 📞 Decision Points & My Suggestions

| Decision | Options | My Recommendation | Why |
|----------|---------|-------------------|-----|
| **Framework** | FastAPI vs Flask | ✅ FastAPI | Faster, modern, auto-docs |
| **Auth** | API Keys vs OAuth2 | ✅ API Keys | Simpler, sufficient for pilot |
| **Database** | PostgreSQL vs None | ✅ None (now) | Add in Phase 5 |
| **Caching** | Redis vs None | ✅ None (now) | Not needed yet |
| **Deployment** | Cloud Run vs Lambda | ✅ Cloud Run | Easier for ML models |
| **Rate Limiting** | Now vs Phase 4 | ✅ Now | Simple with FastAPI |
| **Async** | Sync vs Async | ✅ Sync (mostly) | Simpler, sufficient |

---

## 🚀 Ready to Start?

**Recommended First Steps:**

1. **Day 1 Morning:** Review this document, make final decisions
2. **Day 1 Afternoon:** Set up FastAPI project structure (Cursor AI)
3. **Day 2:** Create schemas and prediction endpoint (Cursor AI)
4. **Day 3:** Test prediction endpoint, verify performance
5. **Day 4:** Add authentication and batch endpoint

**By end of Week 1:** Working API with core endpoints! 🎉

---

**Questions to Answer Before Starting:**

1. Do you want API key authentication or skip auth for now?
   - **My Rec:** Add API keys (30 min with Cursor AI)

2. What cloud provider do you prefer?
   - **My Rec:** Google Cloud Run (easiest) or AWS (most common)

3. Maximum batch size for predictions?
   - **My Rec:** 1000 individuals per request

4. Do you want SHAP values in every response or optional?
   - **My Rec:** Optional (faster without SHAP)

---

**Created:** October 21, 2025  
**Next Action:** Review recommendations → Start Phase 3 implementation  
**Support:** Use Cursor AI + Claude Sonnet for 60% faster development



---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
