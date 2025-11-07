from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import numpy as np
import re

router = APIRouter(prefix="/api/ioc", tags=["ioc-search"])

class IOC(BaseModel):
    ioc_id: str
    value: str
    type: str  # "ip", "domain", "hash", "email", "url", "file_path"
    first_seen: str
    last_seen: str
    threat_level: str  # "critical", "high", "medium", "low"
    confidence: float  # 0-1 scale
    tags: List[str]
    threat_actors: List[str]
    malware_families: List[str]
    campaigns: List[str]
    sources: List[str]
    description: str

class IOCEnrichment(BaseModel):
    ioc_value: str
    ioc_type: str
    reputation_score: int  # 0-100, lower is worse
    threat_intelligence: Dict[str, Any]
    geolocation: Optional[Dict[str, str]]
    whois_data: Optional[Dict[str, str]]
    related_iocs: List[str]
    malware_analysis: Optional[Dict[str, Any]]
    detection_rules: List[str]
    recommendations: List[str]

class IOCSearchResult(BaseModel):
    total_results: int
    query: str
    iocs: List[IOC]
    search_time_ms: float
    related_searches: List[str]

class IOCCorrelation(BaseModel):
    correlation_id: str
    primary_ioc: str
    related_iocs: List[Dict[str, Any]]
    correlation_score: float
    relationship_type: str  # "same_campaign", "same_actor", "infrastructure", "temporal"
    timeline: List[Dict[str, Any]]

class IOCFeed(BaseModel):
    feed_name: str
    last_updated: str
    total_iocs: int
    new_iocs_24h: int
    critical_iocs: int
    feed_reliability: str

# Mock IOC database
MOCK_IOCS = [
    {
        "value": "185.220.101.45",
        "type": "ip",
        "threat_level": "critical",
        "tags": ["c2", "malware", "apt"],
        "threat_actors": ["APT28"],
        "malware_families": ["Sofacy"],
        "campaigns": ["Operation Phantom"]
    },
    {
        "value": "malicious-payload.exe",
        "type": "hash",
        "threat_level": "high",
        "tags": ["ransomware", "trojan"],
        "threat_actors": ["DarkSide"],
        "malware_families": ["DarkSide Ransomware"],
        "campaigns": ["DarkSide 2024"]
    },
    {
        "value": "phishing-site-2024.com",
        "type": "domain",
        "threat_level": "high",
        "tags": ["phishing", "credential_theft"],
        "threat_actors": ["FIN7"],
        "malware_families": ["Carbanak"],
        "campaigns": ["Operation Credential Harvest"]
    },
    {
        "value": "attacker@evil-domain.net",
        "type": "email",
        "threat_level": "medium",
        "tags": ["spearphishing", "social_engineering"],
        "threat_actors": ["Unknown"],
        "malware_families": [],
        "campaigns": []
    },
    {
        "value": "192.168.100.50",
        "type": "ip",
        "threat_level": "low",
        "tags": ["scanning", "reconnaissance"],
        "threat_actors": [],
        "malware_families": [],
        "campaigns": []
    }
]

