"""MITRE ATT&CK framework endpoints for detection coverage and threat modeling"""

from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import numpy as np

router = APIRouter(prefix="/api/mitre", tags=["mitre-attack"])

class AttackTechnique(BaseModel):
    technique_id: str
    technique_name: str
    tactic: str
    sub_techniques: List[str]
    description: str
    detection_coverage: str  # "none", "partial", "good", "excellent"
    detection_score: float  # 0-1 scale
    threat_actors_using: List[str]
    recent_detections: int
    mitigation_implemented: bool
    data_sources: List[str]
    platforms: List[str]

class TacticCoverage(BaseModel):
    tactic_name: str
    tactic_id: str
    total_techniques: int
    covered_techniques: int
    coverage_percentage: float
    gap_count: int
    priority_gaps: List[str]

class CoverageMatrix(BaseModel):
    tactics: List[TacticCoverage]
    techniques: List[AttackTechnique]
    overall_coverage: float
    total_techniques: int
    covered_techniques: int
    gap_techniques: int
    last_updated: str

class ThreatActorTTPs(BaseModel):
    threat_actor: str
    techniques_used: List[Dict[str, Any]]
    tactics_distribution: Dict[str, int]
    detection_coverage: float
    high_risk_techniques: List[str]

class GapAnalysis(BaseModel):
    critical_gaps: List[Dict[str, Any]]
    recommended_detections: List[Dict[str, Any]]
    risk_score: float
    priority_order: List[str]

class DetectionRule(BaseModel):
    rule_id: str
    rule_name: str
    technique_ids: List[str]
    data_source: str
    logic: str
    false_positive_rate: str
    effectiveness: str

# MITRE ATT&CK Tactics (ordered by kill chain)
MITRE_TACTICS = [
    {"id": "TA0043", "name": "Reconnaissance"},
    {"id": "TA0042", "name": "Resource Development"},
    {"id": "TA0001", "name": "Initial Access"},
    {"id": "TA0002", "name": "Execution"},
    {"id": "TA0003", "name": "Persistence"},
    {"id": "TA0004", "name": "Privilege Escalation"},
    {"id": "TA0005", "name": "Defense Evasion"},
    {"id": "TA0006", "name": "Credential Access"},
    {"id": "TA0007", "name": "Discovery"},
    {"id": "TA0008", "name": "Lateral Movement"},
    {"id": "TA0009", "name": "Collection"},
    {"id": "TA0011", "name": "Command and Control"},
    {"id": "TA0010", "name": "Exfiltration"},
    {"id": "TA0040", "name": "Impact"}
]

