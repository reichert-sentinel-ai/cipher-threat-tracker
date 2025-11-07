"""Incident Response Playbook Generator endpoints"""

from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import numpy as np

router = APIRouter(prefix="/api/ir-playbooks", tags=["incident-response"])

class PlaybookStep(BaseModel):
    step_number: int
    phase: str  # "preparation", "detection", "analysis", "containment", "eradication", "recovery", "post-incident"
    action: str
    description: str
    responsible_party: str
    estimated_time: str
    automation_available: bool
    required_tools: List[str]
    success_criteria: List[str]
    escalation_triggers: List[str]

class StakeholderNotification(BaseModel):
    stakeholder_type: str
    notification_trigger: str
    communication_template: str
    notification_method: str
    escalation_threshold: str

class EvidenceItem(BaseModel):
    evidence_type: str
    collection_method: str
    retention_period: str
    chain_of_custody: bool
    legal_hold_required: bool
    storage_location: str

class IncidentPlaybook(BaseModel):
    playbook_id: str
    incident_type: str
    severity: str
    generated_at: str
    estimated_duration: str
    steps: List[PlaybookStep]
    stakeholders: List[StakeholderNotification]
    evidence_collection: List[EvidenceItem]
    mitre_techniques: List[str]
    compliance_requirements: List[str]
    success_metrics: Dict[str, str]

class PlaybookTemplate(BaseModel):
    template_id: str
    name: str
    description: str
    incident_types: List[str]
    complexity: str
    typical_duration: str
    required_skills: List[str]

class IncidentMetrics(BaseModel):
    mean_time_to_detect: str
    mean_time_to_respond: str
    mean_time_to_contain: str
    mean_time_to_recover: str
    total_estimated_time: str

class PostIncidentReport(BaseModel):
    report_id: str
    incident_summary: str
    root_cause: str
    lessons_learned: List[str]
    recommendations: List[str]
    timeline: List[Dict[str, str]]
    affected_systems: List[str]
    financial_impact: Optional[str]

# NIST IR Phases
IR_PHASES = [
    "Preparation",
    "Detection and Analysis", 
    "Containment",
    "Eradication",
    "Recovery",
    "Post-Incident Activity"
]

# Incident type definitions
INCIDENT_TYPES = {
    "ransomware": {
        "name": "Ransomware Attack",
        "severity_default": "critical",
        "typical_duration": "24-72 hours",
        "mitre_techniques": ["T1486", "T1490", "T1485", "T1489"],
        "primary_goals": [
            "Contain spread immediately",
            "Preserve evidence",
            "Assess encryption scope",
            "Initiate recovery procedures"
        ]
    },
    "data_breach": {
        "name": "Data Breach / Exfiltration",
        "severity_default": "high",
        "typical_duration": "48-96 hours",
        "mitre_techniques": ["T1048", "T1041", "T1567", "T1020"],
        "primary_goals": [
            "Identify compromised data",
            "Stop ongoing exfiltration",
            "Assess regulatory impact",
            "Notify affected parties"
        ]
    },
    "phishing": {
        "name": "Phishing Campaign",
        "severity_default": "medium",
        "typical_duration": "4-8 hours",
        "mitre_techniques": ["T1566", "T1204", "T1078"],
        "primary_goals": [
            "Identify affected users",
            "Contain compromised accounts",
            "Remove malicious emails",
            "User awareness training"
        ]
    },
    "malware": {
        "name": "Malware Infection",
        "severity_default": "high",
        "typical_duration": "8-24 hours",
        "mitre_techniques": ["T1059", "T1055", "T1071", "T1547"],
        "primary_goals": [
            "Isolate infected systems",
            "Identify malware family",
            "Assess lateral movement",
            "Remove malware artifacts"
        ]
    },
    "insider_threat": {
        "name": "Insider Threat",
        "severity_default": "high",
        "typical_duration": "24-48 hours",
        "mitre_techniques": ["T1078", "T1005", "T1039", "T1048"],
        "primary_goals": [
            "Monitor suspect activities",
            "Preserve evidence carefully",
            "Coordinate with HR/Legal",
            "Revoke access at right time"
        ]
    },
    "ddos": {
        "name": "DDoS Attack",
        "severity_default": "medium",
        "typical_duration": "2-12 hours",
        "mitre_techniques": ["T1498", "T1499"],
        "primary_goals": [
            "Activate DDoS mitigation",
            "Identify attack vectors",
            "Maintain service availability",
            "Document attack patterns"
        ]
    },
    "apt": {
        "name": "Advanced Persistent Threat",
        "severity_default": "critical",
        "typical_duration": "7-14 days",
        "mitre_techniques": ["T1071", "T1027", "T1055", "T1082", "T1021"],
        "primary_goals": [
            "Maintain operational security",
            "Map adversary infrastructure",
            "Coordinate remediation",
            "Prevent re-compromise"
        ]
    },
    "web_attack": {
        "name": "Web Application Attack",
        "severity_default": "medium",
        "typical_duration": "4-12 hours",
        "mitre_techniques": ["T1190", "T1505", "T1059"],
        "primary_goals": [
            "Identify vulnerability",
            "Block malicious traffic",
            "Patch vulnerable component",
            "Review application logs"
        ]
    }
}

