import os
import dns.resolver


DNS_RECORD_TYPES = [
    "A",
    "AAAA",
    "CNAME",
    "MX",
    "NS",
    "TXT",
    "SOA",
    "CAA"
]


def resolve_records(domain, record_type):

    try:

        answers = dns.resolver.resolve(
            domain,
            record_type,
            lifetime=float(os.getenv("FORENSIC_DNS_TIMEOUT", "2"))
        )

        records = [
            str(answer)
            for answer in answers
        ]

        return records, None

    except Exception as exc:

        return [], str(exc)


def parse_mx_records(records):

    parsed = []

    for record in records:

        parts = record.split()

        if len(parts) >= 2:

            try:
                priority = int(parts[0])
            except ValueError:
                priority = None

            hostname = parts[1].rstrip(".")

            parsed.append({
                "priority": priority,
                "hostname": hostname,
                "raw": record
            })

        else:

            parsed.append({
                "priority": None,
                "hostname": record.rstrip("."),
                "raw": record
            })

    return parsed


def parse_soa_record(record):

    parts = record.split()

    if len(parts) < 7:
        return None

    return {
        "mname": parts[0].rstrip("."),
        "rname": parts[1].rstrip("."),
        "serial": parts[2],
        "refresh": parts[3],
        "retry": parts[4],
        "expire": parts[5],
        "minimum": parts[6],
        "raw": record
    }


def analyze_dns(domain):

    result = {
        "domain": domain,
        "A": [],
        "AAAA": [],
        "CNAME": [],
        "MX": [],
        "NS": [],
        "TXT": [],
        "SOA": [],
        "CAA": [],
        "structured": {
            "MX": [],
            "SOA": None,
            "CAA": []
        },
        "dnssec": {
            "present": False,
            "records": []
        },
        "record_counts": {},
        "findings": [],
        "errors": []
    }

    if not domain:

        result["errors"].append(
            "No domain provided"
        )

        return result

    # ======================================
    # DNS RECORD COLLECTION
    # ======================================

    for record_type in DNS_RECORD_TYPES:

        records, error = resolve_records(
            domain,
            record_type
        )

        result[record_type] = records

        if error:

            result["errors"].append(
                f"{record_type} lookup failed: {error}"
            )

    # ======================================
    # STRUCTURED MX
    # ======================================

    result["structured"]["MX"] = (
        parse_mx_records(
            result["MX"]
        )
    )

    # ======================================
    # STRUCTURED SOA
    # ======================================

    if result["SOA"]:

        result["structured"]["SOA"] = (
            parse_soa_record(
                result["SOA"][0]
            )
        )

    # ======================================
    # STRUCTURED CAA
    # ======================================

    for record in result["CAA"]:

        parts = record.split()

        if len(parts) >= 3:

            result["structured"]["CAA"].append({
                "flags": parts[0],
                "tag": parts[1],
                "value": " ".join(parts[2:]),
                "raw": record
            })

        else:

            result["structured"]["CAA"].append({
                "flags": None,
                "tag": None,
                "value": record,
                "raw": record
            })

    # ======================================
    # DNSSEC CHECK
    # ======================================

    dnskey_records, dnskey_error = (
        resolve_records(
            domain,
            "DNSKEY"
        )
    )

    if dnskey_records:

        result["dnssec"]["present"] = True
        result["dnssec"]["records"] = (
            dnskey_records
        )

    # DNSKEY failure is not automatically
    # treated as a malicious condition.

    # ======================================
    # RECORD COUNTS
    # ======================================

    for record_type in DNS_RECORD_TYPES:

        result["record_counts"][
            record_type
        ] = len(
            result.get(
                record_type,
                []
            )
        )

    # ======================================
    # DNS FINDINGS
    # ======================================

    if not result["A"] and not result["AAAA"]:

        result["findings"].append({
            "type": "no_address_records",
            "severity": "warning",
            "message":
                "Domain has no A or AAAA records."
        })

    if not result["NS"]:

        result["findings"].append({
            "type": "no_name_servers",
            "severity": "warning",
            "message":
                "No NS records were returned."
        })

    if len(result["NS"]) == 1:

        result["findings"].append({
            "type": "single_name_server",
            "severity": "info",
            "message":
                "Only one name server was returned."
        })

    if result["dnssec"]["present"]:

        result["findings"].append({
            "type": "dnssec_present",
            "severity": "info",
            "message":
                "DNSKEY records were found."
        })

    # ======================================
    # DNS SUMMARY
    # ======================================

    result["summary"] = {

        "has_ipv4":
            bool(result["A"]),

        "has_ipv6":
            bool(result["AAAA"]),

        "has_cname":
            bool(result["CNAME"]),

        "has_mx":
            bool(result["MX"]),

        "has_ns":
            bool(result["NS"]),

        "has_txt":
            bool(result["TXT"]),

        "has_soa":
            bool(result["SOA"]),

        "has_caa":
            bool(result["CAA"]),

        "dnssec":
            result["dnssec"]["present"],

        "error_count":
            len(result["errors"])

    }

    return result