@router.get("/search", response_model=IOCSearchResult)
async def search_iocs(
    query: str = Query(..., description="IOC value or search term"),
    ioc_type: Optional[str] = Query(None, description="Filter by IOC type"),
    threat_level: Optional[str] = Query(None, description="Filter by threat level"),
    limit: int = Query(50, le=500, description="Maximum results to return")
):
    """
    Search for IOCs across multiple threat intelligence feeds.
    """
    
    import time
    start_time = time.time()
    
    # Detect IOC type from query if not specified
    if not ioc_type:
        ioc_type = detect_ioc_type(query)
    
    # Generate mock search results
    results = []
    
    # Add some base IOCs
    for mock_ioc in MOCK_IOCS:
        if query.lower() in mock_ioc["value"].lower() or not query:
            if ioc_type and mock_ioc["type"] != ioc_type:
                continue
            if threat_level and mock_ioc["threat_level"] != threat_level:
                continue
            
            first_seen = datetime.now() - timedelta(days=np.random.randint(1, 90))
            last_seen = datetime.now() - timedelta(days=np.random.randint(0, 30))
            
            results.append(IOC(
                ioc_id=f"ioc_{len(results)+1:05d}",
                value=mock_ioc["value"],
                type=mock_ioc["type"],
                first_seen=first_seen.isoformat(),
                last_seen=last_seen.isoformat(),
                threat_level=mock_ioc["threat_level"],
                confidence=round(np.random.uniform(0.7, 0.99), 2),
                tags=mock_ioc["tags"],
                threat_actors=mock_ioc["threat_actors"],
                malware_families=mock_ioc["malware_families"],
                campaigns=mock_ioc["campaigns"],
                sources=["VirusTotal", "AlienVault OTX", "Abuse.ch", "MISP"],
                description=f"Malicious {mock_ioc['type']} associated with threat activity"
            ))
    
    # Generate additional synthetic results
    num_synthetic = min(limit - len(results), 20)
    for i in range(num_synthetic):
        ioc_value, ioc_type_gen = generate_synthetic_ioc(ioc_type)
        
        threat_levels = ["critical", "high", "medium", "low"]
        selected_threat_level = np.random.choice(threat_levels, p=[0.1, 0.3, 0.4, 0.2])
        
        if threat_level and selected_threat_level != threat_level:
            continue
        
        first_seen = datetime.now() - timedelta(days=np.random.randint(1, 180))
        last_seen = datetime.now() - timedelta(days=np.random.randint(0, 60))
        
        results.append(IOC(
            ioc_id=f"ioc_{len(results)+1:05d}",
            value=ioc_value,
            type=ioc_type_gen,
            first_seen=first_seen.isoformat(),
            last_seen=last_seen.isoformat(),
            threat_level=selected_threat_level,
            confidence=round(np.random.uniform(0.6, 0.95), 2),
            tags=np.random.choice([
                "malware", "phishing", "c2", "ransomware", "apt", 
                "trojan", "botnet", "exploit", "backdoor"
            ], size=np.random.randint(1, 4), replace=False).tolist(),
            threat_actors=np.random.choice([
                "APT28", "APT29", "Lazarus", "FIN7", "DarkSide", "Unknown"
            ], size=np.random.randint(0, 2), replace=False).tolist(),
            malware_families=np.random.choice([
                "Emotet", "TrickBot", "Cobalt Strike", "Mimikatz", "Ryuk"
            ], size=np.random.randint(0, 2), replace=False).tolist(),
            campaigns=[f"Campaign-{np.random.randint(1000, 9999)}"],
            sources=["VirusTotal", "AlienVault OTX"],
            description=f"Suspicious {ioc_type_gen} identified in threat intelligence feeds"
        ))
    
    search_time = (time.time() - start_time) * 1000  # Convert to ms
    
    # Generate related searches
    related_searches = [
        f"{query} related infrastructure",
        f"{query} threat actor",
        f"{query} malware family",
        "recent IOCs same campaign"
    ]
    
    return IOCSearchResult(
        total_results=len(results),
        query=query,
        iocs=results[:limit],
        search_time_ms=round(search_time, 2),
        related_searches=related_searches
    )


