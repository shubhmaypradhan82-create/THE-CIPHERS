import re
import unicodedata
from urllib.parse import urlparse


def analyze_domain(url):

    result = {
        "url": url,
        "domain": None,
        "normalized_domain": None,
        "is_punycode": False,
        "has_unicode": False,
        "mixed_script": False,
        "subdomain_count": 0,
        "indicators": []
    }

    # ==========================================
    # PARSE DOMAIN
    # ==========================================

    try:

        working_url = url

        if not working_url.startswith(
            ("http://", "https://")
        ):
            working_url = "http://" + working_url

        parsed = urlparse(working_url)

        domain = parsed.hostname

        if not domain:

            result["indicators"].append(
                "Unable to extract domain"
            )

            return result

        result["domain"] = domain

    except Exception as e:

        result["indicators"].append(
            f"Domain parsing failed: {str(e)}"
        )

        return result

    # ==========================================
    # NORMALIZE DOMAIN
    # ==========================================

    normalized = unicodedata.normalize(
        "NFKC",
        domain
    )

    result["normalized_domain"] = normalized

    # ==========================================
    # PUNYCODE
    # ==========================================

    if "xn--" in domain.lower():

        result["is_punycode"] = True

        result["indicators"].append(
            "Punycode domain detected"
        )

    # ==========================================
    # UNICODE
    # ==========================================

    has_unicode = any(
        ord(char) > 127
        for char in domain
    )

    result["has_unicode"] = has_unicode

    if has_unicode:

        result["indicators"].append(
            "Unicode characters detected in domain"
        )

    # ==========================================
    # MIXED ASCII + UNICODE
    # ==========================================

    has_ascii = any(
        ord(char) <= 127
        for char in domain
    )

    if has_ascii and has_unicode:

        result["mixed_script"] = True

        result["indicators"].append(
            "Mixed ASCII and Unicode characters detected"
        )

    # ==========================================
    # SUBDOMAIN COUNT
    # ==========================================

    parts = domain.split(".")

    # Remove empty parts
    parts = [
        part for part in parts
        if part
    ]

    # Example:
    # login.account.example.com
    # login + account = 2 subdomains

    if len(parts) >= 3:

        subdomain_count = len(parts) - 2

    else:

        subdomain_count = 0

    result["subdomain_count"] = subdomain_count

    if subdomain_count >= 3:

        result["indicators"].append(
            "Multiple subdomain levels detected"
        )

    # ==========================================
    # SUSPICIOUS DOMAIN LENGTH
    # ==========================================

    if len(domain) > 60:

        result["indicators"].append(
            "Unusually long domain detected"
        )

    # ==========================================
    # NUMERIC DOMAIN
    # ==========================================

    if re.fullmatch(
        r"[0-9.]+",
        domain
    ):

        result["indicators"].append(
            "Domain consists primarily of numbers"
        )

    return result
