"""Threat timeline endpoints for comprehensive threat intelligence visualization"""

from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from collections import Counter
import numpy as np
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["threat-timeline"])

class ThreatEvent(BaseModel):
    event_id: str
    timestamp: str
    event_type: str  # "detection", "attack", "ioc", "mitigation", "alert"
    severity: str  # "critical", "high", "medium", "low", "info"
    title: str
    description: str
    threat_actor: Optional[str]
    attack_vector: Optional[str]
    affected_systems: List[str]
    iocs: List[str]
    mitre_tactics: List[str]
    status: str  # "ongoing", "mitigated", "investigating", "resolved"

class ThreatCampaign(BaseModel):
    campaign_id: str
    name: str
    threat_actor: str
    start_date: str
    end_date: Optional[str]
    total_events: int
    severity: str
    targeted_sectors: List[str]
    attack_vectors: List[str]
    success_rate: float

class TimelineAnalysis(BaseModel):
    total_events: int
    date_range: Dict[str, str]
    events: List[ThreatEvent]
    campaigns: List[ThreatCampaign]
    attack_pattern_insights: List[str]
    trending_threats: List[Dict[str, Any]]

class AttackChain(BaseModel):
    chain_id: str
    campaign_name: str
    stages: List[Dict[str, Any]]
    total_duration: str
    kill_chain_phase: str

