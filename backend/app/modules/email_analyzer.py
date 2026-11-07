from email import policy
from email.parser import BytesParser
import ipaddress
import re


IP_PATTERN = re.compile(
    r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
)


def extract_body(message):

    body_parts = []

    if message.is_multipart():

        for part in message.walk():

            content_type = part.get_content_type()

            disposition = str(
                part.get("Content-Disposition", "")
            ).lower()

            if "attachment" in disposition:
                continue

            if content_type in (
                "text/plain",
                "text/html"
            ):

                try:

                    content = part.get_content()

                    if content:
                        body_parts.append(content)

                except Exception:
                    pass

    else:

        try:

            content = message.get_content()

            if content:
                body_parts.append(content)

        except Exception:
            pass

    return "\n".join(body_parts)


def extract_ips(text):

    if not text:
        return []

    results = []

    for value in IP_PATTERN.findall(
        str(text)
    ):

        try:

            ip = ipaddress.ip_address(value)

            if ip.version == 4:
                results.append(value)

        except ValueError:
            pass

    return sorted(set(results))


def classify_ip(value):

    try:

        ip = ipaddress.ip_address(
            value
        )

        if ip.is_private:
            return "private"

        if ip.is_loopback:
            return "loopback"

        if ip.is_reserved:
            return "reserved"

        if ip.is_multicast:
            return "multicast"

        return "public"

    except ValueError:

        return "invalid"


def parse_received_header(header):

    result = {
        "raw": header,
        "from_host": None,
        "from_ip": None,
        "from_ip_classification": None,
        "by_host": None
    }

    if not header:
        return result

    text = str(header)

    from_match = re.search(
        r"\bfrom\s+([^\s(]+)",
        text,
        re.IGNORECASE
    )

    if from_match:

        result["from_host"] = (
            from_match.group(1)
        )

    by_match = re.search(
        r"\bby\s+([^\s(;]+)",
        text,
        re.IGNORECASE
    )

    if by_match:

        result["by_host"] = (
            by_match.group(1)
        )

    ips = extract_ips(text)

    if ips:

        result["from_ip"] = ips[0]

        result["from_ip_classification"] = (
            classify_ip(
                ips[0]
            )
        )

    return result


def analyze_authentication_headers(message):

    authentication = {
        "authentication_results": [],
        "spf": [],
        "dkim": [],
        "dmarc": []
    }

    authentication["authentication_results"] = (
        message.get_all(
            "Authentication-Results",
            []
        )
    )

    authentication["spf"] = (
        message.get_all(
            "Received-SPF",
            []
        )
    )

    authentication["dkim"] = (
        message.get_all(
            "DKIM-Signature",
            []
        )
    )

    dmarc_headers = []

    for header_name, header_value in message.items():

        if (
            header_name.lower()
            == "authentication-results"
            and "dmarc=" in
            str(header_value).lower()
        ):

            dmarc_headers.append(
                str(header_value)
            )

    authentication["dmarc"] = (
        dmarc_headers
    )

    return authentication


def build_received_summary(received_chain):

    source_ips = []
    source_hosts = []
    private_ips = []
    public_ips = []

    for hop in received_chain:

        ip = hop.get("from_ip")

        if ip and ip not in source_ips:

            source_ips.append(ip)

            classification = (
                hop.get(
                    "from_ip_classification"
                )
            )

            if classification == "private":
                private_ips.append(ip)

            elif classification == "public":
                public_ips.append(ip)

        host = hop.get("from_host")

        if (
            host
            and host not in source_hosts
        ):

            source_hosts.append(host)

    return {
        "hop_count":
            len(received_chain),

        "source_ip_count":
            len(source_ips),

        "source_ips":
            source_ips,

        "public_source_ips":
            public_ips,

        "private_source_ips":
            private_ips,

        "source_host_count":
            len(source_hosts),

        "source_hosts":
            source_hosts
    }