# Sample techniques for each tactic
TECHNIQUE_TEMPLATES = {
    "Reconnaissance": [
        ("T1595", "Active Scanning"),
        ("T1592", "Gather Victim Host Information"),
        ("T1589", "Gather Victim Identity Information"),
        ("T1590", "Gather Victim Network Information")
    ],
    "Initial Access": [
        ("T1566", "Phishing"),
        ("T1190", "Exploit Public-Facing Application"),
        ("T1133", "External Remote Services"),
        ("T1078", "Valid Accounts"),
        ("T1091", "Replication Through Removable Media")
    ],
    "Execution": [
        ("T1059", "Command and Scripting Interpreter"),
        ("T1203", "Exploitation for Client Execution"),
        ("T1053", "Scheduled Task/Job"),
        ("T1204", "User Execution"),
        ("T1047", "Windows Management Instrumentation")
    ],
    "Persistence": [
        ("T1098", "Account Manipulation"),
        ("T1547", "Boot or Logon Autostart Execution"),
        ("T1136", "Create Account"),
        ("T1543", "Create or Modify System Process"),
        ("T1053", "Scheduled Task/Job")
    ],
    "Privilege Escalation": [
        ("T1548", "Abuse Elevation Control Mechanism"),
        ("T1134", "Access Token Manipulation"),
        ("T1068", "Exploitation for Privilege Escalation"),
        ("T1574", "Hijack Execution Flow"),
        ("T1055", "Process Injection")
    ],
    "Defense Evasion": [
        ("T1562", "Impair Defenses"),
        ("T1070", "Indicator Removal"),
        ("T1036", "Masquerading"),
        ("T1027", "Obfuscated Files or Information"),
        ("T1055", "Process Injection"),
        ("T1218", "System Binary Proxy Execution")
    ],
    "Credential Access": [
        ("T1110", "Brute Force"),
        ("T1555", "Credentials from Password Stores"),
        ("T1212", "Exploitation for Credential Access"),
        ("T1056", "Input Capture"),
        ("T1003", "OS Credential Dumping")
    ],
    "Discovery": [
        ("T1087", "Account Discovery"),
        ("T1083", "File and Directory Discovery"),
        ("T1046", "Network Service Discovery"),
        ("T1135", "Network Share Discovery"),
        ("T1057", "Process Discovery"),
        ("T1082", "System Information Discovery")
    ],
    "Lateral Movement": [
        ("T1210", "Exploitation of Remote Services"),
        ("T1534", "Internal Spearphishing"),
        ("T1570", "Lateral Tool Transfer"),
        ("T1021", "Remote Services"),
        ("T1080", "Taint Shared Content")
    ],
    "Collection": [
        ("T1560", "Archive Collected Data"),
        ("T1123", "Audio Capture"),
        ("T1115", "Clipboard Data"),
        ("T1005", "Data from Local System"),
        ("T1039", "Data from Network Shared Drive"),
        ("T1025", "Data from Removable Media")
    ],
    "Command and Control": [
        ("T1071", "Application Layer Protocol"),
        ("T1092", "Communication Through Removable Media"),
        ("T1132", "Data Encoding"),
        ("T1001", "Data Obfuscation"),
        ("T1568", "Dynamic Resolution"),
        ("T1573", "Encrypted Channel")
    ],
    "Exfiltration": [
        ("T1020", "Automated Exfiltration"),
        ("T1030", "Data Transfer Size Limits"),
        ("T1048", "Exfiltration Over Alternative Protocol"),
        ("T1041", "Exfiltration Over C2 Channel"),
        ("T1011", "Exfiltration Over Other Network Medium")
    ],
    "Impact": [
        ("T1531", "Account Access Removal"),
        ("T1485", "Data Destruction"),
        ("T1486", "Data Encrypted for Impact"),
        ("T1491", "Defacement"),
        ("T1489", "Service Stop"),
        ("T1490", "Inhibit System Recovery")
    ]
}

