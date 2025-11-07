"""Threat correlation engine for linking related IOCs"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Set
from datetime import datetime, timedelta
from collections import defaultdict
import networkx as nx
import logging

logger = logging.getLogger(__name__)


class ThreatCorrelationEngine:
    """Correlate related IOCs into campaigns and threat actor groups"""
    
    def __init__(self,
                 time_window_hours: int = 24,
                 similarity_threshold: float = 0.7):
        """
        Initialize correlation engine.
        
        Args:
            time_window_hours: Time window for temporal correlation (default: 24 hours)
            similarity_threshold: Minimum similarity for correlation (default: 0.7)
        """
        self.time_window_hours = time_window_hours
        self.similarity_threshold = similarity_threshold
        self.campaigns: Dict[str, Dict] = {}
        self.campaign_counter = 0
    
    def correlate_iocs(self, iocs: List[Dict]) -> Tuple[List[Dict], Dict[str, List[str]]]:
        """
        Correlate IOCs into campaigns.
        
        Args:
            iocs: List of IOC dictionaries
            
        Returns:
            Tuple of (updated IOCs with campaign IDs, campaign mapping)
        """
        if not iocs:
            return [], {}
        
        # Create correlation graph
        graph = self._build_correlation_graph(iocs)
        
        # Find connected components (campaigns)
        campaigns = {}
        for component in nx.connected_components(graph):
            if len(component) < 2:
                continue  # Skip single-node components
            
            # Create campaign
            campaign_id = f"campaign_{self.campaign_counter}"
            self.campaign_counter += 1
            
            component_iocs = [ioc for ioc in iocs if ioc.get('ioc_id') in component]
            
            campaign = {
                'campaign_id': campaign_id,
                'ioc_ids': list(component),
                'num_iocs': len(component),
                'threat_types': list(set(ioc.get('threat_type', 'unknown') for ioc in component_iocs)),
                'sources': list(set(ioc.get('source', 'unknown') for ioc in component_iocs)),
                'first_seen': min((ioc.get('first_seen', '') for ioc in component_iocs), default=''),
                'last_seen': max((ioc.get('last_seen', '') for ioc in component_iocs), default=''),
                'confidence': np.mean([ioc.get('confidence', 0.5) for ioc in component_iocs])
            }
            
            campaigns[campaign_id] = campaign
            
            # Assign campaign IDs to IOCs
            for ioc in component_iocs:
                if 'metadata' not in ioc:
                    ioc['metadata'] = {}
                ioc['metadata']['campaign_id'] = campaign_id
        
        # Update IOCs with campaign info
        updated_iocs = iocs.copy()
        
        # Create mapping from campaign_id to IOC IDs
        campaign_mapping = {
            campaign_id: campaign['ioc_ids']
            for campaign_id, campaign in campaigns.items()
        }
        
        logger.info(f"Correlated {len(iocs)} IOCs into {len(campaigns)} campaigns")
        
        return updated_iocs, campaign_mapping
    
    def _build_correlation_graph(self, iocs: List[Dict]) -> nx.Graph:
        """Build correlation graph from IOCs."""
        graph = nx.Graph()
        
        # Add nodes
        for ioc in iocs:
            ioc_id = ioc.get('ioc_id', '')
            if ioc_id:
                graph.add_node(ioc_id, **ioc)
        
        # Add edges based on correlations
        for i, ioc1 in enumerate(iocs):
            ioc1_id = ioc1.get('ioc_id', '')
            if not ioc1_id:
                continue
            
            for j, ioc2 in enumerate(iocs[i+1:], start=i+1):
                ioc2_id = ioc2.get('ioc_id', '')
                if not ioc2_id:
                    continue
                
                # Calculate similarity
                similarity = self._calculate_similarity(ioc1, ioc2)
                
                if similarity >= self.similarity_threshold:
                    graph.add_edge(ioc1_id, ioc2_id, similarity=similarity, weight=similarity)
        
        return graph
    
    def _calculate_similarity(self, ioc1: Dict, ioc2: Dict) -> float:
        """
        Calculate similarity between two IOCs.
        
        Returns similarity score [0, 1]
        """
        similarity = 0.0
        
        # Temporal similarity (same time window)
        time_sim = self._temporal_similarity(ioc1, ioc2)
        similarity += 0.3 * time_sim
        
        # Source similarity (same source)
        source_sim = 1.0 if ioc1.get('source') == ioc2.get('source') else 0.0
        similarity += 0.2 * source_sim
        
        # Threat type similarity
        threat_sim = 1.0 if ioc1.get('threat_type') == ioc2.get('threat_type') else 0.0
        similarity += 0.2 * threat_sim
        
        # Tag overlap
        tags1 = set(ioc1.get('tags', []))
        tags2 = set(ioc2.get('tags', []))
        if tags1 or tags2:
            tag_sim = len(tags1 & tags2) / len(tags1 | tags2) if (tags1 | tags2) else 0.0
            similarity += 0.2 * tag_sim
        
        # Domain/IP relationship
        relationship_sim = self._relationship_similarity(ioc1, ioc2)
        similarity += 0.1 * relationship_sim
        
        return min(similarity, 1.0)
    
    def _temporal_similarity(self, ioc1: Dict, ioc2: Dict) -> float:
        """Calculate temporal similarity based on time window."""
        try:
            time1 = datetime.fromisoformat(ioc1.get('first_seen', '').replace('Z', '+00:00'))
            time2 = datetime.fromisoformat(ioc2.get('first_seen', '').replace('Z', '+00:00'))
            
            time_diff = abs((time1 - time2).total_seconds() / 3600)  # Hours
            
            if time_diff <= self.time_window_hours:
                # Exponential decay within window
                return np.exp(-time_diff / self.time_window_hours)
            else:
                return 0.0
        except Exception:
            return 0.5  # Default if time parsing fails
    
    def _relationship_similarity(self, ioc1: Dict, ioc2: Dict) -> float:
        """Check for direct relationships (e.g., IP-Domain)."""
        value1 = str(ioc1.get('ioc_value', '')).lower()
        value2 = str(ioc2.get('ioc_value', '')).lower()
        type1 = ioc1.get('ioc_type', '')
        type2 = ioc2.get('ioc_type', '')
        
        # Domain-IP relationship (simplified - would need DNS lookups in production)
        if (type1 == 'domain' and type2 == 'ip') or (type1 == 'ip' and type2 == 'domain'):
            # Check if IP is mentioned in metadata
            metadata1 = ioc1.get('metadata', {})
            metadata2 = ioc2.get('metadata', {})
            
            if 'related_domain' in metadata1 and metadata1['related_domain'] == value2:
                return 1.0
            if 'related_domain' in metadata2 and metadata2['related_domain'] == value1:
                return 1.0
        
        # Hash relationships
        if type1 == 'hash' and type2 == 'hash':
            metadata1 = ioc1.get('metadata', {})
            metadata2 = ioc2.get('metadata', {})
            
            related1 = metadata1.get('related_hashes', {})
            related2 = metadata2.get('related_hashes', {})
            
            if value1 in related2.values() or value2 in related1.values():
                return 1.0
        
        return 0.0
    
    def attribute_threat_actors(self, campaigns: Dict[str, Dict], iocs: List[Dict]) -> Dict[str, List[str]]:
        """
        Attribute campaigns to threat actors based on TTPs and patterns.
        
        Args:
            campaigns: Campaign dictionary
            iocs: List of IOC dictionaries
            
        Returns:
            Dictionary mapping campaign_id to threat actor names
        """
        # Simplified attribution - in production would use MITRE ATT&CK mapping
        attribution = {}
        
        for campaign_id, campaign in campaigns.items():
            threat_types = campaign.get('threat_types', [])
            sources = campaign.get('sources', [])
            
            # Simple heuristics for attribution
            threat_actors = []
            
            # Check threat types and sources for attribution hints
            if 'ransomware' in str(threat_types).lower():
                threat_actors.append('Ransomware Group')
            if 'apt' in str(sources).lower():
                threat_actors.append('APT Group')
            if 'c2_server' in threat_types:
                threat_actors.append('Unknown Threat Actor')
            
            if not threat_actors:
                threat_actors.append('Unknown')
            
            attribution[campaign_id] = threat_actors
        
        return attribution
    
    def get_campaign_timeline(self, campaign_id: str, iocs: List[Dict]) -> List[Dict]:
        """
        Get timeline of IOCs in a campaign.
        
        Args:
            campaign_id: Campaign identifier
            iocs: List of IOC dictionaries
            
        Returns:
            Timeline of IOCs sorted by time
        """
        campaign_iocs = [
            ioc for ioc in iocs
            if ioc.get('metadata', {}).get('campaign_id') == campaign_id
        ]
        
        # Sort by first_seen
        timeline = sorted(campaign_iocs, key=lambda x: x.get('first_seen', ''))
        
        return timeline