def analyze_email(file_path):

    with open(
        file_path,
        "rb"
    ) as f:

        message = BytesParser(
            policy=policy.default
        ).parse(f)

    received_headers = message.get_all(
        "Received",
        []
    )

    received_chain = []

    for index, header in enumerate(
        received_headers,
        start=1
    ):

        hop = parse_received_header(
            header
        )

        hop["hop"] = index

        received_chain.append(
            hop
        )

    authentication = (
        analyze_authentication_headers(
            message
        )
    )

    sender = message.get(
        "From"
    )

    reply_to = message.get(
        "Reply-To"
    )

    return_path = message.get(
        "Return-Path"
    )

    findings = []

    # ======================================
    # BASIC HEADER FINDINGS
    # ======================================

    if not sender:

        findings.append({
            "type": "missing_sender",
            "severity": "warning",
            "message":
                "From header is missing."
        })

    if not message.get("Date"):

        findings.append({
            "type": "missing_date",
            "severity": "info",
            "message":
                "Date header is missing."
        })

    if not message.get("Message-ID"):

        findings.append({
            "type": "missing_message_id",
            "severity": "info",
            "message":
                "Message-ID header is missing."
        })

    # ======================================
    # REPLY-TO
    # ======================================

    if sender and reply_to:

        if (
            "@" in str(sender)
            and "@" in str(reply_to)
        ):

            sender_domain = (
                str(sender)
                .split("@")[-1]
                .lower()
                .rstrip(">")
            )

            reply_domain = (
                str(reply_to)
                .split("@")[-1]
                .lower()
                .rstrip(">")
            )

            if sender_domain != reply_domain:

                findings.append({
                    "type":
                        "reply_to_domain_mismatch",
                    "severity":
                        "warning",
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
    # RETURN-PATH
    # ======================================

    if (
        sender
        and return_path
        and "@" in str(sender)
        and "@" in str(return_path)
    ):

        sender_domain = (
            str(sender)
            .split("@")[-1]
            .lower()
            .rstrip(">")
        )

        return_domain = (
            str(return_path)
            .split("@")[-1]
            .lower()
            .rstrip(">")
        )

        if sender_domain != return_domain:

            findings.append({
                "type":
                    "return_path_mismatch",
                "severity":
                    "info",
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
    # RECEIVED CHAIN
    # ======================================

    received_summary = (
        build_received_summary(
            received_chain
        )
    )

    if not received_chain:

        findings.append({
            "type":
                "missing_received_chain",
            "severity":
                "info",
            "message":
                "No Received headers were found."
        })

    for hop in received_chain:

        classification = hop.get(
            "from_ip_classification"
        )

        if classification in (
            "private",
            "loopback",
            "reserved"
        ):

            findings.append({
                "type":
                    "non_public_received_ip",
                "severity":
                    "info",
                "message":
                    "Received chain contains a non-public source IP.",
                "evidence": {
                    "hop":
                        hop.get("hop"),
                    "ip":
                        hop.get("from_ip"),
                    "classification":
                        classification
                }
            })

    # ======================================
    # AUTHENTICATION
    # ======================================

    if authentication[
        "authentication_results"
    ]:

        auth_text = " ".join(
            str(item)
            for item in
            authentication[
                "authentication_results"
            ]
        ).lower()

        if "spf=fail" in auth_text:

            findings.append({
                "type": "spf_fail",
                "severity": "warning",
                "message":
                    "Authentication-Results contains SPF failure."
            })

        if "dkim=fail" in auth_text:

            findings.append({
                "type": "dkim_fail",
                "severity": "warning",
                "message":
                    "Authentication-Results contains DKIM failure."
            })

        if "dmarc=fail" in auth_text:

            findings.append({
                "type": "dmarc_fail",
                "severity": "warning",
                "message":
                    "Authentication-Results contains DMARC failure."
            })

    # ======================================
    # FINAL RESULT
    # ======================================

    return {

        "from":
            sender,

        "to":
            message.get("To"),

        "subject":
            message.get("Subject"),

        "date":
            message.get("Date"),

        "message_id":
            message.get("Message-ID"),

        "reply_to":
            reply_to,

        "return_path":
            return_path,

        "received":
            [
                str(header)
                for header in received_headers
            ],

        "received_chain":
            received_chain,

        "received_hop_count":
            len(received_chain),

        "received_summary":
            received_summary,

        "authentication":
            authentication,

        "header_findings":
            findings,

        "body":
            extract_body(message)
    }