@router.get("/coverage-matrix", response_model=CoverageMatrix)
async def get_coverage_matrix(
    include_sub_techniques: bool = Query(False, description="Include sub-techniques in analysis")
):
    """
    Get complete MITRE ATT&CK coverage matrix with detection capabilities.
    """
    
    tactics_coverage = []
    all_techniques = []
    
    total_covered = 0
    total_techniques_count = 0
    
    for tactic in MITRE_TACTICS:
        tactic_name = tactic["name"]
        tactic_id = tactic["id"]
        
        # Get techniques for this tactic
        techniques_list = TECHNIQUE_TEMPLATES.get(tactic_name, [])
        
        covered_count = 0
        gap_techniques = []
        
        for tech_id, tech_name in techniques_list:
            # Generate detection coverage (weighted towards partial/good)
            coverage_levels = ["none", "partial", "good", "excellent"]
            coverage_weights = [0.15, 0.35, 0.35, 0.15]
            coverage = np.random.choice(coverage_levels, p=coverage_weights)
            
            detection_score = {
                "none": 0.0,
                "partial": 0.4,
                "good": 0.7,
                "excellent": 0.95
            }[coverage]
            
            if coverage != "none":
                covered_count += 1
                total_covered += 1
            else:
                gap_techniques.append(tech_name)
            
            total_techniques_count += 1
            
            # Generate threat actors using this technique
            threat_actors = []
            if np.random.random() > 0.6:  # 40% chance of known actor
                threat_actors = np.random.choice([
                    "APT28", "APT29", "Lazarus Group", "FIN7", 
                    "DarkSide", "Carbanak", "Equation Group"
                ], size=np.random.randint(1, 3), replace=False).tolist()
            
            # Recent detections
            recent_detections = 0
            if coverage != "none":
                recent_detections = int(np.random.exponential(5))
            
            # Generate sub-techniques
            sub_techniques = []
            if include_sub_techniques:
                num_sub = np.random.randint(0, 4)
                sub_techniques = [f"{tech_id}.{str(i+1).zfill(3)}" for i in range(num_sub)]
            
            all_techniques.append(AttackTechnique(
                technique_id=tech_id,
                technique_name=tech_name,
                tactic=tactic_name,
                sub_techniques=sub_techniques,
                description=f"Adversaries may {tech_name.lower()} to achieve their objectives.",
                detection_coverage=coverage,
                detection_score=detection_score,
                threat_actors_using=threat_actors,
                recent_detections=recent_detections,
                mitigation_implemented=np.random.random() > 0.3,
                data_sources=np.random.choice([
                    "Process monitoring",
                    "File monitoring",
                    "Network traffic",
                    "Windows event logs",
                    "Authentication logs",
                    "Command execution"
                ], size=np.random.randint(1, 4), replace=False).tolist(),
                platforms=np.random.choice([
                    "Windows", "Linux", "macOS", "Cloud"
                ], size=np.random.randint(1, 3), replace=False).tolist()
            ))
        
        coverage_percentage = (covered_count / len(techniques_list) * 100) if techniques_list else 0
        
        tactics_coverage.append(TacticCoverage(
            tactic_name=tactic_name,
            tactic_id=tactic_id,
            total_techniques=len(techniques_list),
            covered_techniques=covered_count,
            coverage_percentage=round(coverage_percentage, 1),
            gap_count=len(gap_techniques),
            priority_gaps=gap_techniques[:3]  # Top 3 gaps
        ))
    
    overall_coverage = (total_covered / total_techniques_count * 100) if total_techniques_count > 0 else 0
    
    return CoverageMatrix(
        tactics=tactics_coverage,
        techniques=all_techniques,
        overall_coverage=round(overall_coverage, 1),
        total_techniques=total_techniques_count,
        covered_techniques=total_covered,
        gap_techniques=total_techniques_count - total_covered,
        last_updated=datetime.now().isoformat()
    )


@router.get("/threat-actor-ttps/{actor_name}", response_model=ThreatActorTTPs)
async def get_threat_actor_ttps(actor_name: str):
    """
    Get MITRE ATT&CK techniques used by a specific threat actor.
    """
    
    # Generate techniques used by this actor
    techniques_used = []
    tactics_dist = {}
    
    # Randomly select techniques across different tactics
    num_techniques = np.random.randint(12, 25)
    
    for tactic in MITRE_TACTICS[:10]:  # Use first 10 tactics
        tactic_name = tactic["name"]
        techniques_list = TECHNIQUE_TEMPLATES.get(tactic_name, [])
        
        if techniques_list:
            # Select 1-3 techniques from this tactic
            num_from_tactic = min(np.random.randint(1, 4), len(techniques_list))
            selected = np.random.choice(len(techniques_list), size=num_from_tactic, replace=False)
            
            for idx in selected:
                tech_id, tech_name = techniques_list[idx]
                
                # Check if we have detection coverage
                has_detection = np.random.random() > 0.3
                
                techniques_used.append({
                    "technique_id": tech_id,
                    "technique_name": tech_name,
                    "tactic": tactic_name,
                    "frequency": np.random.choice(["common", "occasional", "rare"]),
                    "first_observed": (datetime.now() - timedelta(days=np.random.randint(30, 730))).strftime("%Y-%m-%d"),
                    "last_observed": (datetime.now() - timedelta(days=np.random.randint(0, 30))).strftime("%Y-%m-%d"),
                    "detection_coverage": has_detection,
                    "severity": np.random.choice(["critical", "high", "medium"])
                })
                
                tactics_dist[tactic_name] = tactics_dist.get(tactic_name, 0) + 1
    
    # Calculate detection coverage
    covered = sum(1 for t in techniques_used if t["detection_coverage"])
    detection_coverage = covered / len(techniques_used) if techniques_used else 0
    
    # Identify high-risk techniques (those we don't detect)
    high_risk = [
        f"{t['technique_id']} - {t['technique_name']}" 
        for t in techniques_used 
        if not t["detection_coverage"] and t["severity"] in ["critical", "high"]
    ]
    
    return ThreatActorTTPs(
        threat_actor=actor_name,
        techniques_used=techniques_used,
        tactics_distribution=tactics_dist,
        detection_coverage=round(detection_coverage, 2),
        high_risk_techniques=high_risk[:5]  # Top 5 risks
    )


