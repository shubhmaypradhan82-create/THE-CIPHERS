# ==========================================
# CASE-LEVEL RISK ENGINE
# ==========================================


def get_risk_level(score):

    if score >= 80:
        return "CRITICAL"

    if score >= 60:
        return "HIGH"

    if score >= 30:
        return "MEDIUM"

    return "LOW"


def calculate_case_risk(
    email_risk=None,
    url_results=None,
    email_correlation=None,
    email_infrastructure=None
):

    email_risk = email_risk or {}
    url_results = url_results or []
    email_correlation = email_correlation or {}
    email_infrastructure = email_infrastructure or {}

    # --------------------------------------
    # Start with email risk
    # --------------------------------------

    email_score = int(
        email_risk.get(
            "risk_score",
            0
        ) or 0
    )

    # --------------------------------------
    # URL risk aggregation
    # --------------------------------------

    url_scores = []

    for item in url_results:

        risk = item.get(
            "risk_analysis",
            {}
        )

        score = risk.get(
            "risk_score"
        )

        if isinstance(score, int):
            url_scores.append(score)

    if url_scores:

        highest_url_score = max(
            url_scores
        )

        average_url_score = round(
            sum(url_scores) / len(url_scores)
        )

    else:

        highest_url_score = 0
        average_url_score = 0

    # --------------------------------------
    # Evidence-based weighting
    # --------------------------------------
    #
    # Email evidence = 40%
    # Highest URL risk = 40%
    # Cross-source correlation = 20%
    #

    weighted_email = (
        email_score * 0.40
    )

    weighted_url = (
        highest_url_score * 0.40
    )

    correlation_score = 0

    correlation_findings = (
        email_correlation.get(
            "findings",
            []
        )
    )

    infrastructure_findings = (
        email_infrastructure.get(
            "findings",
            []
        )
    )

    # Strong email/URL matches provide
    # evidence strength, not automatic
    # maliciousness.
    for finding in (
        correlation_findings
        + infrastructure_findings
    ):

        evidence_strength = finding.get(
            "evidence_strength",
            0
        )

        if evidence_strength > correlation_score:

            correlation_score = (
                evidence_strength
            )

    weighted_correlation = (
        correlation_score * 0.20
    )

    overall_score = round(
        weighted_email
        + weighted_url
        + weighted_correlation
    )

    overall_score = max(
        0,
        min(overall_score, 100)
    )

    # --------------------------------------
    # Findings
    # --------------------------------------

    findings = []

    if email_score >= 30:

        findings.append({
            "type":
                "email_risk",
            "severity":
                "warning",
            "description":
                "Email evidence contributed significant risk.",
            "source":
                "email_risk_engine"
        })

    if highest_url_score >= 30:

        findings.append({
            "type":
                "url_risk",
            "severity":
                "warning",
            "description":
                "At least one analyzed URL contributed significant risk.",
            "source":
                "url_risk_engine"
        })

    if correlation_score >= 90:

        findings.append({
            "type":
                "strong_correlation",
            "severity":
                "info",
            "description":
                "Strong cross-source relationships were identified.",
            "source":
                "correlation_engine"
        })

    return {

        "risk_score":
            overall_score,

        "risk_level":
            get_risk_level(
                overall_score
            ),

        "components": {

            "email_score":
                email_score,

            "highest_url_score":
                highest_url_score,

            "average_url_score":
                average_url_score,

            "correlation_evidence_strength":
                correlation_score

        },

        "weights": {

            "email":
                0.40,

            "url":
                0.40,

            "correlation":
                0.20

        },

        "findings":
            findings,

        "engine_version":
            "1.0"

    }
