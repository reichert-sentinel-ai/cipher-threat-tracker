"""Threat network graph endpoints"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Optional
import logging

from ...utils.neo4j_graph import Neo4jClient

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/network")
async def get_threat_network(
    actor_name: Optional[str] = Query(None, description="Starting actor name"),
    depth: int = Query(2, description="Graph depth to traverse")
):
    """
    Get threat actor network graph.
    
    Args:
        actor_name: Optional starting actor name
        depth: Graph depth to traverse
        
    Returns:
        Network graph with nodes and relationships
    """
    try:
        neo4j = Neo4jClient()
        
        # Get network
        network = neo4j.get_threat_network(actor_name=actor_name, depth=depth)
        
        # Format for visualization
        nodes = []
        edges = []
        node_ids = set()
        
        for path in network:
            for node in path.get('nodes', []):
                node_id = node.get('ioc_id') or node.get('name') or str(hash(str(node)))
                if node_id not in node_ids:
                    nodes.append({
                        "id": node_id,
                        "label": node.get('ioc_value') or node.get('name') or node_id,
                        "type": node.get('ioc_type') or node.get('label') or 'unknown',
                        "data": node
                    })
                    node_ids.add(node_id)
            
            for rel in path.get('relationships', []):
                # Extract source and target from relationship
                source = str(rel.get('start_node_id', ''))
                target = str(rel.get('end_node_id', ''))
                
                if source and target:
                    edges.append({
                        "source": source,
                        "target": target,
                        "type": rel.get('type', 'RELATED'),
                        "data": dict(rel)
                    })
        
        neo4j.close()
        
        return {
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "num_nodes": len(nodes),
                "num_edges": len(edges)
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting threat network: {e}")
        raise HTTPException(status_code=500, detail=str(e))
