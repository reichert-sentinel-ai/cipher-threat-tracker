"""Elasticsearch integration for IOC indexing"""

import os
from typing import List, Dict, Optional
from datetime import datetime
import logging

try:
    from elasticsearch import Elasticsearch
    from elasticsearch.helpers import bulk
    ELASTICSEARCH_AVAILABLE = True
except ImportError:
    ELASTICSEARCH_AVAILABLE = False
    logging.warning("Elasticsearch not available. Install with: pip install elasticsearch")

logger = logging.getLogger(__name__)


class ElasticsearchClient:
    """Elasticsearch client for IOC indexing"""
    
    def __init__(self, 
                 host: Optional[str] = None,
                 port: int = 9200,
                 username: Optional[str] = None,
                 password: Optional[str] = None):
        """
        Initialize Elasticsearch client.
        
        Args:
            host: Elasticsearch host (defaults to ELASTICSEARCH_HOST env var or localhost)
            port: Elasticsearch port
            username: Username (optional)
            password: Password (optional)
        """
        if not ELASTICSEARCH_AVAILABLE:
            raise ImportError("Elasticsearch not installed. Install with: pip install elasticsearch")
        
        host = host or os.getenv('ELASTICSEARCH_HOST', 'localhost')
        
        # Build connection config
        config = {
            'hosts': [f"{host}:{port}"],
            'timeout': 30
        }
        
        if username or password:
            config['http_auth'] = (username or os.getenv('ELASTICSEARCH_USER', ''),
                                  password or os.getenv('ELASTICSEARCH_PASSWORD', ''))
        
        self.client = Elasticsearch(**config)
        self.index_name = 'iocs'
    
    def create_index(self, force: bool = False):
        """
        Create IOC index with proper mapping.
        
        Args:
            force: Force recreate if index exists
        """
        if self.client.indices.exists(index=self.index_name):
            if force:
                logger.warning(f"Deleting existing index: {self.index_name}")
                self.client.indices.delete(index=self.index_name)
            else:
                logger.info(f"Index {self.index_name} already exists")
                return
        
        # Define index mapping
        mapping = {
            "mappings": {
                "properties": {
                    "ioc_value": {"type": "keyword"},
                    "ioc_type": {"type": "keyword"},
                    "ioc_id": {"type": "keyword"},
                    "source": {"type": "keyword"},
                    "threat_type": {"type": "keyword"},
                    "first_seen": {"type": "date"},
                    "last_seen": {"type": "date"},
                    "confidence": {"type": "float"},
                    "tags": {"type": "keyword"},
                    "metadata": {"type": "object", "enabled": True},
                    "mitre_tactics": {"type": "keyword"},
                    "threat_actors": {"type": "keyword"},
                    "related_iocs": {"type": "keyword"}
                }
            },
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "refresh_interval": "5s"
            }
        }
        
        try:
            # Elasticsearch 8.x supports both body parameter and direct mapping
            self.client.indices.create(index=self.index_name, body=mapping)
            logger.info(f"Created index: {self.index_name}")
        except Exception as e:
            logger.error(f"Error creating index: {e}")
            raise
    
    def index_ioc(self, ioc: Dict) -> bool:
        """
        Index a single IOC.
        
        Args:
            ioc: IOC dictionary
            
        Returns:
            True if successful
        """
        try:
            doc = {
                '_index': self.index_name,
                '_id': ioc.get('ioc_id', ioc.get('ioc_value', '')),
                '_source': ioc
            }
            
            self.client.index(**doc)
            return True
        except Exception as e:
            logger.error(f"Error indexing IOC {ioc.get('ioc_value', '')}: {e}")
            return False
    
    def bulk_index(self, iocs: List[Dict]) -> int:
        """
        Bulk index multiple IOCs.
        
        Args:
            iocs: List of IOC dictionaries
            
        Returns:
            Number of successfully indexed IOCs
        """
        if not iocs:
            return 0
        
        actions = []
        for ioc in iocs:
            action = {
                '_index': self.index_name,
                '_id': ioc.get('ioc_id', ioc.get('ioc_value', '')),
                '_source': ioc
            }
            actions.append(action)
        
        try:
            success, failed = bulk(self.client, actions, raise_on_error=False)
            logger.info(f"Indexed {success} IOCs, {len(failed)} failed")
            return success
        except Exception as e:
            logger.error(f"Error bulk indexing: {e}")
            return 0
    
    def search_ioc(self, ioc_value: str, ioc_type: Optional[str] = None) -> List[Dict]:
        """
        Search for IOC by value.
        
        Args:
            ioc_value: IOC value to search
            ioc_type: Optional IOC type filter
            
        Returns:
            List of matching IOC dictionaries
        """
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"ioc_value": ioc_value}}
                    ]
                }
            }
        }
        
        if ioc_type:
            query["query"]["bool"]["must"].append({"term": {"ioc_type": ioc_type}})
        
        try:
            # Elasticsearch 8.x still supports body parameter for backward compatibility
            response = self.client.search(index=self.index_name, body=query)
            hits = response.get('hits', {}).get('hits', [])
            return [hit['_source'] for hit in hits]
        except Exception as e:
            logger.error(f"Error searching IOC: {e}")
            return []
    
    def search_threats(self, 
                      threat_type: Optional[str] = None,
                      min_confidence: float = 0.0,
                      limit: int = 100) -> List[Dict]:
        """
        Search threats by type and confidence.
        
        Args:
            threat_type: Optional threat type filter
            min_confidence: Minimum confidence score
            limit: Maximum results
            
        Returns:
            List of matching IOC dictionaries
        """
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"range": {"confidence": {"gte": min_confidence}}}
                    ]
                }
            },
            "sort": [{"confidence": {"order": "desc"}}],
            "size": limit
        }
        
        if threat_type:
            query["query"]["bool"]["must"].append({"term": {"threat_type": threat_type}})
        
        try:
            # Elasticsearch 8.x still supports body parameter for backward compatibility
            response = self.client.search(index=self.index_name, body=query)
            hits = response.get('hits', {}).get('hits', [])
            return [hit['_source'] for hit in hits]
        except Exception as e:
            logger.error(f"Error searching threats: {e}")
            return []
    
    def search_by_time_range(self, 
                            start_time, 
                            end_time, 
                            limit: int = 100) -> List[Dict]:
        """
        Search IOCs by time range.
        
        Args:
            start_time: Start datetime
            end_time: End datetime
            limit: Maximum results
            
        Returns:
            List of matching IOC dictionaries
        """
        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "first_seen": {
                                    "gte": start_time.isoformat(),
                                    "lte": end_time.isoformat()
                                }
                            }
                        }
                    ]
                }
            },
            "sort": [{"first_seen": {"order": "desc"}}],
            "size": limit
        }
        
        try:
            # Elasticsearch 8.x still supports body parameter for backward compatibility
            response = self.client.search(index=self.index_name, body=query)
            hits = response.get('hits', {}).get('hits', [])
            return [hit['_source'] for hit in hits]
        except Exception as e:
            logger.error(f"Error searching by time range: {e}")
            return []
    
    def health_check(self) -> bool:
        """Check Elasticsearch health."""
        try:
            health = self.client.cluster.health()
            return health.get('status') in ['green', 'yellow']
        except Exception as e:
            logger.error(f"Elasticsearch health check failed: {e}")
            return False

