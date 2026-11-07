# ==========================================
# FORENSIC RISK ENGINE
# ==========================================


def get_risk_level(score):

    if score >= 80:
        return "CRITICAL"

    if score >= 60:
        return "HIGH"

    if score >= 30:
        return "MEDIUM"

    return "LOW"


def add_finding(
    findings,
    finding_type,
    severity,
    description,
    points,
    source
):

    findings.append({
        "type": finding_type,
        "severity": severity,
        "description": description,
        "points": points,
        "source": source
    })


# ==========================================
# EMAIL RISK
# ==========================================

def calculate_email_risk(email_data):

    email_data = email_data or {}

    score = 0
    findings = []

    sender = email_data.get(
        "from",
        ""
    )

    reply_to = email_data.get(
        "reply_to",
        ""
    )

    subject = email_data.get(
        "subject",
        ""
    )

    # --------------------------------------
    # Reply-To mismatch
    # --------------------------------------

    if sender and reply_to:

        if (
            "@" in sender
            and "@" in reply_to
        ):

            sender_domain = (
                sender.split("@")[-1]
                .lower()
                .rstrip(">")
            )

            reply_domain = (
                reply_to.split("@")[-1]
                .lower()
                .rstrip(">")
            )

            if sender_domain != reply_domain:

                points = 25
                score += points

                add_finding(
                    findings,
                    "Reply-To mismatch",
                    "MEDIUM",
                    "The Reply-To domain is different from the sender domain.",
                    points,
                    "email_analyzer"
                )

    # --------------------------------------
    # Return-Path mismatch
    # --------------------------------------

    return_path = email_data.get(
        "return_path"
    )

    if (
        sender
        and return_path
        and "@" in sender
        and "@" in return_path
    ):

        sender_domain = (
            sender.split("@")[-1]
            .lower()
            .rstrip(">")
        )

        return_domain = (
            return_path.split("@")[-1]
            .lower()
            .rstrip(">")
        )

        if sender_domain != return_domain:

            points = 10
            score += points

            add_finding(
                findings,
                "Return-Path mismatch",
                "LOW",
                "The Return-Path domain differs from the sender domain.",
                points,
                "email_analyzer"
            )

    # --------------------------------------
    # Suspicious subject
    # --------------------------------------

    suspicious_words = [
        "urgent",
        "verify",
        "password",
        "account suspended",
        "click immediately",
        "security alert",
        "confirm your account"
    ]

    for word in suspicious_words:

        if word in subject.lower():

            points = 10
            score += points

            add_finding(
                findings,
                "Suspicious keyword",
                "LOW",
                f"Suspicious keyword detected in subject: {word}",
                points,
                "email_analyzer"
            )

    # ======================================
    # AUTHENTICATION
    # ======================================

    authentication = email_data.get(
        "authentication",
        {}
    )

    auth_results = authentication.get(
        "authentication_results",
        []
    )

    auth_text = " ".join(
        str(item)
        for item in auth_results
    ).lower()

    if "spf=fail" in auth_text:

        points = 20
        score += points

        add_finding(
            findings,
            "SPF failure",
            "MEDIUM",
            "Authentication-Results reports SPF failure.",
            points,
            "email_authentication"
        )

    if "spf=softfail" in auth_text:

        points = 10
        score += points

        add_finding(
            findings,
            "SPF softfail",
            "LOW",
            "Authentication-Results reports SPF softfail.",
            points,
            "email_authentication"
        )

    if "dkim=fail" in auth_text:

        points = 20
        score += points

        add_finding(
            findings,
            "DKIM failure",
            "MEDIUM",
            "Authentication-Results reports DKIM failure.",
            points,
            "email_authentication"
        )

    if "dmarc=fail" in auth_text:

        points = 25
        score += points

        add_finding(
            findings,
            "DMARC failure",
            "HIGH",
            "Authentication-Results reports DMARC failure.",
            points,
            "email_authentication"
        )

    if not auth_results:

        findings.append({
            "type":
                "Authentication headers absent",
            "severity":
                "INFO",
            "description":
                "No Authentication-Results header was found.",
            "points":
                0,
            "source":
                "email_authentication"
        })

    # ======================================
    # RECEIVED CHAIN INTELLIGENCE
    # ======================================

    received_summary = email_data.get(
        "received_summary",
        {}
    )

    hop_count = received_summary.get(
        "hop_count",
        email_data.get(
            "received_hop_count",
            0
        )
    )

    source_ips = received_summary.get(
        "source_ips",
        []
    )

    private_source_ips = received_summary.get(
        "private_source_ips",
        []
    )

    public_source_ips = received_summary.get(
        "public_source_ips",
        []
    )

    if hop_count == 0:

        findings.append({
            "type":
                "Missing Received chain",
            "severity":
                "INFO",
            "description":
                "No Received headers were found.",
            "points":
                0,
            "source":
                "email_analyzer"
        })

    # Private source addresses are useful evidence,
    # but are not inherently malicious.
    if private_source_ips:

        findings.append({
            "type":
                "Private source IP observed",
            "severity":
                "INFO",
            "description":
                (
                    f"{len(private_source_ips)} "
                    "private source IP(s) were observed "
                    "in the Received chain."
                ),
            "points":
                0,
            "source":
                "email_analyzer"
        })

    # A large chain can be unusual, but does not
    # automatically mean malicious.
    if hop_count >= 8:

        points = 5
        score += points

        add_finding(
            findings,
            "Long Received chain",
            "LOW",
            f"{hop_count} Received hops were observed.",
            points,
            "email_analyzer"
        )

    # ======================================
    # HEADER FINDINGS
    # ======================================

    for header_finding in email_data.get(
        "header_findings",
        []
    ):

        finding_type = header_finding.get(
            "type"
        )

        if finding_type in (
            "reply_to_domain_mismatch",
            "return_path_mismatch",
            "spf_fail",
            "dkim_fail",
            "dmarc_fail",
            "missing_received_chain"
        ):
            continue

        findings.append({
            "type":
                header_finding.get(
                    "type",
                    "email_header_finding"
                ),
            "severity":
                header_finding.get(
                    "severity",
                    "INFO"
                ).upper(),
            "description":
                header_finding.get(
                    "message",
                    "Email header finding detected."
                ),
            "points":
                0,
            "source":
                "email_analyzer"
        })

    score = max(
        0,
        min(score, 100)
    )

    return {
        "risk_score": score,
        "risk_level": get_risk_level(score),
        "findings": findings,
        "engine_version": "5.1"
    }


