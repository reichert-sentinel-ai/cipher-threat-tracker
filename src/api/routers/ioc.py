"""IOC lookup and management endpoints"""

from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from typing import List, Dict, Optional
from pydantic import BaseModel
import logging

from ...collectors.ioc_orchestrator import IOCOrchestrator
from ...utils.elastic import ElasticsearchClient

logger = logging.getLogger(__name__)

router = APIRouter()


class IOCLookupRequest(BaseModel):
    """Request model for IOC lookup"""
    ioc_value: str
    ioc_type: Optional[str] = None


class IOCResponse(BaseModel):
    """Response model for IOC data"""
    ioc_value: str
    ioc_type: str
    ioc_id: str
    source: str
    threat_type: str
    first_seen: str
    last_seen: str
    confidence: float
    tags: List[str]
    metadata: Dict


@router.post("/ioc/check", response_model=List[IOCResponse])
async def check_ioc(request: IOCLookupRequest):
    """
    Check if IOC is known threat.
    
    Args:
        request: IOC lookup request
        
    Returns:
        List of matching IOC records
    """
    try:
        # Initialize Elasticsearch client
        es_client = ElasticsearchClient()
        
        # Search for IOC
        results = es_client.search_ioc(
            ioc_value=request.ioc_value,
            ioc_type=request.ioc_type
        )
        
        if not results:
            return []
        
        # Convert to response models
        responses = [
            IOCResponse(**result)
            for result in results
        ]
        
        return responses
        
    except Exception as e:
        logger.error(f"Error checking IOC: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ioc/search")
async def search_iocs(
    query: str = Query(..., description="Search query"),
    ioc_type: Optional[str] = Query(None, description="Filter by IOC type"),
    min_confidence: float = Query(0.0, description="Minimum confidence score"),
    limit: int = Query(100, description="Maximum results")
):
    """
    Search IOCs by query.
    
    Args:
        query: Search query string
        ioc_type: Optional IOC type filter
        min_confidence: Minimum confidence score
        limit: Maximum results
        
    Returns:
        List of matching IOC records
    """
    try:
        es_client = ElasticsearchClient()
        
        # Search threats (simplified - would use full-text search in production)
        results = es_client.search_threats(
            threat_type=ioc_type,
            min_confidence=min_confidence,
            limit=limit
        )
        
        # Filter by query (simplified)
        filtered = [
            result for result in results
            if query.lower() in str(result.get('ioc_value', '')).lower() or
               query.lower() in str(result.get('description', '')).lower()
        ]
        
        return filtered[:limit]
        
    except Exception as e:
        logger.error(f"Error searching IOCs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ioc/collect")
async def collect_iocs(
    limit_per_source: int = Query(100, description="IOCs per source to collect"),
    background_tasks: BackgroundTasks = None
):
    """
    Trigger IOC collection from all sources.
    
    Args:
        limit_per_source: Maximum IOCs per source
        background_tasks: Background tasks for async processing
        
    Returns:
        Collection status
    """
    try:
        orchestrator = IOCOrchestrator()
        es_client = ElasticsearchClient()
        
        # Collect IOCs (async in background)
        def collect_and_index():
            try:
                iocs = orchestrator.collect_all(limit_per_source=limit_per_source)
                
                # Index in Elasticsearch
                es_client.bulk_index(iocs)
                
                logger.info(f"Collected and indexed {len(iocs)} IOCs")
            except Exception as e:
                logger.error(f"Error in background collection: {e}")
        
        if background_tasks:
            background_tasks.add_task(collect_and_index)
        
        return {
            "status": "started",
            "message": f"IOC collection started (limit: {limit_per_source} per source)"
        }
        
    except Exception as e:
        logger.error(f"Error starting IOC collection: {e}")
        raise HTTPException(status_code=500, detail=str(e))

