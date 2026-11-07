from datetime import datetime, timezone


def generate_forensic_report(
    case=None,
    email_evidence=None,
    email_risk=None,
    case_risk=None,
    email_correlation=None,
    email_infrastructure=None,
    analyzed_urls=None,
    ioc_analysis=None,
    timeline=None
):
    case = case or {}
    email_evidence = email_evidence or {}
    email_risk = email_risk or {}
    case_risk = case_risk or {}
    email_correlation = email_correlation or {}
    email_infrastructure = email_infrastructure or {}
    analyzed_urls = analyzed_urls or []
    ioc_analysis = ioc_analysis or {}
    timeline = timeline or []

    primary_iocs = ioc_analysis.get(
        "primary_iocs",
        []
    )

    supporting_iocs = ioc_analysis.get(
        "supporting_iocs",
        []
    )

    findings = []

    for finding in email_risk.get(
        "findings",
        []
    ):
        findings.append({
            "source": finding.get(
                "source",
                "email_risk_engine"
            ),
            "type": finding.get(
                "type",
                "finding"
            ),
            "severity": finding.get(
                "severity",
                "INFO"
            ),
            "description": finding.get(
                "description",
                ""
            ),
            "points": finding.get(
                "points",
                0
            )
        })

    for finding in email_correlation.get(
        "findings",
        []
    ):
        findings.append({
            "source": "email_url_correlation",
            "type": finding.get(
                "type",
                "correlation"
            ),
            "severity": str(
                finding.get(
                    "severity",
                    "INFO"
                )
            ).upper(),
            "description": finding.get(
                "message",
                ""
            ),
            "points": 0
        })

    for finding in email_infrastructure.get(
        "findings",
        []
    ):
        findings.append({
            "source": "email_infrastructure",
            "type": finding.get(
                "type",
                "infrastructure"
            ),
            "severity": str(
                finding.get(
                    "severity",
                    "INFO"
                )
            ).upper(),
            "description": finding.get(
                "message",
                ""
            ),
            "points": 0
        })

    high_priority = [
        item
        for item in findings
        if item.get("severity") in (
            "HIGH",
            "CRITICAL"
        )
    ]

    medium_priority = [
        item
        for item in findings
        if item.get("severity") == "MEDIUM"
    ]

    url_summaries = []

    for item in analyzed_urls:

        url_data = item.get(
            "url_analysis",
            {}
        )

        risk_data = item.get(
            "risk_analysis",
            {}
        )

        url_summaries.append({
            "url": url_data.get("url"),
            "domain": url_data.get("domain"),
            "ip_address": url_data.get(
                "ip_address"
            ),
            "risk_score": risk_data.get(
                "risk_score",
                0
            ),
            "risk_level": risk_data.get(
                "risk_level",
                "LOW"
            )
        })

    return {

        "report": {
            "title":
                "Forensic Investigation Report",

            "generated_at":
                datetime.now(timezone.utc).isoformat(),

            "case_id":
                case.get(
                    "case_id"
                ),

            "investigation_type":
                case.get(
                    "investigation_type"
                ),

            "target":
                case.get(
                    "target"
                )
        },

        "executive_summary": {

            "overall_risk":
                case_risk.get(
                    "risk_level",
                    case.get(
                        "risk",
                        {}
                    ).get(
                        "level",
                        "LOW"
                    )
                ),

            "overall_score":
                case_risk.get(
                    "risk_score",
                    case.get(
                        "risk",
                        {}
                    ).get(
                        "score",
                        0
                    )
                ),

            "email_risk":
                email_risk.get(
                    "risk_level",
                    "LOW"
                ),

            "email_score":
                email_risk.get(
                    "risk_score",
                    0
                ),

            "urls_analyzed":
                len(analyzed_urls),

            "primary_iocs":
                len(primary_iocs),

            "supporting_iocs":
                len(supporting_iocs),

            "timeline_events":
                len(timeline)
        },

        "email_evidence": {
            "from":
                email_evidence.get("from"),

            "to":
                email_evidence.get("to"),

            "subject":
                email_evidence.get("subject"),

            "date":
                email_evidence.get("date"),

            "message_id":
                email_evidence.get("message_id"),

            "reply_to":
                email_evidence.get("reply_to"),

            "return_path":
                email_evidence.get(
                    "return_path"
                ),

            "received_hop_count":
                email_evidence.get(
                    "received_hop_count",
                    0
                )
        },

        "key_findings": (
            high_priority
            + medium_priority
        ),

        "all_findings":
            findings,

        "iocs": {

            "primary":
                primary_iocs,

            "supporting":
                supporting_iocs
        },

        "analyzed_urls":
            url_summaries,

        "email_correlation":
            email_correlation,

        "email_infrastructure":
            email_infrastructure,

        "timeline":
            timeline
    }
