"""Tests for IOC collectors"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.collectors.otx_collector import OTXCollector
from src.collectors.abuse_collector import AbuseCollector
from src.collectors.phishtank_collector import PhishTankCollector
from src.collectors.nvd_collector import NVDCollector
from src.collectors.base_collector import BaseCollector, IOCDeduplicator


class TestBaseCollector:
    """Tests for BaseCollector"""
    
    def test_normalize_ioc(self):
        """Test IOC normalization"""
        collector = BaseCollector()
        
        ioc = {
            'ioc_value': '192.0.2.1',
            'ioc_type': 'ip',
            'source': 'test',
            'threat_type': 'malware',
            'confidence': 0.9
        }
        
        normalized = collector.normalize_ioc(ioc)
        
        assert normalized['ioc_value'] == '192.0.2.1'
        assert normalized['ioc_type'] == 'ip'
        assert 'ioc_id' in normalized
        assert normalized['confidence'] == 0.9
    
    def test_normalize_type(self):
        """Test IOC type normalization"""
        collector = BaseCollector()
        
        assert collector._normalize_type('ipv4') == 'ip'
        assert collector._normalize_type('url') == 'url'
        assert collector._normalize_type('domain') == 'domain'
        assert collector._normalize_type('hash') == 'hash'


class TestIOCDeduplicator:
    """Tests for IOCDeduplicator"""
    
    def test_deduplicate(self):
        """Test IOC deduplication"""
        deduplicator = IOCDeduplicator()
        
        ioc1 = {
            'ioc_id': 'test_id_1',
            'ioc_value': '192.0.2.1',
            'ioc_type': 'ip',
            'source': 'source1',
            'confidence': 0.8
        }
        
        ioc2 = {
            'ioc_id': 'test_id_1',  # Same ID
            'ioc_value': '192.0.2.1',
            'ioc_type': 'ip',
            'source': 'source2',
            'confidence': 0.9
        }
        
        ioc3 = {
            'ioc_id': 'test_id_2',
            'ioc_value': '192.0.2.2',
            'ioc_type': 'ip',
            'source': 'source1',
            'confidence': 0.7
        }
        
        iocs = [ioc1, ioc2, ioc3]
        deduplicated = deduplicator.deduplicate(iocs)
        
        assert len(deduplicated) == 2
        assert deduplicated[0]['confidence'] == 0.9  # Max confidence


class TestOTXCollector:
    """Tests for OTXCollector"""
    
    @patch('src.collectors.otx_collector.requests.Session')
    def test_collect_all(self, mock_session):
        """Test OTX collection"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            'results': [
                {
                    'id': 'pulse_1',
                    'name': 'Test Pulse',
                    'indicators': [
                        {
                            'indicator': '192.0.2.1',
                            'type': 'IPv4',
                            'created': '2024-01-01T00:00:00Z'
                        }
                    ],
                    'created': '2024-01-01T00:00:00Z',
                    'tags': ['malware']
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_session.return_value.get.return_value = mock_response
        
        collector = OTXCollector()
        iocs = collector.collect_all(limit=1)
        
        assert len(iocs) > 0
        assert iocs[0]['ioc_type'] in ['ip', 'url', 'domain', 'hash']


class TestAbuseCollector:
    """Tests for AbuseCollector"""
    
    @patch('src.collectors.abuse_collector.requests.Session')
    def test_collect_malwarebazaar(self, mock_session):
        """Test MalwareBazaar collection"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': [
                {
                    'sha256_hash': 'test_hash_256',
                    'md5_hash': 'test_hash_md5',
                    'first_seen': '2024-01-01T00:00:00Z'
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_session.return_value.post.return_value = mock_response
        
        collector = AbuseCollector()
        iocs = collector.collect_malwarebazaar(limit=1)
        
        assert len(iocs) > 0


class TestPhishTankCollector:
    """Tests for PhishTankCollector"""
    
    @patch('src.collectors.phishtank_collector.requests.Session')
    def test_collect_online_urls(self, mock_session):
        """Test PhishTank collection"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                'url': 'http://phishing.example.com',
                'phish_id': '12345',
                'verified': 'yes',
                'submission_time': '2024-01-01T00:00:00Z'
            }
        ]
        mock_response.raise_for_status = Mock()
        mock_session.return_value.get.return_value = mock_response
        
        collector = PhishTankCollector()
        iocs = collector.collect_online_urls(limit=1)
        
        assert len(iocs) > 0
        assert any(ioc['ioc_type'] == 'url' for ioc in iocs)