@router.get("/enrich/{ioc_value}", response_model=IOCEnrichment)
async def enrich_ioc(
    ioc_value: str,
    include_malware_analysis: bool = Query(True, description="Include malware sandbox results")
):
    """
    Enrich an IOC with comprehensive threat intelligence data.
    """
    
    ioc_type = detect_ioc_type(ioc_value)
    
    # Calculate reputation score (0-100, lower is worse)
    reputation_score = int(np.random.uniform(5, 40))  # Bad reputation
    
    # Threat intelligence data
    threat_intelligence = {
        "verdict": "malicious" if reputation_score < 30 else "suspicious",
        "detections": {
            "total_engines": 70,
            "positive_detections": int(reputation_score / 100 * 70),
            "detection_rate": f"{reputation_score}%"
        },
        "community_votes": {
            "malicious": np.random.randint(50, 200),
            "harmless": np.random.randint(5, 20)
        },
        "last_analysis_date": (datetime.now() - timedelta(hours=2)).isoformat(),
        "threat_categories": ["malware", "phishing", "c2_server"]
    }
    
    # Geolocation (for IP addresses)
    geolocation = None
    if ioc_type == "ip":
        geolocation = {
            "country": np.random.choice(["Russia", "China", "North Korea", "Iran", "Unknown"]),
            "city": "Moscow",
            "latitude": "55.7558",
            "longitude": "37.6173",
            "asn": f"AS{np.random.randint(10000, 99999)}",
            "isp": "Suspicious Hosting Ltd."
        }
    
    # WHOIS data (for domains)
    whois_data = None
    if ioc_type == "domain":
        whois_data = {
            "registrar": "Malicious Registrar Inc.",
            "creation_date": (datetime.now() - timedelta(days=45)).strftime("%Y-%m-%d"),
            "expiration_date": (datetime.now() + timedelta(days=320)).strftime("%Y-%m-%d"),
            "registrant": "REDACTED FOR PRIVACY",
            "name_servers": ["ns1.suspicious.com", "ns2.suspicious.com"],
            "status": ["clientTransferProhibited"]
        }
    
    # Related IOCs
    related_iocs = []
    for i in range(5):
        related_value, related_type = generate_synthetic_ioc(None)
        related_iocs.append(f"{related_type}:{related_value}")
    
    # Malware analysis (for file hashes)
    malware_analysis = None
    if include_malware_analysis and ioc_type == "hash":
        malware_analysis = {
            "sandbox_environment": "Cuckoo Sandbox",
            "analysis_date": datetime.now().isoformat(),
            "malware_family": "TrickBot",
            "file_type": "PE32 executable",
            "size_bytes": 2458624,
            "behaviors": [
                "Registry modification detected",
                "Network communication to C2 server",
                "Credential dumping attempts",
                "Keylogging activity",
                "Lateral movement techniques"
            ],
            "network_indicators": [
                "185.220.101.45:443",
                "malicious-c2.com:8080"
            ],
            "dropped_files": [
                "C:\\Windows\\Temp\\malware.dll",
                "C:\\Users\\Admin\\AppData\\payload.exe"
            ],
            "mitre_techniques": [
                "T1055 - Process Injection",
                "T1071 - Application Layer Protocol",
                "T1082 - System Information Discovery"
            ]
        }
    
    # Detection rules
    detection_rules = [
        "Snort: alert tcp any any -> any 443 (msg:\"Malicious SSL Certificate\"; content:\"|16 03|\"; sid:1000001;)",
        "Yara: rule Malware_Family { strings: $a = \"malicious_string\" condition: $a }",
        "Sigma: Detection of suspicious PowerShell commands",
        "Suricata: ET MALWARE Known Bad SSL Cert"
    ]
    
    # Recommendations
    recommendations = [
        f"BLOCK: Immediately block {ioc_value} at network perimeter",
        "HUNT: Search for related IOCs in your environment",
        "MONITOR: Set up alerts for any future detections",
        "INVESTIGATE: Review logs for any past connections to this IOC",
        "UPDATE: Ensure EDR/AV signatures are current"
    ]
    
    return IOCEnrichment(
        ioc_value=ioc_value,
        ioc_type=ioc_type,
        reputation_score=reputation_score,
        threat_intelligence=threat_intelligence,
        geolocation=geolocation,
        whois_data=whois_data,
        related_iocs=related_iocs,
        malware_analysis=malware_analysis,
        detection_rules=detection_rules,
        recommendations=recommendations
    )


@router.get("/correlate/{ioc_value}", response_model=IOCCorrelation)
async def correlate_iocs(ioc_value: str):
    """
    Find correlations between IOCs to identify campaigns and infrastructure.
    """
    
    # Generate related IOCs with correlation metadata
    related = []
    
    relationship_types = [
        "same_campaign",
        "same_infrastructure", 
        "same_threat_actor",
        "temporal_correlation",
        "behavioral_similarity"
    ]
    
    for i in range(8):
        related_value, related_type = generate_synthetic_ioc(None)
        relationship = np.random.choice(relationship_types)
        
        related.append({
            "ioc_value": related_value,
            "ioc_type": related_type,
            "relationship": relationship,
            "correlation_score": round(np.random.uniform(0.6, 0.95), 2),
            "first_seen": (datetime.now() - timedelta(days=np.random.randint(1, 60))).isoformat(),
            "shared_attributes": np.random.choice([
                "Same C2 server",
                "Same malware family",
                "Same attack pattern",
                "Same TTPs",
                "Temporal proximity"
            ], size=2, replace=False).tolist()
        })
    
    # Generate timeline of correlated activity
    timeline = []
    for i in range(10):
        event_date = datetime.now() - timedelta(days=i*3)
        timeline.append({
            "timestamp": event_date.isoformat(),
            "event_type": np.random.choice([
                "IOC detected",
                "Campaign activity",
                "Infrastructure change",
                "Threat actor activity"
            ]),
            "description": f"Related activity observed involving {np.random.randint(2, 8)} correlated IOCs"
        })
    
    return IOCCorrelation(
        correlation_id=f"corr_{np.random.randint(10000, 99999)}",
        primary_ioc=ioc_value,
        related_iocs=related,
        correlation_score=round(np.random.uniform(0.75, 0.95), 2),
        relationship_type=np.random.choice(relationship_types),
        timeline=timeline
    )


