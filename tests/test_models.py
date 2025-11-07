"""Tests for ML models"""

import pytest
import numpy as np
import torch
from src.models.autoencoder import TrafficAutoencoder, AutoencoderTrainer, AnomalyDetector
from src.models.anomaly_detector import IsolationForestDetector, BehavioralAnomalyDetector
from src.models.ioc_classifier import IOCClassifier
from src.models.correlation_engine import ThreatCorrelationEngine


class TestTrafficAutoencoder:
    """Tests for TrafficAutoencoder"""
    
    def test_forward(self):
        """Test forward pass"""
        model = TrafficAutoencoder(input_dim=512, encoding_dim=128)
        
        x = torch.randn(10, 512)
        output = model(x)
        
        assert output.shape == (10, 512)
    
    def test_encode(self):
        """Test encoding"""
        model = TrafficAutoencoder(input_dim=512, encoding_dim=128)
        
        x = torch.randn(10, 512)
        encoded = model.encode(x)
        
        assert encoded.shape == (10, 128)


class TestAnomalyDetector:
    """Tests for AnomalyDetector"""
    
    def test_fit_threshold(self):
        """Test threshold fitting"""
        model = TrafficAutoencoder(input_dim=512, encoding_dim=128)
        detector = AnomalyDetector(model, threshold_percentile=95.0)
        
        normal_data = torch.randn(100, 512)
        detector.fit_threshold(normal_data)
        
        assert detector.threshold is not None
    
    def test_detect(self):
        """Test anomaly detection"""
        model = TrafficAutoencoder(input_dim=512, encoding_dim=128)
        detector = AnomalyDetector(model, threshold_percentile=95.0)
        
        normal_data = torch.randn(100, 512)
        detector.fit_threshold(normal_data)
        
        test_data = torch.randn(10, 512)
        is_anomaly, scores = detector.detect(test_data)
        
        assert len(is_anomaly) == 10
        assert len(scores) == 10


class TestIsolationForestDetector:
    """Tests for IsolationForestDetector"""
    
    def test_fit_predict(self):
        """Test fit and predict"""
        detector = IsolationForestDetector(contamination=0.05)
        
        X = np.random.randn(100, 10)
        is_anomaly, scores = detector.fit_predict(X)
        
        assert len(is_anomaly) == 100
        assert len(scores) == 100


class TestIOCClassifier:
    """Tests for IOCClassifier"""
    
    def test_extract_features(self):
        """Test feature extraction"""
        classifier = IOCClassifier()
        
        iocs = [
            {
                'ioc_value': '192.0.2.1',
                'ioc_type': 'ip',
                'source': 'test',
                'threat_type': 'malware',
                'confidence': 0.9,
                'tags': ['malware']
            }
        ]
        
        X, y = classifier.extract_features(iocs)
        
        assert len(X) == 1
        assert len(y) == 1
        assert y[0] == 'malware'


class TestThreatCorrelationEngine:
    """Tests for ThreatCorrelationEngine"""
    
    def test_correlate_iocs(self):
        """Test IOC correlation"""
        engine = ThreatCorrelationEngine(time_window_hours=24, similarity_threshold=0.7)
        
        iocs = [
            {
                'ioc_id': 'id1',
                'ioc_value': '192.0.2.1',
                'ioc_type': 'ip',
                'source': 'test1',
                'threat_type': 'malware',
                'first_seen': '2024-01-01T00:00:00Z',
                'tags': ['malware']
            },
            {
                'ioc_id': 'id2',
                'ioc_value': '192.0.2.2',
                'ioc_type': 'ip',
                'source': 'test1',
                'threat_type': 'malware',
                'first_seen': '2024-01-01T01:00:00Z',
                'tags': ['malware']
            }
        ]
        
        correlated_iocs, campaigns = engine.correlate_iocs(iocs)
        
        assert len(correlated_iocs) == 2
        assert isinstance(campaigns, dict)

