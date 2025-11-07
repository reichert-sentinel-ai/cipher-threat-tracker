"""NVD (National Vulnerability Database) CVE collector"""

import os
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging
import time

logger = logging.getLogger(__name__)


class NVDCollector:
    """Collect CVEs from NIST NVD"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize NVD collector.
        
        Args:
            api_key: NVD API key (optional, improves rate limits)
        """
        self.api_key = api_key or os.getenv('NVD_API_KEY', '')
        self.base_url = 'https://services.nvd.nist.gov/rest/json'
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({'apiKey': self.api_key})
    
    def collect_recent_cves(self, days: int = 7, limit: int = 100) -> List[Dict]:
        """
        Collect recent CVEs from NVD.
        
        Args:
            days: Number of days to look back
            limit: Maximum number of CVEs to retrieve
            
        Returns:
            List of normalized CVE dictionaries
        """
        iocs = []
        
        try:
            # Calculate date range
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            start_date_str = start_date.strftime('%Y-%m-%dT00:00:00.000')
            end_date_str = end_date.strftime('%Y-%m-%dT23:59:59.999')
            
            # NVD API v2.0
            url = f"{self.base_url}/cves/2.0"
            params = {
                'pubStartDate': start_date_str,
                'pubEndDate': end_date_str,
                'resultsPerPage': min(limit, 2000)  # Max 2000 per request
            }
            
            # Rate limiting: NVD allows 5 requests per 30 seconds without API key
            # With API key: 50 requests per 30 seconds
            response = self.session.get(url, params=params, timeout=60)
            
            # Handle rate limiting
            if response.status_code == 429:
                logger.warning("NVD rate limit hit, waiting 30 seconds...")
                time.sleep(30)
                response = self.session.get(url, params=params, timeout=60)
            
            response.raise_for_status()
            data = response.json()
            
            vulnerabilities = data.get('vulnerabilities', [])
            
            for vuln_entry in vulnerabilities[:limit]:
                cve_data = vuln_entry.get('cve', {})
                cve_id = cve_data.get('id', '')
                
                if not cve_id:
                    continue
                
                # Extract CVSS scores
                metrics = cve_data.get('metrics', {})
                cvss_v3 = metrics.get('cvssMetricV31', [{}])[0] if metrics.get('cvssMetricV31') else {}
                cvss_v2 = metrics.get('cvssMetricV2', [{}])[0] if metrics.get('cvssMetricV2') else {}
                
                base_score_v3 = cvss_v3.get('cvssData', {}).get('baseScore', 0.0)
                base_score_v2 = cvss_v2.get('cvssData', {}).get('baseScore', 0.0)
                base_score = base_score_v3 or base_score_v2 or 0.0
                
                # Classify threat type based on CVSS score
                threat_type = 'high_risk' if base_score >= 7.0 else 'medium_risk' if base_score >= 4.0 else 'low_risk'
                
                # Extract descriptions
                descriptions = cve_data.get('descriptions', [])
                description = ''
                for desc in descriptions:
                    if desc.get('lang', 'en') == 'en':
                        description = desc.get('value', '')
                        break
                
                # Extract affected products
                configurations = cve_data.get('configurations', [])
                affected_products = []
                for config in configurations:
                    nodes = config.get('nodes', [])
                    for node in nodes:
                        cpe_match = node.get('cpeMatch', [])
                        for match in cpe_match:
                            criteria = match.get('criteria', '')
                            if criteria:
                                affected_products.append(criteria)
                
                ioc = {
                    'ioc_value': cve_id,
                    'ioc_type': 'cve',
                    'source': 'nvd',
                    'threat_type': threat_type,
                    'first_seen': cve_data.get('published', ''),
                    'last_seen': cve_data.get('lastModified', ''),
                    'confidence': min(base_score / 10.0, 1.0) if base_score > 0 else 0.5,
                    'cvss_score': base_score,
                    'cvss_severity': cvss_v3.get('cvssData', {}).get('baseSeverity', 'MEDIUM'),
                    'description': description,
                    'affected_products': affected_products[:10],  # Limit to first 10
                    'tags': ['vulnerability', 'cve'],
                    'references': [ref.get('url', '') for ref in cve_data.get('references', [])][:5]
                }
                
                iocs.append(ioc)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching NVD data: {e}")
        except Exception as e:
            logger.error(f"Unexpected error processing NVD data: {e}")
        
        logger.info(f"Collected {len(iocs)} CVEs from NVD")
        return iocs
    
    def collect_all(self, days: int = 7, limit: int = 100) -> List[Dict]:
        """
        Collect all CVEs from NVD.
        
        Args:
            days: Number of days to look back
            limit: Maximum number of CVEs to retrieve
            
        Returns:
            List of normalized CVE dictionaries
        """
        iocs = self.collect_recent_cves(days=days, limit=limit)
        return iocs

