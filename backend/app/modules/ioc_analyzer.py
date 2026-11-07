import re
import ipaddress
from urllib.parse import urlparse


EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@"
    r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

URL_PATTERN = re.compile(
    r"https?://[^\s\"'<>]+",
    re.IGNORECASE
)

DOMAIN_PATTERN = re.compile(
    r"\b(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}\b"
)

IPV4_PATTERN = re.compile(
    r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
)

MD5_PATTERN = re.compile(
    r"\b[a-fA-F0-9]{32}\b"
)

SHA1_PATTERN = re.compile(
    r"\b[a-fA-F0-9]{40}\b"
)

SHA256_PATTERN = re.compile(
    r"\b[a-fA-F0-9]{64}\b"
)


def clean_url(value):

    if value is None:
        return None

    value = str(value)

    # Convert escaped whitespace sequences
    # that may come from serialized email text.
    value = value.replace("\\r", "")
    value = value.replace("\\n", "")
    value = value.replace("\\t", "")

    # Remove actual whitespace at boundaries.
    value = value.strip()

    # Remove common punctuation accidentally
    # captured after URLs.
    value = value.rstrip(
        ".,;:!?)]}>\"'"
    )

    return value or None


def valid_ip(value):

    try:
        return ipaddress.ip_address(value)
    except ValueError:
        return None


def get_url_domain(url):

    try:
        parsed = urlparse(url)
        return parsed.hostname
    except Exception:
        return None


def unique(values):

    cleaned = []

    for value in values:

        if value is None:
            continue

        value = str(value).strip()

        if value:
            cleaned.append(value)

    return sorted(set(cleaned))


def extract_iocs(data):

    text = str(data)

    # ======================================
    # URLS
    # ======================================

    raw_urls = URL_PATTERN.findall(text)

    urls = []

    for raw_url in raw_urls:

        cleaned = clean_url(raw_url)

        if cleaned:
            urls.append(cleaned)

    urls = unique(urls)

    # ======================================
    # EMAILS
    # ======================================

    emails = unique(
        EMAIL_PATTERN.findall(text)
    )

    # ======================================
    # IPV4
    # ======================================

    ipv4 = []

    for value in unique(
        IPV4_PATTERN.findall(text)
    ):

        ip = valid_ip(value)

        if ip and ip.version == 4:
            ipv4.append(value)

    # ======================================
    # HASHES
    # ======================================

    md5 = unique(
        MD5_PATTERN.findall(text)
    )

    sha1 = unique(
        SHA1_PATTERN.findall(text)
    )

    sha256 = unique(
        SHA256_PATTERN.findall(text)
    )

    # ======================================
    # DOMAINS
    # ======================================

    all_domains = unique(
        DOMAIN_PATTERN.findall(text)
    )

    url_domains = set()

    for url in urls:

        domain = get_url_domain(url)

        if domain:
            url_domains.add(
                domain.lower()
            )

    email_domains = set()

    for email in emails:

        if "@" in email:

            email_domains.add(
                email.split("@", 1)[1].lower()
            )

    domains = []
    supporting_domains = []

    for domain in all_domains:

        lower = domain.lower()

        if lower in email_domains:
            continue

        if lower in url_domains:
            domains.append(domain)
        else:
            supporting_domains.append(domain)

    # ======================================
    # PRIMARY IOCs
    # ======================================

    primary_iocs = []

    for url in urls:

        primary_iocs.append({
            "type": "url",
            "value": url,
            "classification": "primary",
            "confidence": "high"
        })

    for domain in domains:

        primary_iocs.append({
            "type": "domain",
            "value": domain,
            "classification": "primary",
            "confidence": "high"
        })

    for email in emails:

        primary_iocs.append({
            "type": "email",
            "value": email,
            "classification": "primary",
            "confidence": "high"
        })

    for value in md5:

        primary_iocs.append({
            "type": "hash",
            "algorithm": "md5",
            "value": value,
            "classification": "primary",
            "confidence": "high"
        })

    for value in sha1:

        primary_iocs.append({
            "type": "hash",
            "algorithm": "sha1",
            "value": value,
            "classification": "primary",
            "confidence": "high"
        })

    for value in sha256:

        primary_iocs.append({
            "type": "hash",
            "algorithm": "sha256",
            "value": value,
            "classification": "primary",
            "confidence": "high"
        })

    # ======================================
    # SUPPORTING IOCs
    # ======================================

    supporting_iocs = []

    for ip in ipv4:

        supporting_iocs.append({
            "type": "ipv4",
            "value": ip,
            "classification": "supporting",
            "confidence": "high"
        })

    for domain in supporting_domains:

        supporting_iocs.append({
            "type": "domain",
            "value": domain,
            "classification": "supporting",
            "confidence": "medium"
        })

    # ======================================
    # RESULT
    # ======================================

    return {

        "primary_iocs":
            primary_iocs,

        "supporting_iocs":
            supporting_iocs,

        "summary": {

            "primary_count":
                len(primary_iocs),

            "supporting_count":
                len(supporting_iocs),

            "url_count":
                len(urls),

            "domain_count":
                len(domains),

            "supporting_domain_count":
                len(supporting_domains),

            "ipv4_count":
                len(ipv4),

            "email_count":
                len(emails),

            "md5_count":
                len(md5),

            "sha1_count":
                len(sha1),

            "sha256_count":
                len(sha256)

        },

        "urls":
            urls,

        "domains":
            domains,

        "supporting_domains":
            supporting_domains,

        "ipv4":
            ipv4,

        "ipv6":
            [],

        "emails":
            emails,

        "hashes": {

            "md5":
                md5,

            "sha1":
                sha1,

            "sha256":
                sha256

        }

    }
