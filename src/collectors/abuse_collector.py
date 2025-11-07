"""Abuse.ch threat intelligence collectors (MalwareBazaar, URLhaus)"""

import os
import requests
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AbuseCollector:
    """Collect IOCs from Abuse.ch feeds (MalwareBazaar, URLhaus)"""
    
    def __init__(self):
        """Initialize Abuse.ch collector."""
        self.malwarebazaar_url = 'https://mb-api.abuse.ch/api/v1'
        self.urlhaus_url = 'https://urlhaus-api.abuse.ch/v1'
        self.session = requests.Session()
    
    def collect_malwarebazaar(self, limit: int = 100) -> List[Dict]:
        """
        Collect malware samples from MalwareBazaar.
        
        Args:
            limit: Maximum number of samples to retrieve
            
        Returns:
            List of normalized IOC dictionaries
        """
        iocs = []
        
        try:
            # Get recent samples
            url = f"{self.malwarebazaar_url}/get"
            params = {'query': 'get_recent', 'selector': limit}
            
            response = self.session.post(url, data=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            samples = data.get('data', [])
            
            for sample in samples:
                # Extract hashes
                sha256 = sample.get('sha256_hash', '')
                md5 = sample.get('md5_hash', '')
                sha1 = sample.get('sha1_hash', '')
                
                # Primary IOC is SHA256
                if sha256:
                    ioc = {
                        'ioc_value': sha256,
                        'ioc_type': 'hash',
                        'source': 'abuse_ch_malwarebazaar',
                        'threat_type': 'malware',
                        'first_seen': sample.get('first_seen', ''),
                        'last_seen': sample.get('last_seen', ''),
                        'confidence': 0.95,
                        'tags': sample.get('tags', []),
                        'signature': sample.get('signature', ''),
                        'file_type': sample.get('file_type', ''),
                        'file_size': sample.get('file_size', ''),
                        'related_hashes': {
                            'md5': md5,
                            'sha1': sha1
                        }
                    }
                    iocs.append(ioc)
                
                # Also add MD5 and SHA1 as separate IOCs
                for hash_value, hash_type in [(md5, 'md5'), (sha1, 'sha1')]:
                    if hash_value:
                        ioc = {
                            'ioc_value': hash_value,
                            'ioc_type': 'hash',
                            'source': 'abuse_ch_malwarebazaar',
                            'threat_type': 'malware',
                            'first_seen': sample.get('first_seen', ''),
                            'confidence': 0.95,
                            'related_hashes': {'sha256': sha256}
                        }
                        iocs.append(ioc)
                        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching MalwareBazaar data: {e}")
        
        logger.info(f"Collected {len(iocs)} IOCs from MalwareBazaar")
        return iocs
    
    def collect_urlhaus(self, limit: int = 100) -> List[Dict]:
        """
        Collect malicious URLs from URLhaus.
        
        Args:
            limit: Maximum number of URLs to retrieve
            
        Returns:
            List of normalized IOC dictionaries
        """
        iocs = []
        
        try:
            # Get recent URLs
            url = f"{self.urlhaus_url}/urls/recent/limit/{limit}/"
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            urls_data = data.get('urls', [])
            
            for url_entry in urls_data:
                url_value = url_entry.get('url', '')
                if not url_value:
                    continue
                
                # Extract domain from URL
                from urllib.parse import urlparse
                parsed = urlparse(url_value)
                domain = parsed.netloc
                
                # Create URL IOC
                url_ioc = {
                    'ioc_value': url_value,
                    'ioc_type': 'url',
                    'source': 'abuse_ch_urlhaus',
                    'threat_type': 'malware_distribution',
                    'first_seen': url_entry.get('date_added', ''),
                    'last_seen': url_entry.get('lastseen', ''),
                    'confidence': 0.90,
                    'status': url_entry.get('url_status', ''),
                    'tags': url_entry.get('tags', []),
                    'threat': url_entry.get('threat', ''),
                    'related_domain': domain
                }
                iocs.append(url_ioc)
                
                # Also add domain as separate IOC if it's different
                if domain and domain not in url_value:
                    domain_ioc = {
                        'ioc_value': domain,
                        'ioc_type': 'domain',
                        'source': 'abuse_ch_urlhaus',
                        'threat_type': 'malware_distribution',
                        'first_seen': url_entry.get('date_added', ''),
                        'confidence': 0.85,
                        'related_urls': [url_value]
                    }
                    iocs.append(domain_ioc)
                    
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching URLhaus data: {e}")
        
        logger.info(f"Collected {len(iocs)} IOCs from URLhaus")
        return iocs
    
    def collect_all(self, limit: int = 100) -> List[Dict]:
        """
        Collect all IOCs from Abuse.ch feeds.
        
        Args:
            limit: Maximum number of IOCs per feed
            
        Returns:
            List of normalized IOC dictionaries
        """
        all_iocs = []
        
        # Collect from MalwareBazaar
        malware_iocs = self.collect_malwarebazaar(limit=limit)
        all_iocs.extend(malware_iocs)
        
        # Collect from URLhaus
        url_iocs = self.collect_urlhaus(limit=limit)
        all_iocs.extend(url_iocs)
        
        logger.info(f"Collected total {len(all_iocs)} IOCs from Abuse.ch")
        return all_iocs

