"""Threats endpoints"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Optional
import logging

from ...utils.elastic import ElasticsearchClient

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/threats")
async def get_threats(
    threat_type: Optional[str] = Query(None, description="Filter by threat type"),
    min_confidence: float = Query(0.7, description="Minimum confidence score"),
    limit: int = Query(100, description="Maximum results")
):
    """
    Get active threats.
    
    Args:
        threat_type: Optional threat type filter
        min_confidence: Minimum confidence score
        limit: Maximum results
        
    Returns:
        List of threat IOC dictionaries
    """
    try:
        es_client = ElasticsearchClient()
        threats = es_client.search_threats(
            threat_type=threat_type,
            min_confidence=min_confidence,
            limit=limit
        )
        return {"threats": threats, "count": len(threats)}
    except Exception as e:
        logger.error(f"Error getting threats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/threats/stats")
async def get_threat_stats():
    """Get threat statistics."""
    try:
        es_client = ElasticsearchClient()
        
        # Get all high-confidence threats
        high_confidence = es_client.search_threats(min_confidence=0.8, limit=1000)
        
        # Count by threat type
        threat_types = {}
        sources = {}
        
        for threat in high_confidence:
            threat_type = threat.get('threat_type', 'unknown')
            source = threat.get('source', 'unknown')
            
            threat_types[threat_type] = threat_types.get(threat_type, 0) + 1
            sources[source] = sources.get(source, 0) + 1
        
        return {
            "total_threats": len(high_confidence),
            "by_threat_type": threat_types,
            "by_source": sources
        }
    except Exception as e:
        logger.error(f"Error getting threat stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

