"""Orchestrator for collecting IOCs from all sources"""

from typing import List, Dict
import logging

from .otx_collector import OTXCollector
from .abuse_collector import AbuseCollector
from .phishtank_collector import PhishTankCollector
from .nvd_collector import NVDCollector
from .base_collector import BaseCollector, IOCDeduplicator

logger = logging.getLogger(__name__)


class IOCOrchestrator:
    """Orchestrate IOC collection from all sources"""
    
    def __init__(self):
        """Initialize IOC orchestrator with all collectors."""
        self.otx = OTXCollector()
        self.abuse = AbuseCollector()
        self.phishtank = PhishTankCollector()
        self.nvd = NVDCollector()
        self.base_collector = BaseCollector()
        self.deduplicator = IOCDeduplicator()
    
    def collect_all(self, limit_per_source: int = 100) -> List[Dict]:
        """
        Collect IOCs from all sources.
        
        Args:
            limit_per_source: Maximum IOCs per source
            
        Returns:
            List of normalized and deduplicated IOC dictionaries
        """
        all_iocs = []
        
        # Collect from OTX
        try:
            logger.info("Collecting IOCs from OTX...")
            otx_iocs = self.otx.collect_all(limit=limit_per_source)
            normalized_otx = [self.base_collector.normalize_ioc(ioc) for ioc in otx_iocs]
            all_iocs.extend(normalized_otx)
            logger.info(f"Collected {len(normalized_otx)} IOCs from OTX")
        except Exception as e:
            logger.error(f"Error collecting from OTX: {e}")
        
        # Collect from Abuse.ch
        try:
            logger.info("Collecting IOCs from Abuse.ch...")
            abuse_iocs = self.abuse.collect_all(limit=limit_per_source)
            normalized_abuse = [self.base_collector.normalize_ioc(ioc) for ioc in abuse_iocs]
            all_iocs.extend(normalized_abuse)
            logger.info(f"Collected {len(normalized_abuse)} IOCs from Abuse.ch")
        except Exception as e:
            logger.error(f"Error collecting from Abuse.ch: {e}")
        
        # Collect from PhishTank
        try:
            logger.info("Collecting IOCs from PhishTank...")
            phishtank_iocs = self.phishtank.collect_all(limit=limit_per_source)
            normalized_phishtank = [self.base_collector.normalize_ioc(ioc) for ioc in phishtank_iocs]
            all_iocs.extend(normalized_phishtank)
            logger.info(f"Collected {len(normalized_phishtank)} IOCs from PhishTank")
        except Exception as e:
            logger.error(f"Error collecting from PhishTank: {e}")
        
        # Collect from NVD
        try:
            logger.info("Collecting CVEs from NVD...")
            nvd_iocs = self.nvd.collect_all(days=7, limit=limit_per_source)
            normalized_nvd = [self.base_collector.normalize_ioc(ioc) for ioc in nvd_iocs]
            all_iocs.extend(normalized_nvd)
            logger.info(f"Collected {len(normalized_nvd)} CVEs from NVD")
        except Exception as e:
            logger.error(f"Error collecting from NVD: {e}")
        
        # Deduplicate
        logger.info(f"Deduplicating {len(all_iocs)} IOCs...")
        deduplicated = self.deduplicator.deduplicate(all_iocs)
        logger.info(f"Final count: {len(deduplicated)} unique IOCs")
        
        return deduplicated

