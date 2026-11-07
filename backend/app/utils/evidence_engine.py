# ==========================================
# FORENSIC EVIDENCE ENGINE
# ==========================================


CONFIDENCE_LEVELS = {
    "confirmed": 100,
    "high": 90,
    "medium": 70,
    "low": 40,
    "informational": 20
}


SEVERITY_LEVELS = {
    "critical": 100,
    "high": 75,
    "medium": 50,
    "low": 25,
    "info": 10
}


# ==========================================
# CONFIDENCE FROM EVIDENCE STRENGTH
# ==========================================

def confidence_from_strength(strength):

    if strength >= 90:
        return "confirmed"

    if strength >= 75:
        return "high"

    if strength >= 50:
        return "medium"

    if strength >= 25:
        return "low"

    return "informational"


# ==========================================
# NORMALIZE FINDING
# ==========================================

def normalize_finding(
    finding_type,
    message,
    severity="info",
    evidence=None,
    evidence_strength=50
):

    evidence_strength = max(
        0,
        min(100, int(evidence_strength))
    )

    confidence = confidence_from_strength(
        evidence_strength
    )

    severity = severity.lower()

    if severity not in SEVERITY_LEVELS:
        severity = "info"

    return {

        "type": finding_type,

        "message": message,

        "severity": severity,

        "confidence": confidence,

        "evidence_strength":
            evidence_strength,

        "evidence":
            evidence

    }


# ==========================================
# NORMALIZE FINDINGS LIST
# ==========================================

def normalize_findings(findings):

    normalized = []

    for finding in findings:

        if not isinstance(
            finding,
            dict
        ):
            continue

        normalized.append(
            normalize_finding(
                finding_type=
                    finding.get(
                        "type",
                        "unknown"
                    ),

                message=
                    finding.get(
                        "message",
                        "Unknown finding"
                    ),

                severity=
                    finding.get(
                        "severity",
                        "info"
                    ),

                evidence=
                    finding.get(
                        "evidence"
                    ),

                evidence_strength=
                    finding.get(
                        "evidence_strength",
                        50
                    )
            )
        )

    return normalized


# ==========================================
# EVIDENCE SUMMARY
# ==========================================

def summarize_evidence(findings):

    summary = {

        "total_findings": 0,

        "confirmed": 0,

        "high": 0,

        "medium": 0,

        "low": 0,

        "informational": 0,

        "critical": 0,

        "high_severity": 0,

        "medium_severity": 0,

        "low_severity": 0,

        "info_severity": 0

    }

    for finding in findings:

        summary["total_findings"] += 1

        confidence = finding.get(
            "confidence",
            "informational"
        )

        severity = finding.get(
            "severity",
            "info"
        )

        if confidence in summary:
            summary[confidence] += 1

        severity_key = {
            "critical":
                "critical",

            "high":
                "high_severity",

            "medium":
                "medium_severity",

            "low":
                "low_severity",

            "info":
                "info_severity"
        }.get(severity)

        if severity_key:
            summary[severity_key] += 1

    return summary


# ==========================================
# BUILD EVIDENCE REPORT
# ==========================================

def build_evidence_report(findings):

    normalized = normalize_findings(
        findings
    )

    summary = summarize_evidence(
        normalized
    )

    return {

        "findings":
            normalized,

        "summary":
            summary

    }