# ==========================================
# THREAT INTELLIGENCE
# ==========================================

def apply_threat_intelligence(
    findings,
    threat_intel_data
):

    score = 0

    for item in (
        threat_intel_data or {}
    ).get(
        "ioc_results",
        []
    ):

        ioc = item.get(
            "ioc",
            {}
        )

        ioc_type = ioc.get(
            "type",
            "unknown"
        )

        value = ioc.get(
            "value",
            ""
        )

        malicious = 0
        benign = 0

        for provider in item.get(
            "provider_results",
            []
        ):

            status = provider.get(
                "status"
            )

            verdict = provider.get(
                "malicious"
            )

            if status in (
                "unknown",
                "not_configured",
                "error",
                "not_found",
                "unsupported",
                "timeout",
                "authentication_error",
                "rate_limited"
            ):
                continue

            if verdict is True:
                malicious += 1

            elif verdict is False:
                benign += 1

        if malicious >= 2:

            points = 40
            score += points

            add_finding(
                findings,
                "Threat intelligence match",
                "HIGH",
                (
                    f"{ioc_type} {value} received "
                    f"malicious verdicts from "
                    f"{malicious} providers."
                ),
                points,
                "threat_intelligence"
            )

        elif malicious == 1:

            points = 25
            score += points

            add_finding(
                findings,
                "Threat intelligence match",
                "MEDIUM",
                (
                    f"{ioc_type} {value} received "
                    "a malicious verdict from one provider."
                ),
                points,
                "threat_intelligence"
            )

        elif benign >= 2:

            findings.append({
                "type":
                    "Threat intelligence benign result",
                "severity":
                    "INFO",
                "description":
                    (
                        f"{ioc_type} {value} received "
                        f"benign verdicts from "
                        f"{benign} providers."
                    ),
                "points":
                    0,
                "source":
                    "threat_intelligence"
            })

    return score


# ==========================================
# COMBINED URL RISK
# ==========================================

