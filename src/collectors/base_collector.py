"""Base collector class and IOC normalizer"""

from typing import List, Dict, Any
from datetime import datetime
import hashlib
import re
import logging

logger = logging.getLogger(__name__)


class BaseCollector:
    """Base class for all IOC collectors"""
    
    def normalize_ioc(self, ioc: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize IOC to standard format.
        
        Args:
            ioc: Raw IOC dictionary
            
        Returns:
            Normalized IOC dictionary
        """
        normalized = {
            'ioc_value': str(ioc.get('ioc_value', '')).strip(),
            'ioc_type': self._normalize_type(ioc.get('ioc_type', 'unknown')),
            'source': ioc.get('source', 'unknown'),
            'threat_type': ioc.get('threat_type', 'unknown'),
            'first_seen': self._normalize_timestamp(ioc.get('first_seen', '')),
            'last_seen': self._normalize_timestamp(ioc.get('last_seen', ioc.get('first_seen', ''))),
            'confidence': float(ioc.get('confidence', 0.5)),
            'tags': self._normalize_tags(ioc.get('tags', [])),
            'metadata': {k: v for k, v in ioc.items() 
                        if k not in ['ioc_value', 'ioc_type', 'source', 'threat_type', 
                                   'first_seen', 'last_seen', 'confidence', 'tags']}
        }
        
        # Generate unique ID for deduplication
        normalized['ioc_id'] = self._generate_ioc_id(normalized)
        
        return normalized
    
    def _normalize_type(self, ioc_type: str) -> str:
        """Normalize IOC type to standard format."""
        type_map = {
            'ipv4': 'ip',
            'ipv6': 'ip',
            'ip': 'ip',
            'url': 'url',
            'domain': 'domain',
            'hostname': 'domain',
            'hash': 'hash',
            'md5': 'hash',
            'sha1': 'hash',
            'sha256': 'hash',
            'filehash-md5': 'hash',
            'filehash-sha1': 'hash',
            'filehash-sha256': 'hash',
            'email': 'email',
            'cidr': 'ip_range',
            'cve': 'cve'
        }
        return type_map.get(ioc_type.lower(), ioc_type.lower())
    
    def _normalize_timestamp(self, timestamp: Any) -> str:
        """Normalize timestamp to ISO 8601 format."""
        if not timestamp:
            return datetime.utcnow().isoformat() + 'Z'
        
        if isinstance(timestamp, datetime):
            return timestamp.isoformat() + 'Z'
        
        if isinstance(timestamp, str):
            # Try to parse various formats
            try:
                # ISO format
                if 'T' in timestamp or 'Z' in timestamp:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    return dt.isoformat() + 'Z'
                # Common date formats
                for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%m/%d/%Y']:
                    try:
                        dt = datetime.strptime(timestamp, fmt)
                        return dt.isoformat() + 'Z'
                    except ValueError:
                        continue
            except Exception:
                pass
        
        return datetime.utcnow().isoformat() + 'Z'
    
    def _normalize_tags(self, tags: Any) -> List[str]:
        """Normalize tags to list of strings."""
        if isinstance(tags, list):
            return [str(tag).lower().strip() for tag in tags if tag]
        elif isinstance(tags, str):
            return [tag.strip() for tag in tags.split(',') if tag.strip()]
        else:
            return []
    
    def _generate_ioc_id(self, ioc: Dict[str, Any]) -> str:
        """
        Generate unique ID for IOC based on value and type.
        Used for deduplication.
        
        Args:
            ioc: Normalized IOC dictionary
            
        Returns:
            SHA256 hash of IOC value and type
        """
        value = str(ioc.get('ioc_value', '')).lower().strip()
        ioc_type = str(ioc.get('ioc_type', '')).lower()
        
        # For IPs, normalize
        if ioc_type == 'ip':
            value = self._normalize_ip(value)
        # For URLs, normalize
        elif ioc_type == 'url':
            value = self._normalize_url(value)
        # For domains, normalize
        elif ioc_type == 'domain':
            value = self._normalize_domain(value)
        # For hashes, normalize case
        elif ioc_type == 'hash':
            value = value.lower()
        
        content = f"{ioc_type}:{value}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    @staticmethod
    def _normalize_ip(ip: str) -> str:
        """Normalize IP address."""
        # Remove whitespace
        ip = ip.strip()
        # Handle IPv6
        if ':' in ip:
            # Normalize IPv6 (simplified)
            return ip.lower()
        # IPv4 - just ensure it's valid format
        parts = ip.split('.')
        if len(parts) == 4:
            try:
                return '.'.join(str(int(p)) for p in parts)
            except ValueError:
                return ip
        return ip
    
    @staticmethod
    def _normalize_url(url: str) -> str:
        """Normalize URL."""
        url = url.strip().lower()
        # Remove protocol if present
        url = re.sub(r'^https?://', '', url)
        # Remove trailing slash
        url = url.rstrip('/')
        return url
    
    @staticmethod
    def _normalize_domain(domain: str) -> str:
        """Normalize domain name."""
        domain = domain.strip().lower()
        # Remove protocol if present
        domain = re.sub(r'^https?://', '', domain)
        # Remove path
        domain = domain.split('/')[0]
        # Remove port
        domain = domain.split(':')[0]
        # Remove www. prefix for normalization
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain


class IOCDeduplicator:
    """Deduplicate IOCs across sources"""
    
    def __init__(self):
        """Initialize deduplicator."""
        self.seen_iocs = {}
    
    def deduplicate(self, iocs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Deduplicate IOCs, keeping highest confidence and merging metadata.
        
        Args:
            iocs: List of normalized IOC dictionaries
            
        Returns:
            Deduplicated list of IOC dictionaries
        """
        seen = {}
        
        for ioc in iocs:
            ioc_id = ioc.get('ioc_id', '')
            
            if not ioc_id:
                continue
            
            if ioc_id not in seen:
                seen[ioc_id] = ioc.copy()
            else:
                # Merge: keep highest confidence, combine sources
                existing = seen[ioc_id]
                
                # Update confidence to max
                existing['confidence'] = max(existing.get('confidence', 0), ioc.get('confidence', 0))
                
                # Merge sources
                sources = set([existing.get('source', ''), ioc.get('source', '')])
                existing['metadata']['all_sources'] = list(sources)
                
                # Merge tags
                all_tags = set(existing.get('tags', []) + ioc.get('tags', []))
                existing['tags'] = list(all_tags)
                
                # Update timestamps (earliest first_seen, latest last_seen)
                if ioc.get('first_seen', '') < existing.get('first_seen', ''):
                    existing['first_seen'] = ioc.get('first_seen', '')
                if ioc.get('last_seen', '') > existing.get('last_seen', ''):
                    existing['last_seen'] = ioc.get('last_seen', '')
                
                # Merge metadata
                for key, value in ioc.get('metadata', {}).items():
                    if key not in existing.get('metadata', {}):
                        existing['metadata'][key] = value
        
        return list(seen.values())

