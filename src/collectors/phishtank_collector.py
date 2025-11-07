"""PhishTank phishing URL collector"""

import os
import requests
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PhishTankCollector:
    """Collect phishing URLs from PhishTank"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize PhishTank collector.
        
        Args:
            api_key: PhishTank API key (optional for public feeds)
        """
        self.api_key = api_key or os.getenv('PHISHTANK_API_KEY', '')
        self.base_url = 'http://data.phishtank.com'
        self.session = requests.Session()
    
    def collect_online_urls(self, limit: int = 100) -> List[Dict]:
        """
        Collect currently online phishing URLs from PhishTank.
        
        Args:
            limit: Maximum number of URLs to retrieve
            
        Returns:
            List of normalized IOC dictionaries
        """
        iocs = []
        
        try:
            # Use public feed (no API key required)
            url = f"{self.base_url}/data/online-valid.json"
            
            response = self.session.get(url, timeout=60)  # Large file, longer timeout
            response.raise_for_status()
            
            data = response.json()
            phish_entries = data if isinstance(data, list) else data.get('phishes', [])
            
            for entry in phish_entries[:limit]:
                phish_url = entry.get('url', '')
                if not phish_url:
                    continue
                
                # Extract domain from URL
                from urllib.parse import urlparse
                parsed = urlparse(phish_url)
                domain = parsed.netloc
                
                # Create URL IOC
                url_ioc = {
                    'ioc_value': phish_url,
                    'ioc_type': 'url',
                    'source': 'phishtank',
                    'threat_type': 'phishing',
                    'first_seen': entry.get('submission_time', ''),
                    'last_seen': entry.get('verification_time', ''),
                    'confidence': 0.95 if entry.get('verified', 'yes') == 'yes' else 0.70,
                    'verified': entry.get('verified', 'no'),
                    'phish_id': entry.get('phish_id', ''),
                    'phish_detail_url': entry.get('phish_detail_url', ''),
                    'target': entry.get('target', ''),
                    'related_domain': domain
                }
                iocs.append(url_ioc)
                
                # Also add domain as separate IOC
                if domain:
                    domain_ioc = {
                        'ioc_value': domain,
                        'ioc_type': 'domain',
                        'source': 'phishtank',
                        'threat_type': 'phishing',
                        'first_seen': entry.get('submission_time', ''),
                        'confidence': 0.90 if entry.get('verified', 'yes') == 'yes' else 0.65,
                        'related_urls': [phish_url]
                    }
                    iocs.append(domain_ioc)
                    
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching PhishTank data: {e}")
        
        logger.info(f"Collected {len(iocs)} IOCs from PhishTank")
        return iocs
    
    def collect_all(self, limit: int = 100) -> List[Dict]:
        """
        Collect all phishing URLs from PhishTank.
        
        Args:
            limit: Maximum number of URLs to retrieve
            
        Returns:
            List of normalized IOC dictionaries
        """
        iocs = self.collect_online_urls(limit=limit)
        return iocs