@router.get("/events", response_model=TimelineAnalysis)
async def get_threat_timeline(
    days_back: int = Query(30, description="Number of days to analyze"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    threat_actor: Optional[str] = Query(None, description="Filter by threat actor"),
    event_type: Optional[str] = Query(None, description="Filter by event type")
):
    """
    Get comprehensive threat intelligence timeline with events, campaigns, and analysis.
    """
    try:
        # Ensure days_back is valid
        if days_back < 1:
            days_back = 30
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Threat actors database
        threat_actors = [
            "APT28 (Fancy Bear)",
            "APT29 (Cozy Bear)",
            "Lazarus Group",
            "Equation Group",
            "Carbanak",
            "FIN7",
            "DarkSide",
            "REvil",
            "Conti"
        ]
        
        # Attack vectors
        attack_vectors = [
            "Phishing",
            "Ransomware",
            "SQL Injection",
            "Zero-Day Exploit",
            "Credential Stuffing",
            "DDoS",
            "Supply Chain Attack",
            "Watering Hole",
            "Malvertising"
        ]
        
        # Generate synthetic threat events
        events = []
        num_events = np.random.randint(40, 80)
        
        for i in range(num_events):
            event_date = start_date + timedelta(
                days=np.random.randint(0, days_back),
                hours=np.random.randint(0, 24)
            )
            
            event_types = ["detection", "attack", "ioc", "mitigation", "alert"]
            severities = ["critical", "high", "medium", "low", "info"]
            
            # Weighted severity distribution (more medium/low, fewer critical)
            severity_weights = [0.1, 0.2, 0.4, 0.2, 0.1]
            selected_severity = np.random.choice(severities, p=severity_weights)
            
            selected_type = np.random.choice(event_types)
            selected_actor = np.random.choice(threat_actors + [None, None, None])  # Some unknown
            selected_vector = np.random.choice(attack_vectors)
            
            # Generate IOCs
            iocs = []
            if selected_type in ["detection", "attack", "ioc"]:
                num_iocs = np.random.randint(1, 5)
                for _ in range(num_iocs):
                    ioc_type = np.random.choice(["ip", "domain", "hash", "email"])
                    if ioc_type == "ip":
                        iocs.append(f"{np.random.randint(1,255)}.{np.random.randint(1,255)}.{np.random.randint(1,255)}.{np.random.randint(1,255)}")
                    elif ioc_type == "domain":
                        iocs.append(f"malicious-{np.random.randint(1000,9999)}.com")
                    elif ioc_type == "hash":
                        # Generate a random hex string for hash (avoiding int32 overflow)
                        hash_value = ''.join([f'{np.random.randint(0, 16):x}' for _ in range(64)])
                        iocs.append(f"SHA256:{hash_value}")
                    else:
                        iocs.append(f"phishing@attacker-{np.random.randint(100,999)}.com")
            
            # MITRE ATT&CK tactics
            mitre_tactics = np.random.choice([
                "Initial Access",
                "Execution",
                "Persistence",
                "Privilege Escalation",
                "Defense Evasion",
                "Credential Access",
                "Discovery",
                "Lateral Movement",
                "Collection",
                "Command and Control",
                "Exfiltration",
                "Impact"
            ], size=np.random.randint(1, 4), replace=False).tolist()
            
            # Generate event title and description
            titles = {
                "detection": f"Malicious Activity Detected via {selected_vector}",
                "attack": f"{selected_vector} Attack in Progress",
                "ioc": f"New IOCs Identified - {selected_vector} Campaign",
                "mitigation": f"Threat Mitigated - {selected_vector}",
                "alert": f"Security Alert - Suspicious {selected_vector} Activity"
            }
            
            descriptions = {
                "detection": f"Automated detection systems identified suspicious {selected_vector} activity targeting critical infrastructure.",
                "attack": f"Active {selected_vector} attack detected with potential data exfiltration attempts.",
                "ioc": f"Threat intelligence feeds identified new indicators associated with {selected_vector} campaigns.",
                "mitigation": f"Security team successfully blocked and contained {selected_vector} threat.",
                "alert": f"Multiple security sensors triggered alerts for potential {selected_vector} activity."
            }
            
            statuses = ["ongoing", "mitigated", "investigating", "resolved"]
            status_weights = [0.15, 0.35, 0.25, 0.25]
            
            events.append(ThreatEvent(
                event_id=f"evt_{i+1:04d}",
                timestamp=event_date.isoformat(),
                event_type=selected_type,
                severity=selected_severity,
                title=titles[selected_type],
                description=descriptions[selected_type],
                threat_actor=selected_actor,
                attack_vector=selected_vector,
                affected_systems=[
                    f"server-{np.random.randint(1,50):02d}",
                    f"workstation-{np.random.randint(1,200):03d}"
                ],
                iocs=iocs,
                mitre_tactics=mitre_tactics,
                status=np.random.choice(statuses, p=status_weights)
            ))
        
        # Sort events by timestamp
        events.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Apply filters
        if severity:
            events = [e for e in events if e.severity == severity]
        if threat_actor:
            events = [e for e in events if e.threat_actor == threat_actor]
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        # Generate campaigns (grouped related events)
        campaigns = []
        if len(threat_actors) >= 3 and days_back >= 7 and len(events) > 0:
            # Get unique threat actors from filtered events
            available_actors = list(set([e.threat_actor for e in events if e.threat_actor]))
            
            if len(available_actors) >= 2:  # Need at least 2 actors for campaigns
                num_campaigns = min(6, len(available_actors))
                campaign_size = min(num_campaigns, max(2, len(available_actors)))
                
                if campaign_size >= 2:
                    try:
                        campaign_actors = np.random.choice(available_actors, size=min(campaign_size, len(available_actors)), replace=False).tolist()
                    except ValueError:
                        # Fallback if numpy choice fails
                        campaign_actors = available_actors[:campaign_size]
                    
                    for idx, actor in enumerate(campaign_actors):
                        max_start_day = max(1, days_back - 7)
                        # Ensure we have a valid range for random.randint
                        if max_start_day <= 0:
                            max_start_day = 1
                        campaign_start_offset = np.random.randint(0, max(max_start_day, 1))
                        campaign_start = start_date + timedelta(days=campaign_start_offset)
                        campaign_duration = np.random.randint(3, 14)
                        campaign_end = campaign_start + timedelta(days=campaign_duration)
                        
                        # Count events in this campaign
                        campaign_events = [
                            e for e in events 
                            if e.threat_actor == actor and 
                            campaign_start <= datetime.fromisoformat(e.timestamp) <= campaign_end
                        ]
                        
                        if len(campaign_events) > 0:
                            try:
                                # Get unique sectors list
                                sectors_list = [
                                    "Financial Services",
                                    "Healthcare",
                                    "Government",
                                    "Energy",
                                    "Technology",
                                    "Manufacturing"
                                ]
                                num_sectors = min(np.random.randint(1, 3), len(sectors_list))
                                selected_sectors = np.random.choice(sectors_list, size=num_sectors, replace=False).tolist()
                                
                                campaigns.append(ThreatCampaign(
                                    campaign_id=f"camp_{idx+1:03d}",
                                    name=f"Operation {actor.split()[0]} {np.random.choice(['Storm', 'Shadow', 'Phantom', 'Viper', 'Dragon'])}",
                                    threat_actor=actor,
                                    start_date=campaign_start.strftime("%Y-%m-%d"),
                                    end_date=campaign_end.strftime("%Y-%m-%d") if campaign_end <= end_date else None,
                                    total_events=len(campaign_events),
                                    severity=max([e.severity for e in campaign_events], key=lambda s: ["info", "low", "medium", "high", "critical"].index(s)),
                                    targeted_sectors=selected_sectors,
                                    attack_vectors=list(set([e.attack_vector for e in campaign_events if e.attack_vector])),
                                    success_rate=round(np.random.uniform(0.3, 0.8), 2)
                                ))
                            except Exception as e:
                                # Skip this campaign if there's an error
                                continue
        
        # Generate insights
        attack_vectors_list = [e.attack_vector for e in events if e.attack_vector]
        most_common_vector = 'N/A'
        if attack_vectors_list:
            vector_counts = Counter(attack_vectors_list)
            most_common_vector = vector_counts.most_common(1)[0][0] if vector_counts else 'N/A'
        
        attack_pattern_insights = [
            f"Detected {len([e for e in events if e.severity in ['critical', 'high']])} high-severity threats in the past {days_back} days",
            f"Most common attack vector: {most_common_vector}",
            f"{len([e for e in events if e.status == 'mitigated'])} threats successfully mitigated",
            f"Average time to detection: {np.random.randint(15, 120)} minutes",
            f"{len(campaigns)} active threat campaigns identified"
        ]
        
        # Trending threats (attack vectors with increasing frequency)
        attack_vector_counts = {}
        for event in events:
            if event.attack_vector:
                attack_vector_counts[event.attack_vector] = attack_vector_counts.get(event.attack_vector, 0) + 1
        
        trending_threats = [
            {
                "name": vector,
                "count": count,
                "trend": "increasing" if np.random.random() > 0.5 else "stable",
                "severity_distribution": {
                    "critical": len([e for e in events if e.attack_vector == vector and e.severity == "critical"]),
                    "high": len([e for e in events if e.attack_vector == vector and e.severity == "high"]),
                    "medium": len([e for e in events if e.attack_vector == vector and e.severity == "medium"])
                }
            }
            for vector, count in sorted(attack_vector_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        ]
    
        return TimelineAnalysis(
            total_events=len(events),
            date_range={
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d")
            },
            events=events[:100],  # Limit to 100 most recent
            campaigns=campaigns,
            attack_pattern_insights=attack_pattern_insights,
            trending_threats=trending_threats
        )
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"Error in get_threat_timeline: {str(e)}\n{error_details}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/attack-chain/{campaign_id}", response_model=AttackChain)
async def get_attack_chain(campaign_id: str):
    """
    Get detailed attack chain (kill chain) for a specific campaign.
    """
    
    # Cyber Kill Chain stages
    stages = [
        {
            "stage": "Reconnaissance",
            "timestamp": (datetime.now() - timedelta(days=15)).isoformat(),
            "description": "Threat actor conducted network scanning and OSINT gathering",
            "indicators": ["Port scanning detected", "DNS enumeration observed"],
            "mitre_technique": "T1595 - Active Scanning"
        },
        {
            "stage": "Weaponization",
            "timestamp": (datetime.now() - timedelta(days=14)).isoformat(),
            "description": "Malicious payload created and packaged with exploit",
            "indicators": ["Custom malware variant identified"],
            "mitre_technique": "T1587 - Develop Capabilities"
        },
        {
            "stage": "Delivery",
            "timestamp": (datetime.now() - timedelta(days=13)).isoformat(),
            "description": "Spear-phishing emails sent to 27 employees",
            "indicators": ["Phishing emails from compromised domain"],
            "mitre_technique": "T1566 - Phishing"
        },
        {
            "stage": "Exploitation",
            "timestamp": (datetime.now() - timedelta(days=12)).isoformat(),
            "description": "Zero-day vulnerability exploited on victim systems",
            "indicators": ["CVE-2024-XXXXX exploitation detected"],
            "mitre_technique": "T1203 - Exploitation for Client Execution"
        },
        {
            "stage": "Installation",
            "timestamp": (datetime.now() - timedelta(days=11)).isoformat(),
            "description": "Remote access trojan (RAT) installed with persistence",
            "indicators": ["Registry modifications", "Scheduled task creation"],
            "mitre_technique": "T1547 - Boot or Logon Autostart Execution"
        },
        {
            "stage": "Command & Control",
            "timestamp": (datetime.now() - timedelta(days=10)).isoformat(),
            "description": "C2 channel established to external infrastructure",
            "indicators": ["Beaconing to 185.XX.XX.XX", "Encrypted traffic anomaly"],
            "mitre_technique": "T1071 - Application Layer Protocol"
        },
        {
            "stage": "Actions on Objectives",
            "timestamp": (datetime.now() - timedelta(days=5)).isoformat(),
            "description": "Data exfiltration and lateral movement observed",
            "indicators": ["Large data transfers", "Credential dumping attempts"],
            "mitre_technique": "T1048 - Exfiltration Over Alternative Protocol"
        }
    ]
    
    return AttackChain(
        chain_id=campaign_id,
        campaign_name="Operation Phantom Shadow",
        stages=stages,
        total_duration="10 days",
        kill_chain_phase="Actions on Objectives"
    )


@router.get("/event-details/{event_id}")
async def get_event_details(event_id: str):
    """
    Get comprehensive details for a specific threat event.
    """
    
    return {
        "event_id": event_id,
        "full_description": "Detailed forensic analysis revealed a sophisticated multi-stage attack leveraging advanced persistence mechanisms and encrypted command-and-control channels. The threat actor utilized living-off-the-land techniques to evade detection, compromising multiple systems across the network infrastructure.",
        "technical_details": {
            "protocol": "HTTPS",
            "port": 443,
            "payload_size": "2.4 MB",
            "encryption": "TLS 1.3"
        },
        "affected_assets": [
            {"hostname": "web-server-01", "ip": "10.0.1.15", "os": "Ubuntu 20.04"},
            {"hostname": "db-server-03", "ip": "10.0.2.47", "os": "Windows Server 2019"}
        ],
        "response_actions": [
            {"timestamp": "2024-11-01T14:30:00Z", "action": "Alert generated", "actor": "SIEM"},
            {"timestamp": "2024-11-01T14:35:00Z", "action": "Incident ticket created", "actor": "SOC Analyst"},
            {"timestamp": "2024-11-01T14:45:00Z", "action": "Network isolation initiated", "actor": "IR Team"},
            {"timestamp": "2024-11-01T15:20:00Z", "action": "Threat contained", "actor": "IR Team"}
        ],
        "forensic_artifacts": [
            "Memory dump captured",
            "Network PCAP collected",
            "Disk image acquired",
            "Event logs preserved"
        ],
        "attribution_confidence": "High",
        "related_campaigns": ["camp_001", "camp_003"]
    }

