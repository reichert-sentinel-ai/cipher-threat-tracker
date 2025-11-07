"""AlienVault OTX (Open Threat Exchange) IOC collector"""

import os
import requests
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class OTXCollector:
    """Collect IOCs from AlienVault OTX"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OTX collector.
        
        Args:
            api_key: OTX API key (defaults to OTX_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('OTX_API_KEY', '')
        self.base_url = 'https://otx.alienvault.com/api/v1'
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({'X-OTX-API-KEY': self.api_key})
    
    def get_all_pulses(self, limit: int = 100) -> List[Dict]:
        """
        Get all pulses (threat intelligence reports) from OTX.
        
        Args:
            limit: Maximum number of pulses to retrieve
            
        Returns:
            List of pulse dictionaries
        """
        pulses = []
        page = 1
        
        try:
            while len(pulses) < limit:
                url = f"{self.base_url}/pulses/subscribed"
                params = {'page': page, 'page_size': 50}
                
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                results = data.get('results', [])
                
                if not results:
                    break
                
                pulses.extend(results)
                page += 1
                
                if len(pulses) >= limit:
                    break
                    
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching OTX pulses: {e}")
            
        return pulses[:limit]
    
    def extract_iocs(self, pulses: List[Dict]) -> List[Dict]:
        """
        Extract IOCs from pulses.
        
        Args:
            pulses: List of pulse dictionaries
            
        Returns:
            List of normalized IOC dictionaries
        """
        iocs = []
        
        for pulse in pulses:
            pulse_id = pulse.get('id', '')
            pulse_name = pulse.get('name', '')
            created = pulse.get('created', '')
            
            # Extract indicators from pulse
            indicators = pulse.get('indicators', [])
            
            for indicator in indicators:
                ioc_type = indicator.get('type', '').lower()
                ioc_value = indicator.get('indicator', '')
                
                if not ioc_value:
                    continue
                
                # Normalize IOC
                normalized = {
                    'ioc_value': ioc_value,
                    'ioc_type': self._normalize_ioc_type(ioc_type),
                    'source': 'otx',
                    'source_id': pulse_id,
                    'source_name': pulse_name,
                    'threat_type': self._classify_threat_type(ioc_type),
                    'first_seen': created,
                    'last_seen': indicator.get('created', created),
                    'confidence': pulse.get('tlp', 'white'),
                    'tags': pulse.get('tags', []),
                    'description': pulse.get('description', ''),
                    'references': pulse.get('references', [])
                }
                
                iocs.append(normalized)
        
        return iocs
    
    def collect_all(self, limit: int = 100) -> List[Dict]:
        """
        Collect all IOCs from OTX.
        
        Args:
            limit: Maximum number of pulses to process
            
        Returns:
            List of normalized IOC dictionaries
        """
        pulses = self.get_all_pulses(limit=limit)
        iocs = self.extract_iocs(pulses)
        
        logger.info(f"Collected {len(iocs)} IOCs from OTX")
        return iocs
    
    @staticmethod
    def _normalize_ioc_type(ioc_type: str) -> str:
        """Normalize IOC type to standard format."""
        type_map = {
            'ipv4': 'ip',
            'ipv6': 'ip',
            'url': 'url',
            'domain': 'domain',
            'hostname': 'domain',
            'filehash-md5': 'hash',
            'filehash-sha1': 'hash',
            'filehash-sha256': 'hash',
            'email': 'email',
            'cidr': 'ip_range'
        }
        return type_map.get(ioc_type.lower(), ioc_type.lower())
    
    @staticmethod
    def _classify_threat_type(ioc_type: str) -> str:
        """Classify threat type based on IOC type."""
        if ioc_type in ['filehash-md5', 'filehash-sha1', 'filehash-sha256']:
            return 'malware'
        elif ioc_type in ['url', 'domain']:
            return 'phishing'
        elif ioc_type in ['ipv4', 'ipv6']:
            return 'c2_server'
        else:
            return 'unknown'

