from datetime import datetime, timezone
import hashlib


def generate_case_id(seed=None):

    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%d%H%M%S"
    )

    seed_value = (
        seed
        if seed is not None
        else timestamp
    )

    digest = hashlib.sha256(
        str(seed_value).encode()
    ).hexdigest()[:8].upper()

    return f"CASE-{timestamp}-{digest}"


def build_case_summary(
    case_id,
    investigation_type,
    target,
    risk_data=None,
    ioc_data=None,
    correlation_data=None,
    email_correlation=None
):

    risk_data = risk_data or {}
    ioc_data = ioc_data or {}
    correlation_data = correlation_data or {}
    email_correlation = email_correlation or {}

    risk_findings = risk_data.get(
        "findings",
        []
    )

    correlation_findings = (
        correlation_data.get(
            "findings",
            []
        )
    )

    email_findings = (
        email_correlation.get(
            "findings",
            []
        )
    )

    ioc_summary = ioc_data.get(
        "summary",
        {}
    )

    return {

        "case_id":
            case_id,

        "created_at":
            datetime.now(timezone.utc).isoformat(),

        "investigation_type":
            investigation_type,

        "target":
            target,

        "risk": {

            "score":
                risk_data.get(
                    "risk_score",
                    0
                ),

            "level":
                risk_data.get(
                    "risk_level",
                    "LOW"
                )

        },

        "evidence_summary": {

            "risk_findings":
                len(risk_findings),

            "correlation_findings":
                len(correlation_findings),

            "email_correlation_findings":
                len(email_findings),

            "primary_iocs":
                ioc_summary.get(
                    "primary_count",
                    0
                ),

            "supporting_iocs":
                ioc_summary.get(
                    "supporting_count",
                    0
                ),

            "relationships":
                correlation_data.get(
                    "relationship_count",
                    0
                ),

            "entities":
                correlation_data.get(
                    "entity_count",
                    0
                )

        }

    }
