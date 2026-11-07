from urllib.parse import urlparse
import socket
import re


def analyze_url(url):

    result = {
        "url": url,
        "protocol": None,
        "domain": None,
        "port": None,
        "ip_address": None,
        "suspicious_indicators": []
    }

    # Add protocol if missing
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)

    result["protocol"] = parsed.scheme
    result["domain"] = parsed.hostname
    result["port"] = parsed.port

    domain = parsed.hostname

    if not domain:
        result["suspicious_indicators"].append(
            "Invalid or missing domain"
        )
        return result

    # --------------------------------
    # Resolve domain to IP
    # --------------------------------

    try:

        ip = socket.gethostbyname(domain)
        result["ip_address"] = ip

    except socket.gaierror:

        result["suspicious_indicators"].append(
            "Domain could not be resolved"
        )

    # --------------------------------
    # Check IP address in URL
    # --------------------------------

    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"

    if re.match(ip_pattern, domain):

        result["suspicious_indicators"].append(
            "URL uses an IP address instead of a domain"
        )

    # --------------------------------
    # Check suspicious characters
    # --------------------------------

    if "@" in url:

        result["suspicious_indicators"].append(
            "URL contains @ symbol"
        )

    # --------------------------------
    # Check excessive subdomains
    # --------------------------------

    parts = domain.split(".")

    if len(parts) > 4:

        result["suspicious_indicators"].append(
            "Large number of subdomains"
        )

    # --------------------------------
    # Check suspicious words
    # --------------------------------

    suspicious_words = [
        "login",
        "verify",
        "verification",
        "password",
        "secure",
        "account",
        "update",
        "bank",
        "signin"
    ]

    url_lower = url.lower()

    for word in suspicious_words:

        if word in url_lower:

            result["suspicious_indicators"].append(
                f"Suspicious keyword: {word}"
            )

    return result