@router.get("/generate", response_model=IncidentPlaybook)
async def generate_playbook(
    incident_type: str = Query(..., description="Type of incident"),
    severity: str = Query("high", description="Incident severity: low, medium, high, critical"),
    scope: str = Query("single", description="Scope: single, multiple, enterprise-wide"),
    automation_level: str = Query("standard", description="Automation level: minimal, standard, advanced")
):
    """
    Generate a customized incident response playbook based on incident parameters.
    """
    
    if incident_type not in INCIDENT_TYPES:
        raise HTTPException(status_code=400, detail=f"Unknown incident type: {incident_type}")
    
    incident_info = INCIDENT_TYPES[incident_type]
    playbook_id = f"PB-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Generate steps based on incident type and NIST phases
    steps = []
    step_counter = 1
    
    # PREPARATION PHASE
    prep_steps = [
        {
            "action": "Activate Incident Response Team",
            "description": f"Assemble IR team members and establish communication channels for {incident_info['name']}",
            "responsible": "IR Team Lead",
            "time": "15 minutes",
            "tools": ["Slack/Teams", "PagerDuty", "Conference Bridge"],
            "success": ["All team members notified", "War room established"],
            "escalation": ["Key personnel unavailable after 30 minutes"]
        },
        {
            "action": "Initialize Incident Tracking",
            "description": "Create incident ticket and begin documentation",
            "responsible": "IR Analyst",
            "time": "10 minutes",
            "tools": ["JIRA", "ServiceNow", "Incident Log Template"],
            "success": ["Ticket created with all required fields", "Chain of custody log started"],
            "escalation": ["Unable to access ticketing system"]
        },
        {
            "action": "Establish Severity and Scope",
            "description": f"Confirm {severity} severity and {scope} scope assessment",
            "responsible": "IR Team Lead",
            "time": "20 minutes",
            "tools": ["Asset Inventory", "Network Diagrams", "SIEM"],
            "success": ["Severity validated", "Affected systems identified"],
            "escalation": ["Scope expanding beyond initial assessment"]
        }
    ]
    
    for prep in prep_steps:
        steps.append(PlaybookStep(
            step_number=step_counter,
            phase="Preparation",
            action=prep["action"],
            description=prep["description"],
            responsible_party=prep["responsible"],
            estimated_time=prep["time"],
            automation_available=automation_level in ["standard", "advanced"],
            required_tools=prep["tools"],
            success_criteria=prep["success"],
            escalation_triggers=prep["escalation"]
        ))
        step_counter += 1
    
    # DETECTION AND ANALYSIS PHASE
    analysis_steps = generate_analysis_steps(incident_type, severity)
    for analysis in analysis_steps:
        steps.append(PlaybookStep(
            step_number=step_counter,
            phase="Detection and Analysis",
            **analysis
        ))
        step_counter += 1
    
    # CONTAINMENT PHASE
    containment_steps = generate_containment_steps(incident_type, severity, scope)
    for contain in containment_steps:
        steps.append(PlaybookStep(
            step_number=step_counter,
            phase="Containment",
            **contain
        ))
        step_counter += 1
    
    # ERADICATION PHASE
    eradication_steps = generate_eradication_steps(incident_type)
    for erad in eradication_steps:
        steps.append(PlaybookStep(
            step_number=step_counter,
            phase="Eradication",
            **erad
        ))
        step_counter += 1
    
    # RECOVERY PHASE
    recovery_steps = generate_recovery_steps(incident_type, scope)
    for recover in recovery_steps:
        steps.append(PlaybookStep(
            step_number=step_counter,
            phase="Recovery",
            **recover
        ))
        step_counter += 1
    
    # POST-INCIDENT PHASE
    post_steps = [
        {
            "action": "Conduct Post-Incident Review",
            "description": "Schedule and conduct lessons learned meeting with all stakeholders",
            "responsible_party": "IR Team Lead",
            "estimated_time": "2-4 hours",
            "automation_available": False,
            "required_tools": ["Meeting Scheduler", "Documentation Template"],
            "success_criteria": ["All stakeholders present", "Action items documented"],
            "escalation_triggers": ["Critical findings require immediate executive briefing"]
        },
        {
            "action": "Update Security Controls",
            "description": "Implement improvements based on lessons learned",
            "responsible_party": "Security Engineering",
            "estimated_time": "1-2 weeks",
            "automation_available": automation_level == "advanced",
            "required_tools": ["Change Management System", "Security Tools"],
            "success_criteria": ["All approved changes implemented", "Documentation updated"],
            "escalation_triggers": ["Changes blocked by operational constraints"]
        }
    ]
    
    for post in post_steps:
        steps.append(PlaybookStep(
            step_number=step_counter,
            phase="Post-Incident Activity",
            **post
        ))
        step_counter += 1
    
    # Generate stakeholder notifications
    stakeholders = generate_stakeholder_notifications(incident_type, severity)
    
    # Generate evidence collection requirements
    evidence = generate_evidence_requirements(incident_type, severity)
    
    # Determine compliance requirements
    compliance = []
    if incident_type in ["data_breach", "ransomware"]:
        compliance.extend(["GDPR Article 33 (72-hour breach notification)", "State breach notification laws"])
    if severity in ["high", "critical"]:
        compliance.extend(["SOC 2 incident reporting", "Cyber insurance notification"])
    compliance.append("Internal security policy compliance")
    
    # Success metrics
    success_metrics = {
        "containment_time": f"< {get_containment_sla(severity)}",
        "system_recovery": "All critical systems operational",
        "evidence_preservation": "100% of required evidence collected",
        "stakeholder_notification": "All notifications sent within SLA"
    }
    
    return IncidentPlaybook(
        playbook_id=playbook_id,
        incident_type=incident_info["name"],
        severity=severity,
        generated_at=datetime.now().isoformat(),
        estimated_duration=incident_info["typical_duration"],
        steps=steps,
        stakeholders=stakeholders,
        evidence_collection=evidence,
        mitre_techniques=incident_info["mitre_techniques"],
        compliance_requirements=compliance,
        success_metrics=success_metrics
    )


