"""Campaigns endpoints"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Optional
import logging

from ...utils.neo4j_graph import Neo4jClient

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/campaigns")
async def get_campaigns(
    limit: int = Query(100, description="Maximum results")
):
    """
    Get all active campaigns.
    
    Args:
        limit: Maximum results
        
    Returns:
        List of campaign dictionaries
    """
    try:
        neo4j = Neo4jClient()
        campaigns = neo4j.get_all_campaigns(limit=limit)
        neo4j.close()
        return {"campaigns": campaigns, "count": len(campaigns)}
    except Exception as e:
        logger.error(f"Error getting campaigns: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/campaigns/{campaign_id}")
async def get_campaign_details(campaign_id: str):
    """
    Get details for a specific campaign.
    
    Args:
        campaign_id: Campaign ID
        
    Returns:
        Campaign details
    """
    try:
        neo4j = Neo4jClient()
        campaign = neo4j.get_campaign_details(campaign_id)
        neo4j.close()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        return campaign
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting campaign details: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/campaigns/{campaign_id}/iocs")
async def get_campaign_iocs(campaign_id: str):
    """
    Get all IOCs in a campaign.
    
    Args:
        campaign_id: Campaign ID
        
    Returns:
        List of IOC dictionaries
    """
    try:
        neo4j = Neo4jClient()
        iocs = neo4j.get_campaign_iocs(campaign_id)
        neo4j.close()
        return {"iocs": iocs, "count": len(iocs)}
    except Exception as e:
        logger.error(f"Error getting campaign IOCs: {e}")
        raise HTTPException(status_code=500, detail=str(e))