@router.get("/gap-analysis", response_model=GapAnalysis)
async def get_gap_analysis():
    """
    Identify critical detection gaps and provide recommendations.
    """
    
    critical_gaps = []
    
    # Generate critical gaps
    high_priority_tactics = ["Initial Access", "Execution", "Persistence", "Defense Evasion", "Credential Access"]
    
    for tactic in high_priority_tactics:
        techniques = TECHNIQUE_TEMPLATES.get(tactic, [])
        if techniques:
            # Pick 2-3 gaps per tactic
            num_gaps = min(np.random.randint(2, 4), len(techniques))
            for i in range(num_gaps):
                tech_id, tech_name = techniques[i]
                
                critical_gaps.append({
                    "technique_id": tech_id,
                    "technique_name": tech_name,
                    "tactic": tactic,
                    "risk_level": np.random.choice(["critical", "high", "medium"], p=[0.3, 0.5, 0.2]),
                    "threat_actors_using": np.random.randint(2, 8),
                    "recent_campaigns": np.random.randint(1, 5),
                    "estimated_effort": np.random.choice(["Low", "Medium", "High"]),
                    "estimated_time": np.random.choice(["1-2 weeks", "2-4 weeks", "1-2 months"])
                })
    
    # Sort by risk level
    risk_order = {"critical": 3, "high": 2, "medium": 1}
    critical_gaps.sort(key=lambda x: risk_order.get(x["risk_level"], 0), reverse=True)
    
    # Generate recommendations
    recommended_detections = []
    
    for gap in critical_gaps[:10]:  # Top 10 gaps
        recommended_detections.append({
            "technique_id": gap["technique_id"],
            "technique_name": gap["technique_name"],
            "recommended_data_source": np.random.choice([
                "Sysmon Event Logs",
                "EDR Telemetry",
                "Network Flow Data",
                "Authentication Logs",
                "Process Creation Events"
            ]),
            "detection_method": np.random.choice([
                "Behavioral Analytics",
                "Signature-based",
                "Anomaly Detection",
                "Threat Intelligence Feed",
                "Machine Learning Model"
            ]),
            "implementation_priority": gap["risk_level"],
            "expected_false_positive_rate": np.random.choice(["Low", "Medium", "High"])
        })
    
    # Calculate overall risk score
    risk_score = len([g for g in critical_gaps if g["risk_level"] == "critical"]) * 10 + \
                  len([g for g in critical_gaps if g["risk_level"] == "high"]) * 5
    risk_score = min(100, risk_score)  # Cap at 100
    
    # Priority order for implementation
    priority_order = [
        "Implement EDR/XDR solution",
        "Deploy Sysmon across endpoints",
        "Enable PowerShell logging",
        "Implement network traffic analysis",
        "Deploy UEBA for anomaly detection",
        "Enable command-line auditing",
        "Implement file integrity monitoring",
        "Deploy deception technology"
    ]
    
    return GapAnalysis(
        critical_gaps=critical_gaps[:15],  # Top 15 gaps
        recommended_detections=recommended_detections,
        risk_score=risk_score,
        priority_order=priority_order
    )