def generate_analysis_steps(incident_type: str, severity: str) -> List[Dict]:
    """Generate detection and analysis steps based on incident type."""
    
    common_steps = [
        {
            "action": "Collect Initial Evidence",
            "description": f"Gather logs, memory dumps, and artifacts related to {incident_type}",
            "responsible_party": "Forensics Analyst",
            "estimated_time": "30-60 minutes",
            "automation_available": True,
            "required_tools": ["EDR Platform", "Log Aggregation", "Memory Capture Tools"],
            "success_criteria": ["All relevant logs collected", "Volatile data preserved"],
            "escalation_triggers": ["Critical systems unavailable for analysis"]
        },
        {
            "action": "Analyze Indicators of Compromise",
            "description": "Identify IOCs and determine scope of compromise",
            "responsible_party": "Threat Intelligence Analyst",
            "estimated_time": "1-2 hours",
            "automation_available": True,
            "required_tools": ["SIEM", "Threat Intel Platform", "Sandbox Environment"],
            "success_criteria": ["IOCs identified and documented", "Threat actor attribution attempted"],
            "escalation_triggers": ["Unknown malware family", "Advanced evasion techniques detected"]
        }
    ]
    
    # Add incident-specific analysis steps
    if incident_type == "ransomware":
        common_steps.append({
            "action": "Identify Ransomware Variant",
            "description": "Analyze ransom note and encryption patterns to identify ransomware family",
            "responsible_party": "Malware Analyst",
            "estimated_time": "30 minutes",
            "automation_available": True,
            "required_tools": ["ID Ransomware", "VirusTotal", "Malware Sandbox"],
            "success_criteria": ["Ransomware family identified", "Decryption possibility assessed"],
            "escalation_triggers": ["Unknown ransomware variant", "No decryption tool available"]
        })
    elif incident_type == "data_breach":
        common_steps.append({
            "action": "Assess Data Classification",
            "description": "Determine what data was accessed/exfiltrated and its sensitivity level",
            "responsible_party": "Data Protection Officer",
            "estimated_time": "2-4 hours",
            "automation_available": False,
            "required_tools": ["DLP Logs", "Data Classification System", "Access Logs"],
            "success_criteria": ["All compromised data identified", "Regulatory impact assessed"],
            "escalation_triggers": ["PII/PHI compromised", "Regulatory reporting required"]
        })
    
    return common_steps


