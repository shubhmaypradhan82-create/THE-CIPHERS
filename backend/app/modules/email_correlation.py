import re
from urllib.parse import urlparse


EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@"
    r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

URL_PATTERN = re.compile(
    r"https?://[^\s\"'<>]+",
    re.IGNORECASE
)


def clean_url(url):

    if not url:
        return None

    url = str(url).strip()

    # Remove common trailing characters
    url = url.rstrip(
        " \t\r\n,.;:!?)]}>\"'"
    )

    return url or None


def normalize_domain(value):

    if not value:
        return None

    value = str(value).strip().lower()

    if "@" in value:
        value = value.split("@", 1)[1]

    if value.startswith(
        ("http://", "https://")
    ):
        parsed = urlparse(value)
        value = parsed.hostname or ""

    value = value.rstrip(".")

    return value or None


def extract_email_addresses(email_data):

    addresses = set()

    fields = [
        "from",
        "to",
        "reply_to",
        "body"
    ]

    for field in fields:

        value = email_data.get(field)

        if not value:
            continue

        if isinstance(value, list):
            values = value
        else:
            values = [value]

        for item in values:

            matches = EMAIL_PATTERN.findall(
                str(item)
            )

            addresses.update(
                match.lower()
                for match in matches
            )

    for header in email_data.get(
        "received",
        []
    ):

        matches = EMAIL_PATTERN.findall(
            str(header)
        )

        addresses.update(
            match.lower()
            for match in matches
        )

    return sorted(addresses)


def extract_urls_from_email(email_data):

    urls = set()

    fields = [
        "from",
        "to",
        "reply_to",
        "subject",
        "body"
    ]

    for field in fields:

        value = email_data.get(field)

        if not value:
            continue

        if isinstance(value, list):
            values = value
        else:
            values = [value]

        for item in values:

            matches = URL_PATTERN.findall(
                str(item)
            )

            for match in matches:

                cleaned = clean_url(
                    match
                )

                if cleaned:
                    urls.add(
                        cleaned
                    )

    for header in email_data.get(
        "received",
        []
    ):

        matches = URL_PATTERN.findall(
            str(header)
        )

        for match in matches:

            cleaned = clean_url(
                match
            )

            if cleaned:
                urls.add(
                    cleaned
                )

    return sorted(urls)


def extract_url_domain(url):

    try:

        parsed = urlparse(
            url
        )

        return parsed.hostname

    except Exception:

        return None


def correlate_email_with_urls(
    email_data=None,
    url_analyses=None
):

    email_data = email_data or {}

    url_analyses = url_analyses or []

    email_addresses = (
        extract_email_addresses(
            email_data
        )
    )

    email_domains = set()

    for address in email_addresses:

        domain = normalize_domain(
            address
        )

        if domain:
            email_domains.add(
                domain
            )

    email_urls = (
        extract_urls_from_email(
            email_data
        )
    )

    normalized_email_urls = {
        url.rstrip("/")
        for url in email_urls
    }

    findings = []
    matches = []

    # ======================================
    # EMAIL URLs vs ANALYZED URLs
    # ======================================

    for analysis in url_analyses:

        if not isinstance(
            analysis,
            dict
        ):
            continue

        url_data = analysis.get(
            "url_analysis",
            analysis
        )

        url = url_data.get(
            "url"
        )

        domain = normalize_domain(
            url_data.get("domain")
        )

        if not url:
            continue

        clean_analyzed_url = clean_url(
            url
        )

        # ----------------------------------
        # DOMAIN MATCH
        # ----------------------------------

        if (
            domain
            and domain in email_domains
        ):

            match = {
                "type":
                    "email_domain_match",

                "email_domain":
                    domain,

                "url":
                    clean_analyzed_url,

                "confidence":
                    "high",

                "evidence_strength":
                    95
            }

            matches.append(
                match
            )

            findings.append({

                "type":
                    "email_domain_match",

                "severity":
                    "info",

                "message":
                    "URL domain matches a domain found in the email.",

                "confidence":
                    "high",

                "evidence_strength":
                    95,

                "evidence": {

                    "domain":
                        domain,

                    "url":
                        clean_analyzed_url

                }

            })

        # ----------------------------------
        # DIRECT URL MATCH
        # ----------------------------------

        if (
            clean_analyzed_url
            and clean_analyzed_url.rstrip("/")
            in normalized_email_urls
        ):

            match = {

                "type":
                    "email_url_match",

                "email_url":
                    clean_analyzed_url,

                "url":
                    clean_analyzed_url,

                "confidence":
                    "very_high",

                "evidence_strength":
                    100

            }

            matches.append(
                match
            )

            findings.append({

                "type":
                    "email_url_match",

                "severity":
                    "info",

                "message":
                    "URL found directly in email evidence.",

                "confidence":
                    "very_high",

                "evidence_strength":
                    100,

                "evidence": {

                    "url":
                        clean_analyzed_url

                }

            })

    # ======================================
    # EMAIL BODY URLS
    # ======================================

    analyzed_domains = set()

    for analysis in url_analyses:

        if not isinstance(
            analysis,
            dict
        ):
            continue

        url_data = analysis.get(
            "url_analysis",
            analysis
        )

        domain = normalize_domain(
            url_data.get("domain")
        )

        if domain:
            analyzed_domains.add(
                domain
            )

    for email_url in email_urls:

        email_url_domain = (
            normalize_domain(
                extract_url_domain(
                    email_url
                )
            )
        )

        if (
            email_url_domain
            and email_url_domain
            in analyzed_domains
        ):
            continue

        # URL exists in email but has
        # not yet been analyzed.

        findings.append({

            "type":
                "email_url_observed",

            "severity":
                "info",

            "message":
                "URL extracted from email body/header evidence.",

            "confidence":
                "high",

            "evidence_strength":
                95,

            "evidence": {

                "url":
                    email_url

            }

        })

    # ======================================
    # REPLY-TO MISMATCH
    # ======================================

    sender = email_data.get(
        "from"
    )

    reply_to = email_data.get(
        "reply_to"
    )

    if sender and reply_to:

        sender_domain = normalize_domain(
            sender
        )

        reply_domain = normalize_domain(
            reply_to
        )

        if (
            sender_domain
            and reply_domain
            and sender_domain
            != reply_domain
        ):

            findings.append({

                "type":
                    "reply_to_domain_mismatch",

                "severity":
                    "warning",

                "message":
                    "Email Reply-To domain differs from sender domain.",

                "confidence":
                    "high",

                "evidence_strength":
                    90,

                "evidence": {

                    "sender_domain":
                        sender_domain,

                    "reply_to_domain":
                        reply_domain

                }

            })

    # ======================================
    # RESULT
    # ======================================

    return {

        "email_addresses":
            email_addresses,

        "email_domains":
            sorted(email_domains),

        "email_urls":
            email_urls,

        "url_matches":
            matches,

        "findings":
            findings,

        "summary": {

            "email_address_count":
                len(email_addresses),

            "email_domain_count":
                len(email_domains),

            "email_url_count":
                len(email_urls),

            "url_match_count":
                len(matches),

            "finding_count":
                len(findings)

        }

    }
