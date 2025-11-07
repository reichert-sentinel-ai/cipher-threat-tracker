"""Threat actors endpoints"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Optional
import logging

from ...utils.neo4j_graph import Neo4jClient

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/actors")
async def get_actors(
    limit: int = Query(100, description="Maximum results")
):
    """
    Get all threat actors.
    
    Args:
        limit: Maximum results
        
    Returns:
        List of threat actor dictionaries
    """
    try:
        neo4j = Neo4jClient()
        actors = neo4j.get_all_actors(limit=limit)
        neo4j.close()
        return {"actors": actors, "count": len(actors)}
    except Exception as e:
        logger.error(f"Error getting actors: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/actors/{actor_name}")
async def get_actor_details(actor_name: str):
    """
    Get details for a specific threat actor.
    
    Args:
        actor_name: Threat actor name
        
    Returns:
        Threat actor details
    """
    try:
        neo4j = Neo4jClient()
        actor = neo4j.get_actor_details(actor_name)
        neo4j.close()
        
        if not actor:
            raise HTTPException(status_code=404, detail="Actor not found")
        
        return actor
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting actor details: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/actors/{actor_name}/iocs")
async def get_actor_iocs(actor_name: str):
    """
    Get all IOCs associated with a threat actor.
    
    Args:
        actor_name: Threat actor name
        
    Returns:
        List of IOC dictionaries
    """
    try:
        neo4j = Neo4jClient()
        iocs = neo4j.get_actor_iocs(actor_name)
        neo4j.close()
        return {"iocs": iocs, "count": len(iocs)}
    except Exception as e:
        logger.error(f"Error getting actor IOCs: {e}")
        raise HTTPException(status_code=500, detail=str(e))