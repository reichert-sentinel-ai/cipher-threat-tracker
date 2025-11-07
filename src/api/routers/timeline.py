"""IOC timeline endpoints"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging

# Optional imports - allow server to start without networkx
try:
    from ...utils.elastic import ElasticsearchClient
    ELASTICSEARCH_AVAILABLE = True
except ImportError:
    ELASTICSEARCH_AVAILABLE = False
    ElasticsearchClient = None

try:
    from ...models.correlation_engine import ThreatCorrelationEngine
    CORRELATION_ENGINE_AVAILABLE = True
except ImportError:
    CORRELATION_ENGINE_AVAILABLE = False
    ThreatCorrelationEngine = None

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/timeline")
async def get_ioc_timeline(
    hours: int = Query(24, description="Hours to look back"),
    threat_type: Optional[str] = Query(None, description="Filter by threat type"),
    min_confidence: float = Query(0.7, description="Minimum confidence score")
):
    """
    Get IOC timeline.
    
    Args:
        hours: Hours to look back
        threat_type: Optional threat type filter
        min_confidence: Minimum confidence score
        
    Returns:
        Timeline of IOCs sorted by time
    """
    if not ELASTICSEARCH_AVAILABLE:
        raise HTTPException(status_code=503, detail="Elasticsearch not available")
    
    try:
        es_client = ElasticsearchClient()
        
        # Get threats
        threats = es_client.search_threats(
            threat_type=threat_type,
            min_confidence=min_confidence,
            limit=1000
        )
        
        # Sort by first_seen
        timeline = sorted(
            threats,
            key=lambda x: x.get('first_seen', ''),
            reverse=True
        )
        
        # Filter by time window
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        filtered_timeline = [
            ioc for ioc in timeline
            if datetime.fromisoformat(ioc.get('first_seen', '').replace('Z', '+00:00')) >= cutoff_time
        ]
        
        return {
            "timeline": filtered_timeline,
            "count": len(filtered_timeline),
            "hours": hours
        }
        
    except Exception as e:
        logger.error(f"Error getting timeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/timeline/campaign/{campaign_id}")
async def get_campaign_timeline(campaign_id: str):
    """
    Get timeline for a specific campaign.
    
    Args:
        campaign_id: Campaign identifier
        
    Returns:
        Timeline of IOCs in campaign
    """
    if not ELASTICSEARCH_AVAILABLE or not CORRELATION_ENGINE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Required dependencies not available")
    
    try:
        es_client = ElasticsearchClient()
        correlation_engine = ThreatCorrelationEngine()
        
        # Get all threats
        iocs = es_client.search_threats(min_confidence=0.7, limit=1000)
        
        # Get campaign timeline
        timeline = correlation_engine.get_campaign_timeline(campaign_id, iocs)
        
        return {
            "campaign_id": campaign_id,
            "timeline": timeline,
            "count": len(timeline)
        }
        
    except Exception as e:
        logger.error(f"Error getting campaign timeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))
