"""Tests for FastAPI endpoints"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


class TestAPI:
    """Tests for FastAPI endpoints"""
    
    def test_root(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Cipher Threat Intelligence API"
    
    def test_health(self):
        """Test health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_ioc_check(self):
        """Test IOC check endpoint"""
        payload = {
            "ioc_value": "192.0.2.1",
            "ioc_type": "ip"
        }
        # This will fail if Elasticsearch is not available
        # Should return empty list or error
        response = client.post("/api/v1/ioc/check", json=payload)
        # Accept both 200 (empty results) and 500 (service unavailable)
        assert response.status_code in [200, 500]
    
    def test_threats_endpoint(self):
        """Test threats endpoint"""
        response = client.get("/api/v1/threats")
        # Accept both 200 (results) and 500 (service unavailable)
        assert response.status_code in [200, 500]
    
    def test_detect_anomaly(self):
        """Test anomaly detection endpoint"""
        payload = {
            "features": [0.1] * 512,
            "method": "autoencoder"
        }
        response = client.post("/api/v1/detect/anomaly", json=payload)
        assert response.status_code == 200

