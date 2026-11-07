from urllib.parse import urlparse


def get_domain(value):

    if not value:
        return None

    value = str(value).strip()

    if "@" in value:
        return (
            value.rsplit("@", 1)[1]
            .strip()
            .lower()
            .rstrip(">")
        )

    return value.lower().rstrip(".")


def normalize_domain(value):

    if not value:
        return None

    value = str(value).strip().lower()

    if "@" in value:
        value = value.rsplit("@", 1)[1]

    return value.rstrip(".>")


def collect_url_domains(analyzed_urls):

    domains = set()

    for item in analyzed_urls or []:

        url_data = item.get(
            "url_analysis",
            {}
        )

        domain = normalize_domain(
            url_data.get("domain")
        )

        if domain:
            domains.add(domain)

    return domains


def collect_url_ips(analyzed_urls):

    ips = set()

    for item in analyzed_urls or []:

        url_data = item.get(
            "url_analysis",
            {}
        )

        ip = url_data.get(
            "ip_address"
        )

        if ip:
            ips.add(str(ip))

    return ips


def collect_received_hosts(email_data):

    hosts = set()
    ips = set()

    for hop in email_data.get(
        "received_chain",
        []
    ):

        host = hop.get(
            "from_host"
        )

        ip = hop.get(
            "from_ip"
        )

        if host:
            hosts.add(
                normalize_domain(host)
            )

        if ip:
            ips.add(
                str(ip)
            )

    return hosts, ips


def correlate_email_infrastructure(
    email_data=None,
    analyzed_urls=None
):

    email_data = email_data or {}
    analyzed_urls = analyzed_urls or []

    findings = []
    relationships = []

    # ======================================
    # EMAIL DOMAINS
    # ======================================

    sender_domain = get_domain(
        email_data.get("from")
    )

    reply_domain = get_domain(
        email_data.get("reply_to")
    )

    return_domain = get_domain(
        email_data.get("return_path")
    )

    email_domains = {
        domain
        for domain in (
            sender_domain,
            reply_domain,
            return_domain
        )
        if domain
    }

    # ======================================
    # URL INFRASTRUCTURE
    # ======================================

    url_domains = collect_url_domains(
        analyzed_urls
    )

    url_ips = collect_url_ips(
        analyzed_urls
    )

    # ======================================
    # RECEIVED INFRASTRUCTURE
    # ======================================

    received_hosts, received_ips = (
        collect_received_hosts(
            email_data
        )
    )

    # ======================================
    # EMAIL DOMAIN ↔ URL DOMAIN
    # ======================================

    for email_domain in email_domains:

        if email_domain in url_domains:

            relationships.append({
                "source":
                    email_domain,
                "relation":
                    "appears_in_email_and_url",
                "target":
                    email_domain,
                "confidence":
                    "high",
                "evidence_strength":
                    95
            })

            findings.append({
                "type":
                    "email_url_domain_match",
                "severity":
                    "info",
                "confidence":
                    "high",
                "evidence_strength":
                    95,
                "message":
                    "Email domain matches a domain used by an analyzed URL.",
                "evidence": {
                    "domain":
                        email_domain
                }
            })

    # ======================================
    # RECEIVED HOST ↔ URL DOMAIN
    # ======================================

    for host in received_hosts:

        if not host:
            continue

        if host in url_domains:

            relationships.append({
                "source":
                    host,
                "relation":
                    "received_host_matches_url_domain",
                "target":
                    host,
                "confidence":
                    "medium",
                "evidence_strength":
                    85
            })

            findings.append({
                "type":
                    "received_host_url_match",
                "severity":
                    "info",
                "confidence":
                    "medium",
                "evidence_strength":
                    85,
                "message":
                    "A Received-chain hostname matches an analyzed URL domain.",
                "evidence": {
                    "host":
                        host
                }
            })

    # ======================================
    # RECEIVED IP ↔ URL IP
    # ======================================

    for ip in received_ips:

        if ip in url_ips:

            relationships.append({
                "source":
                    ip,
                "relation":
                    "received_ip_matches_url_ip",
                "target":
                    ip,
                "confidence":
                    "high",
                "evidence_strength":
                    95
            })

            findings.append({
                "type":
                    "received_ip_url_match",
                "severity":
                    "info",
                "confidence":
                    "high",
                "evidence_strength":
                    95,
                "message":
                    "A Received-chain IP matches an analyzed URL IP.",
                "evidence": {
                    "ip":
                        ip
                }
            })

    # ======================================
    # SENDER ↔ REPLY-TO
    # ======================================

    if (
        sender_domain
        and reply_domain
        and sender_domain != reply_domain
    ):

        relationships.append({
            "source":
                sender_domain,
            "relation":
                "reply_to_domain",
            "target":
                reply_domain,
            "confidence":
                "high",
            "evidence_strength":
                90
        })

        findings.append({
            "type":
                "reply_to_domain_mismatch",
            "severity":
                "warning",
            "confidence":
                "high",
            "evidence_strength":
                90,
            "message":
                "Reply-To domain differs from sender domain.",
            "evidence": {
                "sender_domain":
                    sender_domain,
                "reply_to_domain":
                    reply_domain
            }
        })

    # ======================================
    # SENDER ↔ RETURN-PATH
    # ======================================

    if (
        sender_domain
        and return_domain
        and sender_domain != return_domain
    ):

        relationships.append({
            "source":
                sender_domain,
            "relation":
                "return_path_domain",
            "target":
                return_domain,
            "confidence":
                "medium",
            "evidence_strength":
                85
        })

        findings.append({
            "type":
                "return_path_domain_mismatch",
            "severity":
                "info",
            "confidence":
                "medium",
            "evidence_strength":
                85,
            "message":
                "Return-Path domain differs from sender domain.",
            "evidence": {
                "sender_domain":
                    sender_domain,
                "return_path_domain":
                    return_domain
            }
        })

    # ======================================
    # URL COUNT / INFRASTRUCTURE SUMMARY
    # ======================================

    summary = {
        "sender_domain":
            sender_domain,

        "reply_to_domain":
            reply_domain,

        "return_path_domain":
            return_domain,

        "email_domain_count":
            len(email_domains),

        "url_domain_count":
            len(url_domains),

        "url_ip_count":
            len(url_ips),

        "received_host_count":
            len(received_hosts),

        "received_ip_count":
            len(received_ips),

        "relationships":
            len(relationships),

        "findings":
            len(findings)
    }

    return {
        "findings": findings,
        "relationships": relationships,
        "summary": summary
    }