def generate_containment_steps(incident_type: str, severity: str, scope: str) -> List[Dict]:
    """Generate containment steps based on incident parameters."""
    
    steps = []
    
    if incident_type in ["ransomware", "malware", "apt"]:
        steps.append({
            "action": "Network Isolation",
            "description": "Isolate affected systems from network to prevent spread",
            "responsible_party": "Network Security Team",
            "estimated_time": "15-30 minutes",
            "automation_available": True,
            "required_tools": ["Firewall", "Network Access Control", "EDR Remote Isolation"],
            "success_criteria": ["All affected systems isolated", "No lateral movement detected"],
            "escalation_triggers": ["Isolation impacting critical business operations"]
        })
    
    if incident_type == "phishing":
        steps.append({
            "action": "Email Remediation",
            "description": "Remove malicious emails from all mailboxes",
            "responsible_party": "Email Security Team",
            "estimated_time": "30 minutes",
            "automation_available": True,
            "required_tools": ["Email Security Gateway", "O365 Admin Center", "Email DLP"],
            "success_criteria": ["All malicious emails removed", "No additional clicks detected"],
            "escalation_triggers": ["Emails already opened/clicked by multiple users"]
        })
    
    if incident_type in ["data_breach", "insider_threat"]:
        steps.append({
            "action": "Access Revocation",
            "description": "Disable compromised accounts and revoke access tokens",
            "responsible_party": "Identity & Access Management",
            "estimated_time": "20 minutes",
            "automation_available": True,
            "required_tools": ["Active Directory", "IAM Platform", "PAM Solution"],
            "success_criteria": ["All compromised credentials disabled", "New access tokens issued"],
            "escalation_triggers": ["Service accounts compromised", "Admin access involved"]
        })
    
    steps.append({
        "action": "Short-term Containment Verification",
        "description": "Verify containment measures are effective and no active threats remain",
        "responsible_party": "SOC Team",
        "estimated_time": "1-2 hours",
        "automation_available": True,
        "required_tools": ["SIEM", "EDR Platform", "Network Monitoring"],
        "success_criteria": ["No active malicious activity", "Containment measures holding"],
        "escalation_triggers": ["Continued malicious activity", "New systems compromised"]
    })
    
    return steps


def generate_eradication_steps(incident_type: str) -> List[Dict]:
    """Generate eradication steps."""
    
    return [
        {
            "action": "Remove Malicious Artifacts",
            "description": "Delete malware, backdoors, and attacker tools from all systems",
            "responsible_party": "System Administrators",
            "estimated_time": "2-4 hours",
            "automation_available": True,
            "required_tools": ["EDR Platform", "Antivirus", "Script Repository"],
            "success_criteria": ["All malicious files removed", "No persistence mechanisms remain"],
            "escalation_triggers": ["Malware re-appears", "Hidden persistence found"]
        },
        {
            "action": "Patch Vulnerabilities",
            "description": "Apply security patches to close exploited vulnerabilities",
            "responsible_party": "Patch Management Team",
            "estimated_time": "4-8 hours",
            "automation_available": True,
            "required_tools": ["Patch Management System", "Vulnerability Scanner"],
            "success_criteria": ["All critical patches applied", "Vulnerability scan clean"],
            "escalation_triggers": ["Patches break critical applications"]
        },
        {
            "action": "Reset Credentials",
            "description": "Force password reset for all potentially compromised accounts",
            "responsible_party": "Identity & Access Management",
            "estimated_time": "1-3 hours",
            "automation_available": True,
            "required_tools": ["Active Directory", "Password Manager", "MFA System"],
            "success_criteria": ["All affected passwords reset", "MFA enforced"],
            "escalation_triggers": ["Users unable to access critical systems"]
        }
    ]


