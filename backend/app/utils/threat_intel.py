from app.utils.threat_intel_manager import (
    ThreatIntelManager
)


def enrich_iocs(ioc_data=None):

    manager = ThreatIntelManager()

    return manager.enrich(
        ioc_data
    )
