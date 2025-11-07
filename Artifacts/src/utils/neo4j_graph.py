"""Neo4j graph database integration for threat actor network"""

import os
from typing import List, Dict, Optional
from datetime import datetime
import logging

try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False
    logging.warning("Neo4j not available. Install with: pip install neo4j")

logger = logging.getLogger(__name__)


class Neo4jClient:
    """Neo4j client for threat graph construction"""
    
    def __init__(self,
                 uri: Optional[str] = None,
                 username: Optional[str] = None,
                 password: Optional[str] = None):
        """
        Initialize Neo4j client.
        
        Args:
            uri: Neo4j URI (defaults to NEO4J_URI env var or bolt://localhost:7687)
            username: Username (defaults to NEO4J_USER env var or neo4j)
            password: Password (defaults to NEO4J_PASSWORD env var)
        """
        if not NEO4J_AVAILABLE:
            raise ImportError("Neo4j not installed. Install with: pip install neo4j")
        
        uri = uri or os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        username = username or os.getenv('NEO4J_USER', 'neo4j')
        password = password or os.getenv('NEO4J_PASSWORD', 'password')
        
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
    
    def close(self):
        """Close Neo4j connection."""
        self.driver.close()
    
    def create_constraints(self):
        """Create constraints and indexes for better performance."""
        constraints = [
            "CREATE CONSTRAINT ioc_id IF NOT EXISTS FOR (i:IOC) REQUIRE i.ioc_id IS UNIQUE",
            "CREATE CONSTRAINT actor_name IF NOT EXISTS FOR (a:ThreatActor) REQUIRE a.name IS UNIQUE",
            "CREATE CONSTRAINT campaign_id IF NOT EXISTS FOR (c:Campaign) REQUIRE c.campaign_id IS UNIQUE"
        ]
        
        with self.driver.session() as session:
            for constraint in constraints:
                try:
                    session.run(constraint)
                    logger.info(f"Created constraint: {constraint[:50]}...")
                except Exception as e:
                    logger.debug(f"Constraint may already exist: {e}")
    
    def create_ioc_node(self, ioc: Dict) -> bool:
        """
        Create or update IOC node.
        
        Args:
            ioc: IOC dictionary
            
        Returns:
            True if successful
        """
        query = """
        MERGE (i:IOC {ioc_id: $ioc_id})
        SET i.ioc_value = $ioc_value,
            i.ioc_type = $ioc_type,
            i.source = $source,
            i.threat_type = $threat_type,
            i.first_seen = $first_seen,
            i.last_seen = $last_seen,
            i.confidence = $confidence,
            i.tags = $tags,
            i.updated_at = datetime()
        """
        
        try:
            with self.driver.session() as session:
                session.run(query, **ioc)
            return True
        except Exception as e:
            logger.error(f"Error creating IOC node: {e}")
            return False
    
    def create_threat_actor(self, actor_name: str, metadata: Optional[Dict] = None) -> bool:
        """
        Create or update threat actor node.
        
        Args:
            actor_name: Threat actor name
            metadata: Optional metadata dictionary
            
        Returns:
            True if successful
        """
        metadata = metadata or {}
        
        query = """
        MERGE (a:ThreatActor {name: $name})
        SET a.aliases = $aliases,
            a.country_of_origin = $country_of_origin,
            a.sector_targets = $sector_targets,
            a.updated_at = datetime()
        """
        
        params = {
            'name': actor_name,
            'aliases': metadata.get('aliases', []),
            'country_of_origin': metadata.get('country_of_origin', ''),
            'sector_targets': metadata.get('sector_targets', [])
        }
        
        try:
            with self.driver.session() as session:
                session.run(query, **params)
            return True
        except Exception as e:
            logger.error(f"Error creating threat actor: {e}")
            return False
    
    def link_ioc_to_actor(self, ioc_id: str, actor_name: str, relationship: str = "USES") -> bool:
        """
        Link IOC to threat actor.
        
        Args:
            ioc_id: IOC ID
            actor_name: Threat actor name
            relationship: Relationship type (default: USES)
            
        Returns:
            True if successful
        """
        query = f"""
        MATCH (i:IOC {{ioc_id: $ioc_id}})
        MATCH (a:ThreatActor {{name: $actor_name}})
        MERGE (a)-[:{relationship}]->(i)
        """
        
        try:
            with self.driver.session() as session:
                session.run(query, ioc_id=ioc_id, actor_name=actor_name)
            return True
        except Exception as e:
            logger.error(f"Error linking IOC to actor: {e}")
            return False
    
    def create_campaign(self, campaign_id: str, metadata: Dict) -> bool:
        """
        Create or update campaign node.
        
        Args:
            campaign_id: Campaign identifier
            metadata: Campaign metadata
            
        Returns:
            True if successful
        """
        query = """
        MERGE (c:Campaign {campaign_id: $campaign_id})
        SET c.name = $name,
            c.description = $description,
            c.start_date = $start_date,
            c.end_date = $end_date,
            c.updated_at = datetime()
        """
        
        params = {
            'campaign_id': campaign_id,
            'name': metadata.get('name', ''),
            'description': metadata.get('description', ''),
            'start_date': metadata.get('start_date', ''),
            'end_date': metadata.get('end_date', '')
        }
        
        try:
            with self.driver.session() as session:
                session.run(query, **params)
            return True
        except Exception as e:
            logger.error(f"Error creating campaign: {e}")
            return False
    
    def link_ioc_to_campaign(self, ioc_id: str, campaign_id: str) -> bool:
        """
        Link IOC to campaign.
        
        Args:
            ioc_id: IOC ID
            campaign_id: Campaign ID
            
        Returns:
            True if successful
        """
        query = """
        MATCH (i:IOC {ioc_id: $ioc_id})
        MATCH (c:Campaign {campaign_id: $campaign_id})
        MERGE (i)-[:FROM_CAMPAIGN]->(c)
        """
        
        try:
            with self.driver.session() as session:
                session.run(query, ioc_id=ioc_id, campaign_id=campaign_id)
            return True
        except Exception as e:
            logger.error(f"Error linking IOC to campaign: {e}")
            return False
    
    def link_actors(self, actor1: str, actor2: str, relationship: str = "ASSOCIATED_WITH") -> bool:
        """
        Link two threat actors.
        
        Args:
            actor1: First threat actor name
            actor2: Second threat actor name
            relationship: Relationship type (default: ASSOCIATED_WITH)
            
        Returns:
            True if successful
        """
        query = f"""
        MATCH (a1:ThreatActor {{name: $actor1}})
        MATCH (a2:ThreatActor {{name: $actor2}})
        MERGE (a1)-[:{relationship}]->(a2)
        """
        
        try:
            with self.driver.session() as session:
                session.run(query, actor1=actor1, actor2=actor2)
            return True
        except Exception as e:
            logger.error(f"Error linking actors: {e}")
            return False
    
    def get_threat_network(self, actor_name: Optional[str] = None, depth: int = 2) -> List[Dict]:
        """
        Get threat actor network graph.
        
        Args:
            actor_name: Optional starting actor name
            depth: Graph depth to traverse
            
        Returns:
            List of node and relationship dictionaries
        """
        if actor_name:
            query = f"""
            MATCH path = (a:ThreatActor {{name: $actor_name}})-[*1..{depth}]-(related)
            RETURN nodes(path) as nodes, relationships(path) as relationships
            LIMIT 100
            """
            params = {'actor_name': actor_name}
        else:
            query = f"""
            MATCH path = (a:ThreatActor)-[*1..{depth}]-(related)
            RETURN nodes(path) as nodes, relationships(path) as relationships
            LIMIT 100
            """
            params = {}
        
        try:
            with self.driver.session() as session:
                result = session.run(query, **params)
                paths = []
                for record in result:
                    nodes = [dict(node) for node in record['nodes']]
                    relationships = [dict(rel) for rel in record['relationships']]
                    paths.append({
                        'nodes': nodes,
                        'relationships': relationships
                    })
                return paths
        except Exception as e:
            logger.error(f"Error getting threat network: {e}")
            return []
    
    def bulk_create_iocs(self, iocs: List[Dict]) -> int:
        """
        Bulk create IOC nodes.
        
        Args:
            iocs: List of IOC dictionaries
            
        Returns:
            Number of successfully created nodes
        """
        if not iocs:
            return 0
        
        query = """
        UNWIND $iocs AS ioc
        MERGE (i:IOC {ioc_id: ioc.ioc_id})
        SET i.ioc_value = ioc.ioc_value,
            i.ioc_type = ioc.ioc_type,
            i.source = ioc.source,
            i.threat_type = ioc.threat_type,
            i.first_seen = ioc.first_seen,
            i.last_seen = ioc.last_seen,
            i.confidence = ioc.confidence,
            i.tags = ioc.tags,
            i.updated_at = datetime()
        """
        
        try:
            with self.driver.session() as session:
                result = session.run(query, iocs=iocs)
                result.consume()
                return len(iocs)
        except Exception as e:
            logger.error(f"Error bulk creating IOCs: {e}")
            return 0
    
    def get_all_actors(self, limit: int = 100) -> List[Dict]:
        """
        Get all threat actors.
        
        Args:
            limit: Maximum number of actors to return
            
        Returns:
            List of threat actor dictionaries
        """
        query = """
        MATCH (a:ThreatActor)
        RETURN a.name as name, 
               a.aliases as aliases,
               a.country_of_origin as country_of_origin,
               a.sector_targets as sector_targets,
               a.updated_at as updated_at
        LIMIT $limit
        """
        
        try:
            with self.driver.session() as session:
                result = session.run(query, limit=limit)
                actors = [dict(record) for record in result]
                return actors
        except Exception as e:
            logger.error(f"Error getting all actors: {e}")
            return []
    
    def get_actor_details(self, actor_name: str) -> Optional[Dict]:
        """
        Get details for a specific threat actor.
        
        Args:
            actor_name: Threat actor name
            
        Returns:
            Actor details dictionary or None if not found
        """
        query = """
        MATCH (a:ThreatActor {name: $name})
        OPTIONAL MATCH (a)-[:USES]->(i:IOC)
        OPTIONAL MATCH (a)-[:ASSOCIATED_WITH]-(related:ThreatActor)
        RETURN a,
               collect(DISTINCT i.ioc_value) as iocs,
               collect(DISTINCT related.name) as related_actors
        """
        
        try:
            with self.driver.session() as session:
                result = session.run(query, name=actor_name)
                record = result.single()
                
                if not record:
                    return None
                
                actor_data = dict(record['a'])
                actor_data['iocs'] = record['iocs'] or []
                actor_data['related_actors'] = record['related_actors'] or []
                
                return actor_data
        except Exception as e:
            logger.error(f"Error getting actor details: {e}")
            return None
    
    def get_actor_iocs(self, actor_name: str) -> List[Dict]:
        """
        Get all IOCs associated with a threat actor.
        
        Args:
            actor_name: Threat actor name
            
        Returns:
            List of IOC dictionaries
        """
        query = """
        MATCH (a:ThreatActor {name: $name})-[r:USES]->(i:IOC)
        RETURN i.ioc_value as ioc_value,
               i.ioc_type as ioc_type,
               i.ioc_id as ioc_id,
               i.source as source,
               i.threat_type as threat_type,
               i.confidence as confidence,
               i.first_seen as first_seen,
               i.last_seen as last_seen,
               i.tags as tags
        """
        
        try:
            with self.driver.session() as session:
                result = session.run(query, name=actor_name)
                iocs = [dict(record) for record in result]
                return iocs
        except Exception as e:
            logger.error(f"Error getting actor IOCs: {e}")
            return []
    
    def get_all_campaigns(self, limit: int = 100) -> List[Dict]:
        """
        Get all campaigns.
        
        Args:
            limit: Maximum number of campaigns to return
            
        Returns:
            List of campaign dictionaries
        """
        query = """
        MATCH (c:Campaign)
        OPTIONAL MATCH (c)<-[:FROM_CAMPAIGN]-(i:IOC)
        RETURN c.campaign_id as campaign_id,
               c.name as name,
               c.description as description,
               c.start_date as start_date,
               c.end_date as end_date,
               count(i) as num_iocs,
               c.updated_at as updated_at
        ORDER BY c.updated_at DESC
        LIMIT $limit
        """
        
        try:
            with self.driver.session() as session:
                result = session.run(query, limit=limit)
                campaigns = [dict(record) for record in result]
                return campaigns
        except Exception as e:
            logger.error(f"Error getting all campaigns: {e}")
            return []
    
    def get_campaign_details(self, campaign_id: str) -> Optional[Dict]:
        """
        Get details for a specific campaign.
        
        Args:
            campaign_id: Campaign identifier
            
        Returns:
            Campaign details dictionary or None if not found
        """
        query = """
        MATCH (c:Campaign {campaign_id: $campaign_id})
        OPTIONAL MATCH (c)<-[:FROM_CAMPAIGN]-(i:IOC)
        OPTIONAL MATCH (i)<-[:USES]-(a:ThreatActor)
        RETURN c,
               collect(DISTINCT i.ioc_value) as iocs,
               collect(DISTINCT a.name) as threat_actors
        """
        
        try:
            with self.driver.session() as session:
                result = session.run(query, campaign_id=campaign_id)
                record = result.single()
                
                if not record:
                    return None
                
                campaign_data = dict(record['c'])
                campaign_data['iocs'] = record['iocs'] or []
                campaign_data['threat_actors'] = record['threat_actors'] or []
                
                return campaign_data
        except Exception as e:
            logger.error(f"Error getting campaign details: {e}")
            return None
    
    def get_campaign_iocs(self, campaign_id: str) -> List[Dict]:
        """
        Get all IOCs in a campaign.
        
        Args:
            campaign_id: Campaign identifier
            
        Returns:
            List of IOC dictionaries
        """
        query = """
        MATCH (c:Campaign {campaign_id: $campaign_id})<-[:FROM_CAMPAIGN]-(i:IOC)
        RETURN i.ioc_value as ioc_value,
               i.ioc_type as ioc_type,
               i.ioc_id as ioc_id,
               i.source as source,
               i.threat_type as threat_type,
               i.confidence as confidence,
               i.first_seen as first_seen,
               i.last_seen as last_seen,
               i.tags as tags
        ORDER BY i.first_seen DESC
        """
        
        try:
            with self.driver.session() as session:
                result = session.run(query, campaign_id=campaign_id)
                iocs = [dict(record) for record in result]
                return iocs
        except Exception as e:
            logger.error(f"Error getting campaign IOCs: {e}")
            return []