def generate_recovery_steps(incident_type: str, scope: str) -> List[Dict]:
    """Generate recovery steps."""
    
    steps = [
        {
            "action": "Restore from Clean Backups",
            "description": "Restore systems and data from verified clean backups",
            "responsible_party": "Backup & Recovery Team",
            "estimated_time": "4-12 hours",
            "automation_available": True,
            "required_tools": ["Backup Solution", "Recovery Tools", "Integrity Checker"],
            "success_criteria": ["All systems restored", "Data integrity verified"],
            "escalation_triggers": ["Backups also compromised", "Backup corruption detected"]
        },
        {
            "action": "Gradual System Restoration",
            "description": "Bring systems back online in controlled manner with enhanced monitoring",
            "responsible_party": "IT Operations",
            "estimated_time": "2-8 hours",
            "automation_available": False,
            "required_tools": ["Monitoring Tools", "Change Management", "Runbooks"],
            "success_criteria": ["All systems operational", "No anomalies detected"],
            "escalation_triggers": ["System instability", "Abnormal behavior detected"]
        },
        {
            "action": "Enhanced Monitoring Period",
            "description": "Implement 30-day enhanced monitoring for signs of re-compromise",
            "responsible_party": "SOC Team",
            "estimated_time": "30 days",
            "automation_available": True,
            "required_tools": ["SIEM", "EDR Platform", "UEBA"],
            "success_criteria": ["No suspicious activity detected", "All alerts triaged"],
            "escalation_triggers": ["Indicators of re-compromise"]
        }
    ]
    
    return steps


def generate_stakeholder_notifications(incident_type: str, severity: str) -> List[StakeholderNotification]:
    """Generate stakeholder notification requirements."""
    
    stakeholders = []
    
    # Executive notification
    if severity in ["high", "critical"]:
        stakeholders.append(StakeholderNotification(
            stakeholder_type="Executive Leadership (CISO, CIO, CEO)",
            notification_trigger="Immediately upon incident confirmation",
            communication_template="Executive Brief: [Incident Type] - [Severity] - [Current Status] - [Business Impact] - [Estimated Recovery Time]",
            notification_method="Phone call + Email",
            escalation_threshold="If business operations significantly impacted"
        ))
    
    # Legal notification
    if incident_type in ["data_breach", "ransomware", "insider_threat"]:
        stakeholders.append(StakeholderNotification(
            stakeholder_type="Legal Department",
            notification_trigger="Within 1 hour of confirmation",
            communication_template="Legal Notification: Incident involves [Data Types] - [Regulatory Implications] - [Required Notifications]",
            notification_method="Secure email + Phone",
            escalation_threshold="If regulatory reporting required"
        ))
    
    # PR/Communications
    if severity == "critical" or incident_type == "data_breach":
        stakeholders.append(StakeholderNotification(
            stakeholder_type="Public Relations / Communications",
            notification_trigger="Before any public disclosure",
            communication_template="PR Brief: [Approved Messaging] - [Q&A Preparation] - [Media Response Plan]",
            notification_method="Secure email",
            escalation_threshold="If media inquiries received"
        ))
    
    # Cyber Insurance
    stakeholders.append(StakeholderNotification(
        stakeholder_type="Cyber Insurance Provider",
        notification_trigger="Within 24 hours",
        communication_template="Insurance Claim: [Policy Number] - [Incident Details] - [Estimated Impact] - [Response Actions]",
        notification_method="Insurance portal + Email",
        escalation_threshold="If costs exceed deductible"
    ))
    
    return stakeholders