@router.get("/detection-rules/{technique_id}", response_model=List[DetectionRule])
async def get_detection_rules(technique_id: str):
    """
    Get detection rules for a specific MITRE ATT&CK technique.
    """
    
    rules = []
    
    # Generate 3-5 detection rules
    num_rules = np.random.randint(3, 6)
    
    rule_types = ["Sigma", "Yara", "Snort", "Suricata", "KQL", "SPL"]
    
    for i in range(num_rules):
        rule_type = np.random.choice(rule_types)
        
        rules.append(DetectionRule(
            rule_id=f"RULE-{np.random.randint(10000, 99999)}",
            rule_name=f"{rule_type} - Detect {technique_id}",
            technique_ids=[technique_id],
            data_source=np.random.choice([
                "Windows Event Logs",
                "Sysmon",
                "Network Traffic",
                "Process Monitoring",
                "File System"
            ]),
            logic=f"title: Detects {technique_id}\nlogsource:\n  category: process_creation\ndetection:\n  selection:\n    - CommandLine|contains: 'suspicious_pattern'\n  condition: selection",
            false_positive_rate=np.random.choice(["Low", "Medium", "High"]),
            effectiveness=np.random.choice(["Excellent", "Good", "Moderate"])
        ))
    
    return rules


@router.get("/technique-details/{technique_id}")
async def get_technique_details(technique_id: str):
    """
    Get comprehensive details for a specific technique.
    """
    
    return {
        "technique_id": technique_id,
        "name": "Example Technique Name",
        "description": "Detailed description of the adversary technique and how it works.",
        "tactics": ["Initial Access", "Execution"],
        "platforms": ["Windows", "Linux", "macOS"],
        "data_sources": [
            "Process monitoring",
            "File monitoring", 
            "Network traffic analysis"
        ],
        "detection_methods": [
            "Monitor for unusual process execution",
            "Analyze command-line arguments",
            "Correlate with authentication events"
        ],
        "mitigations": [
            "M1038 - Execution Prevention",
            "M1026 - Privileged Account Management",
            "M1018 - User Account Management"
        ],
        "examples": [
            {
                "name": "APT28 Campaign",
                "description": "APT28 has used this technique in spearphishing campaigns",
                "source": "MITRE ATT&CK"
            }
        ],
        "references": [
            "https://attack.mitre.org/techniques/T1566/",
            "https://www.fireeye.com/blog/threat-research/..."
        ]
    }


@router.get("/tactic-summary/{tactic_name}")
async def get_tactic_summary(tactic_name: str):
    """
    Get summary statistics for a specific tactic.
    """
    
    techniques = TECHNIQUE_TEMPLATES.get(tactic_name, [])
    
    # Calculate coverage stats
    covered = int(len(techniques) * np.random.uniform(0.5, 0.9))
    
    return {
        "tactic_name": tactic_name,
        "total_techniques": len(techniques),
        "covered_techniques": covered,
        "coverage_percentage": round((covered / len(techniques) * 100) if techniques else 0, 1),
        "common_data_sources": [
            "Process monitoring",
            "File monitoring",
            "Network traffic",
            "Windows event logs"
        ],
        "threat_actor_usage": {
            "high": np.random.randint(5, 15),
            "medium": np.random.randint(10, 25),
            "low": np.random.randint(15, 40)
        },
        "top_techniques_by_usage": [
            {"id": t[0], "name": t[1], "usage_count": np.random.randint(10, 50)}
            for t in techniques[:5]
        ]
    }
