def calculate_url_risk(url_data):

    score = 0
    findings = []

    indicators = url_data.get(
        "suspicious_indicators", []
    )

    # ==========================================
    # SUSPICIOUS INDICATORS
    # ==========================================

    for indicator in indicators:

        indicator_lower = indicator.lower()

        if "ip address" in indicator_lower:

            score += 30

            findings.append({
                "type": "IP-based URL",
                "severity": "HIGH",
                "description": indicator
            })

        elif "suspicious keyword" in indicator_lower:

            score += 10

            findings.append({
                "type": "Suspicious keyword",
                "severity": "LOW",
                "description": indicator
            })

        elif "@" in indicator_lower:

            score += 25

            findings.append({
                "type": "URL obfuscation",
                "severity": "MEDIUM",
                "description": indicator
            })

        elif "subdomain" in indicator_lower:

            score += 15

            findings.append({
                "type": "Excessive subdomains",
                "severity": "MEDIUM",
                "description": indicator
            })

        else:

            score += 10

            findings.append({
                "type": "Suspicious indicator",
                "severity": "LOW",
                "description": indicator
            })

    # ==========================================
    # HTTP WITHOUT HTTPS
    # ==========================================

    if url_data.get("protocol") == "http":

        score += 10

        findings.append({
            "type": "Unencrypted HTTP",
            "severity": "LOW",
            "description": (
                "The URL uses HTTP instead of HTTPS."
            )
        })

    # ==========================================
    # LIMIT SCORE
    # ==========================================

    score = min(score, 100)

    # ==========================================
    # RISK LEVEL
    # ==========================================

    if score >= 70:

        risk_level = "HIGH"

    elif score >= 40:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "findings": findings
    }