def generate_evidence_requirements(incident_type: str, severity: str) -> List[EvidenceItem]:
    """Generate evidence collection requirements."""
    
    evidence = [
        EvidenceItem(
            evidence_type="System Logs",
            collection_method="Automated collection via SIEM and log aggregation",
            retention_period="90 days minimum, 7 years if legal hold",
            chain_of_custody=True,
            legal_hold_required=severity in ["high", "critical"],
            storage_location="Evidence Repository (encrypted)"
        ),
        EvidenceItem(
            evidence_type="Network Traffic Captures",
            collection_method="PCAP collection at perimeter and internal segments",
            retention_period="30 days minimum",
            chain_of_custody=True,
            legal_hold_required=incident_type in ["data_breach", "apt"],
            storage_location="Network Forensics Storage"
        ),
        EvidenceItem(
            evidence_type="Memory Dumps",
            collection_method="EDR-based memory capture or manual tools",
            retention_period="Until analysis complete + 90 days",
            chain_of_custody=True,
            legal_hold_required=True,
            storage_location="Forensics Lab Storage"
        ),
        EvidenceItem(
            evidence_type="Disk Images",
            collection_method="Forensic disk imaging (write-blocked)",
            retention_period="7 years if litigation possible",
            chain_of_custody=True,
            legal_hold_required=severity == "critical",
            storage_location="Forensics Lab Storage (offline)"
        )
    ]
    
    if incident_type == "insider_threat":
        evidence.append(EvidenceItem(
            evidence_type="HR Records and Access Logs",
            collection_method="Coordinate with HR, export access logs",
            retention_period="Per HR policy (typically 7 years)",
            chain_of_custody=True,
            legal_hold_required=True,
            storage_location="Secure HR System + Evidence Repository"
        ))
    
    return evidence


def get_containment_sla(severity: str) -> str:
    """Get containment SLA based on severity."""
    sla_map = {
        "critical": "1 hour",
        "high": "4 hours",
        "medium": "24 hours",
        "low": "72 hours"
    }
    return sla_map.get(severity, "24 hours")


@router.get("/templates", response_model=List[PlaybookTemplate])
async def get_playbook_templates():
    """Get available playbook templates."""
    
    templates = []
    for incident_id, info in INCIDENT_TYPES.items():
        templates.append(PlaybookTemplate(
            template_id=incident_id,
            name=info["name"],
            description=f"Standardized response procedures for {info['name']} incidents",
            incident_types=[incident_id],
            complexity="medium" if incident_id in ["phishing", "ddos", "web_attack"] else "high",
            typical_duration=info["typical_duration"],
            required_skills=[
                "Incident Response",
                "Forensics Analysis",
                "Threat Intelligence"
            ] + (["Malware Analysis"] if incident_id in ["ransomware", "malware", "apt"] else [])
        ))
    
    return templates


@router.get("/metrics/{incident_type}", response_model=IncidentMetrics)
async def get_incident_metrics(incident_type: str):
    """Get historical performance metrics for incident type."""
    
    if incident_type not in INCIDENT_TYPES:
        raise HTTPException(status_code=400, detail="Unknown incident type")
    
    # Simulated metrics
    return IncidentMetrics(
        mean_time_to_detect=f"{np.random.randint(15, 120)} minutes",
        mean_time_to_respond=f"{np.random.randint(30, 240)} minutes",
        mean_time_to_contain=f"{np.random.randint(2, 12)} hours",
        mean_time_to_recover=f"{np.random.randint(6, 48)} hours",
        total_estimated_time=INCIDENT_TYPES[incident_type]["typical_duration"]
    )