@router.get("/feeds", response_model=List[IOCFeed])
async def get_ioc_feeds():
    """
    Get status and statistics for IOC threat intelligence feeds.
    """
    
    feeds = [
        {
            "name": "VirusTotal",
            "total_iocs": 15_234_567,
            "new_24h": 1_245,
            "critical": 89
        },
        {
            "name": "AlienVault OTX",
            "total_iocs": 8_456_123,
            "new_24h": 987,
            "critical": 56
        },
        {
            "name": "Abuse.ch",
            "total_iocs": 3_123_456,
            "new_24h": 456,
            "critical": 34
        },
        {
            "name": "MISP Threat Sharing",
            "total_iocs": 5_678_901,
            "new_24h": 678,
            "critical": 45
        },
        {
            "name": "ThreatFox",
            "total_iocs": 2_345_678,
            "new_24h": 234,
            "critical": 23
        }
    ]
    
    return [
        IOCFeed(
            feed_name=feed["name"],
            last_updated=(datetime.now() - timedelta(minutes=np.random.randint(5, 60))).isoformat(),
            total_iocs=feed["total_iocs"],
            new_iocs_24h=feed["new_24h"],
            critical_iocs=feed["critical"],
            feed_reliability=np.random.choice(["excellent", "good", "moderate"])
        )
        for feed in feeds
    ]


@router.post("/bulk-check")
async def bulk_ioc_check(iocs: List[str]):
    """
    Check multiple IOCs in a single request.
    """
    
    results = []
    for ioc in iocs[:100]:  # Limit to 100 IOCs
        ioc_type = detect_ioc_type(ioc)
        threat_level = np.random.choice(["critical", "high", "medium", "low", "clean"], p=[0.05, 0.15, 0.25, 0.30, 0.25])
        
        results.append({
            "ioc": ioc,
            "type": ioc_type,
            "threat_level": threat_level,
            "found_in_feeds": np.random.randint(0, 5),
            "confidence": round(np.random.uniform(0.6, 0.95), 2) if threat_level != "clean" else 0
        })
    
    return {
        "total_checked": len(iocs),
        "malicious_count": len([r for r in results if r["threat_level"] in ["critical", "high"]]),
        "suspicious_count": len([r for r in results if r["threat_level"] == "medium"]),
        "clean_count": len([r for r in results if r["threat_level"] == "clean"]),
        "results": results
    }


# Helper functions
def detect_ioc_type(value: str) -> str:
    """Detect IOC type from value."""
    # IP address pattern
    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', value):
        return "ip"
    # Domain pattern
    elif re.match(r'^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]?\.([a-zA-Z]{2,}|[a-zA-Z]{2,}\.[a-zA-Z]{2,})$', value):
        return "domain"
    # Email pattern
    elif '@' in value and '.' in value:
        return "email"
    # Hash pattern (MD5, SHA1, SHA256)
    elif re.match(r'^[a-fA-F0-9]{32}$|^[a-fA-F0-9]{40}$|^[a-fA-F0-9]{64}$', value):
        return "hash"
    # URL pattern
    elif value.startswith(('http://', 'https://', 'ftp://')):
        return "url"
    else:
        return "unknown"


def generate_synthetic_ioc(ioc_type: Optional[str] = None):
    """Generate synthetic IOC for testing."""
    if not ioc_type:
        ioc_type = np.random.choice(["ip", "domain", "hash", "email", "url"])
    
    if ioc_type == "ip":
        return f"{np.random.randint(1,255)}.{np.random.randint(1,255)}.{np.random.randint(1,255)}.{np.random.randint(1,255)}", "ip"
    elif ioc_type == "domain":
        return f"malicious-{np.random.randint(1000,9999)}.com", "domain"
    elif ioc_type == "hash":
        return f"{''.join([np.random.choice('0123456789abcdef') for _ in range(64)])}", "hash"
    elif ioc_type == "email":
        return f"attacker{np.random.randint(100,999)}@evil-domain.com", "email"
    elif ioc_type == "url":
        return f"https://malicious-site-{np.random.randint(1000,9999)}.com/payload", "url"
    
    return "unknown", "unknown"