def calculate_combined_url_risk(
    url_data=None,
    redirect_data=None,
    http_data=None,
    tls_data=None,
    ioc_data=None,
    correlation_data=None,
    threat_intel_data=None
):

    url_data = url_data or {}
    redirect_data = redirect_data or {}
    http_data = http_data or {}
    tls_data = tls_data or {}
    ioc_data = ioc_data or {}
    correlation_data = correlation_data or {}
    threat_intel_data = threat_intel_data or {}

    score = 0
    findings = []

    for indicator in url_data.get(
        "suspicious_indicators",
        []
    ):

        text = str(indicator)
        lower = text.lower()

        if "ip address" in lower:
            points = 25
            severity = "HIGH"
            kind = "IP-based URL"

        elif "suspicious keyword" in lower:
            points = 10
            severity = "LOW"
            kind = "Suspicious keyword"

        elif "@" in lower:
            points = 20
            severity = "MEDIUM"
            kind = "URL obfuscation"

        elif "subdomain" in lower:
            points = 15
            severity = "MEDIUM"
            kind = "Excessive subdomains"

        else:
            points = 5
            severity = "LOW"
            kind = "Suspicious URL indicator"

        score += points

        add_finding(
            findings,
            kind,
            severity,
            text,
            points,
            "url_analyzer"
        )

    if url_data.get(
        "protocol"
    ) == "http":

        points = 15
        score += points

        add_finding(
            findings,
            "Unencrypted HTTP",
            "MEDIUM",
            "The URL uses HTTP instead of HTTPS.",
            points,
            "url_analyzer"
        )

    status = http_data.get(
        "status_code"
    )

    if isinstance(status, int):

        if status >= 500:

            points = 10
            score += points

            add_finding(
                findings,
                "Server error",
                "LOW",
                f"HTTP status {status}.",
                points,
                "http_analyzer"
            )

        elif status >= 400:

            points = 5
            score += points

            add_finding(
                findings,
                "HTTP error response",
                "LOW",
                f"HTTP status {status}.",
                points,
                "http_analyzer"
            )

    for indicator in http_data.get(
        "suspicious_indicators",
        []
    ):

        text = str(indicator)
        lower = text.lower()

        if (
            "header missing" in lower
            or "does not include hsts" in lower
        ):

            points = 2
            kind = "HTTP security weakness"
            severity = "LOW"

        elif "password submission" in lower:

            points = 3
            kind = "Password form detected"
            severity = "LOW"

        elif "obfuscated javascript" in lower:

            points = 8
            kind = "Potential JavaScript obfuscation"
            severity = "MEDIUM"

        else:

            points = 3
            kind = "HTTP indicator"
            severity = "LOW"

        score += points

        add_finding(
            findings,
            kind,
            severity,
            text,
            points,
            "http_analyzer"
        )

    if redirect_data.get(
        "redirect_count",
        0
    ) >= 5:

        points = 15
        score += points

        add_finding(
            findings,
            "Large redirect chain",
            "MEDIUM",
            f"{redirect_data['redirect_count']} redirects detected.",
            points,
            "redirect_analyzer"
        )

    if redirect_data.get(
        "domain_changes"
    ):

        points = 20
        score += points

        add_finding(
            findings,
            "Domain change",
            "MEDIUM",
            "Redirect chain changed domains.",
            points,
            "redirect_analyzer"
        )

    for indicator in tls_data.get(
        "suspicious_indicators",
        []
    ):

        text = str(indicator)
        lower = text.lower()

        if "expired" in lower:

            points = 15
            severity = "MEDIUM"

        elif "legacy tls" in lower:

            points = 15
            severity = "MEDIUM"

        elif "expires within 30 days" in lower:

            points = 2
            severity = "LOW"

        elif "hostname not directly present" in lower:

            points = 10
            severity = "MEDIUM"

        else:

            points = 3
            severity = "LOW"

        score += points

        add_finding(
            findings,
            "TLS certificate issue",
            severity,
            text,
            points,
            "tls_analyzer"
        )

    summary = ioc_data.get(
        "summary",
        {}
    )

    if summary.get(
        "primary_count",
        0
    ):

        findings.append({
            "type":
                "Primary IOCs observed",
            "severity":
                "INFO",
            "description":
                f"{summary['primary_count']} primary IOC(s) extracted.",
            "points":
                0,
            "source":
                "ioc_analyzer"
        })

    if summary.get(
        "supporting_count",
        0
    ):

        findings.append({
            "type":
                "Supporting infrastructure",
            "severity":
                "INFO",
            "description":
                f"{summary['supporting_count']} supporting IOC(s) observed.",
            "points":
                0,
            "source":
                "ioc_analyzer"
        })

    for finding in correlation_data.get(
        "findings",
        []
    ):

        finding_type = finding.get(
            "type",
            ""
        )

        if finding_type == "dns_ip_mismatch":

            points = 20
            score += points

            add_finding(
                findings,
                "DNS/IP mismatch",
                "MEDIUM",
                finding.get(
                    "message",
                    "DNS and IP information differ."
                ),
                points,
                "correlation_engine"
            )

        elif finding_type == "certificate_domain_mismatch":

            points = 10
            score += points

            add_finding(
                findings,
                "Certificate/domain mismatch",
                "MEDIUM",
                finding.get(
                    "message",
                    "Certificate SAN does not match the domain."
                ),
                points,
                "correlation_engine"
            )

        elif finding_type in (
            "cross_source_match",
            "infrastructure_profile",
            "certificate_domain_match"
        ):

            findings.append({
                "type":
                    "Corroborated evidence",
                "severity":
                    "INFO",
                "description":
                    finding.get(
                        "message",
                        "Evidence corroborated."
                    ),
                "points":
                    0,
                "source":
                    "correlation_engine"
            })

    score += apply_threat_intelligence(
        findings,
        threat_intel_data
    )

    score = max(
        0,
        min(score, 100)
    )

    return {
        "risk_score": score,
        "risk_level": get_risk_level(score),
        "findings": findings,
        "engine_version": "5.1"
    }


# ==========================================
# COMPATIBILITY
# ==========================================

def calculate_url_risk(url_data):

    return calculate_combined_url_risk(
        url_data=url_data
    )