@router.post("/post-incident-report", response_model=PostIncidentReport)
async def generate_post_incident_report(
    incident_id: str,
    incident_type: str,
    actual_duration: str,
    root_cause: str
):
    """Generate post-incident analysis report."""
    
    report_id = f"PIR-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Generate timeline
    timeline = [
        {
            "timestamp": (datetime.now() - timedelta(hours=48)).isoformat(),
            "event": "Initial compromise detected",
            "phase": "Detection"
        },
        {
            "timestamp": (datetime.now() - timedelta(hours=47)).isoformat(),
            "event": "Incident response team activated",
            "phase": "Response"
        },
        {
            "timestamp": (datetime.now() - timedelta(hours=46)).isoformat(),
            "event": "Affected systems isolated",
            "phase": "Containment"
        },
        {
            "timestamp": (datetime.now() - timedelta(hours=40)).isoformat(),
            "event": "Threat eradicated from environment",
            "phase": "Eradication"
        },
        {
            "timestamp": (datetime.now() - timedelta(hours=24)).isoformat(),
            "event": "Systems restored from backup",
            "phase": "Recovery"
        },
        {
            "timestamp": datetime.now().isoformat(),
            "event": "Post-incident review completed",
            "phase": "Post-Incident"
        }
    ]
    
    # Generate lessons learned
    lessons_learned = [
        "Earlier detection possible with enhanced monitoring of [specific data source]",
        "Containment procedures worked effectively but could be automated",
        "Backup verification process should be performed more frequently",
        "Communication protocols with legal team need improvement",
        "Additional training needed on [specific tool or technique]"
    ]
    
    # Generate recommendations
    recommendations = [
        "Implement automated detection rule for [specific IOC pattern]",
        "Deploy additional EDR sensors on critical systems",
        "Update incident response playbook based on lessons learned",
        "Conduct tabletop exercise for similar scenario within 60 days",
        "Review and update backup retention policies",
        "Enhance security awareness training focusing on [attack vector]"
    ]
    
    return PostIncidentReport(
        report_id=report_id,
        incident_summary=f"{INCIDENT_TYPES.get(incident_type, {}).get('name', incident_type)} incident affecting multiple systems. Response completed in {actual_duration}.",
        root_cause=root_cause,
        lessons_learned=lessons_learned,
        recommendations=recommendations,
        timeline=timeline,
        affected_systems=[
            "web-server-01",
            "db-server-03",
            "workstation-45",
            "workstation-67"
        ],
        financial_impact="Estimated $50,000 - $100,000 (downtime + response costs)"
    )


@router.get("/communication-template/{stakeholder_type}")
async def get_communication_template(stakeholder_type: str):
    """Get communication template for specific stakeholder."""
    
    templates = {
        "executive": """
TO: Executive Leadership
FROM: Incident Response Team
SUBJECT: [SEVERITY] Security Incident - [INCIDENT_TYPE]

EXECUTIVE SUMMARY:
A [severity] security incident has been identified involving [brief description].

CURRENT STATUS:
- Detection Time: [timestamp]
- Current Phase: [phase]
- Systems Affected: [count/description]
- Business Impact: [description]

IMMEDIATE ACTIONS TAKEN:
1. [action 1]
2. [action 2]
3. [action 3]

ESTIMATED RECOVERY TIME: [timeframe]

NEXT UPDATE: [timeframe]

INCIDENT COMMANDER: [name]
CONTACT: [phone/email]
        """,
        "legal": """
TO: Legal Department
FROM: Incident Response Team
SUBJECT: Legal Notification - Security Incident

INCIDENT DETAILS:
- Incident ID: [ID]
- Type: [incident type]
- Discovery Date: [date]
- Data Involved: [description]

REGULATORY CONSIDERATIONS:
- [regulation 1]: [requirement]
- [regulation 2]: [requirement]

POTENTIAL NOTIFICATIONS REQUIRED:
- [notification 1]
- [notification 2]

EVIDENCE PRESERVATION:
All evidence has been preserved per legal hold procedures.

NEXT STEPS:
Please advise on:
1. Regulatory reporting requirements
2. Customer/partner notification requirements
3. Additional legal considerations

CONTACT: [IR Lead name and contact]
        """,
        "technical": """
TECHNICAL INCIDENT BRIEF

INCIDENT: [ID] - [Type]
SEVERITY: [Level]

TECHNICAL DETAILS:
- Attack Vector: [description]
- IOCs Identified: [list]
- MITRE Techniques: [list]
- Systems Compromised: [list]

ANALYSIS FINDINGS:
[Detailed technical findings]

CONTAINMENT MEASURES:
[Actions taken]

REQUIRED TECHNICAL ACTIONS:
1. [action with responsible party]
2. [action with responsible party]

MONITORING REQUIREMENTS:
[Specific monitoring needs]

ARTIFACTS LOCATION: [file share/ticket system]
        """
    }
    
    return {
        "stakeholder_type": stakeholder_type,
        "template": templates.get(stakeholder_type, "Template not found"),
        "usage_notes": "Replace [PLACEHOLDERS] with actual incident details"
    }

