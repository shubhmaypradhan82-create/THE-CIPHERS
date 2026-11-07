import os
import socket
import ssl
from datetime import datetime, timezone
from urllib.parse import urlparse


def parse_certificate_time(value):

    if not value:
        return None

    try:
        dt = datetime.strptime(
            value,
            "%b %d %H:%M:%S %Y %Z"
        )

        return dt.replace(
            tzinfo=timezone.utc
        ).isoformat()

    except ValueError:
        return value


def get_days_remaining(not_after):

    if not not_after:
        return None

    try:

        dt = datetime.strptime(
            not_after,
            "%b %d %H:%M:%S %Y %Z"
        ).replace(
            tzinfo=timezone.utc
        )

        now = datetime.now(
            timezone.utc
        )

        return (dt - now).days

    except ValueError:

        return None


def analyze_tls(url):

    result = {
        "url": url,
        "hostname": None,
        "port": 443,
        "tls_version": None,
        "cipher": None,
        "certificate": {
            "subject": None,
            "issuer": None,
            "serial_number": None,
            "version": None,
            "not_before": None,
            "not_after": None,
            "days_remaining": None,
            "san": [],
            "is_expired": None
        },
        "suspicious_indicators": [],
        "errors": []
    }

    if not url:
        result["errors"].append(
            "No URL provided"
        )
        return result

    try:

        if not url.startswith(
            ("http://", "https://")
        ):
            url = "https://" + url

        parsed = urlparse(url)

        hostname = parsed.hostname

        port = parsed.port or 443

        result["hostname"] = hostname
        result["port"] = port

        if not hostname:

            result["errors"].append(
                "Could not determine hostname"
            )

            return result

        # TLS connections are meaningful for HTTPS.
        if parsed.scheme.lower() != "https":

            result["errors"].append(
                "TLS analysis requires an HTTPS URL"
            )

            return result

        context = ssl.create_default_context()

        with socket.create_connection(
            (hostname, port),
            timeout=float(os.getenv("FORENSIC_TLS_TIMEOUT", "3"))
        ) as raw_socket:

            with context.wrap_socket(
                raw_socket,
                server_hostname=hostname
            ) as tls_socket:

                result["tls_version"] = (
                    tls_socket.version()
                )

                cipher = tls_socket.cipher()

                if cipher:
                    result["cipher"] = {
                        "name": cipher[0],
                        "protocol": cipher[1],
                        "bits": cipher[2]
                    }

                certificate = (
                    tls_socket.getpeercert()
                )

                # ==================================
                # SUBJECT
                # ==================================

                subject_parts = []

                for group in certificate.get(
                    "subject",
                    []
                ):

                    for key, value in group:

                        subject_parts.append({
                            "key": key,
                            "value": value
                        })

                result["certificate"]["subject"] = (
                    subject_parts
                )

                # ==================================
                # ISSUER
                # ==================================

                issuer_parts = []

                for group in certificate.get(
                    "issuer",
                    []
                ):

                    for key, value in group:

                        issuer_parts.append({
                            "key": key,
                            "value": value
                        })

                result["certificate"]["issuer"] = (
                    issuer_parts
                )

                # ==================================
                # SERIAL / VERSION
                # ==================================

                result["certificate"]["serial_number"] = (
                    certificate.get(
                        "serialNumber"
                    )
                )

                result["certificate"]["version"] = (
                    certificate.get(
                        "version"
                    )
                )

                # ==================================
                # VALIDITY
                # ==================================

                not_before = certificate.get(
                    "notBefore"
                )

                not_after = certificate.get(
                    "notAfter"
                )

                result["certificate"]["not_before"] = (
                    parse_certificate_time(
                        not_before
                    )
                )

                result["certificate"]["not_after"] = (
                    parse_certificate_time(
                        not_after
                    )
                )

                days_remaining = (
                    get_days_remaining(
                        not_after
                    )
                )

                result["certificate"][
                    "days_remaining"
                ] = days_remaining

                if days_remaining is not None:

                    result["certificate"][
                        "is_expired"
                    ] = days_remaining < 0

                # ==================================
                # SUBJECT ALTERNATIVE NAMES
                # ==================================

                san = []

                for item in certificate.get(
                    "subjectAltName",
                    []
                ):

                    if len(item) == 2:

                        san.append({
                            "type": item[0],
                            "value": item[1]
                        })

                result["certificate"]["san"] = san

                # ==================================
                # TLS FINDINGS
                # ==================================

                if result["certificate"]["is_expired"]:

                    result["suspicious_indicators"].append(
                        "TLS certificate is expired"
                    )

                elif (
                    days_remaining is not None
                    and days_remaining <= 30
                ):

                    result["suspicious_indicators"].append(
                        "TLS certificate expires within 30 days"
                    )

                if (
                    result["tls_version"]
                    in ("TLSv1", "TLSv1.1")
                ):

                    result["suspicious_indicators"].append(
                        "Legacy TLS version detected"
                    )

                # ==================================
                # SAN HOSTNAME CHECK
                # ==================================

                san_values = [
                    item["value"].lower()
                    for item in san
                    if item.get("value")
                ]

                if hostname.lower() not in san_values:

                    wildcard_match = False

                    for name in san_values:

                        if (
                            name.startswith("*.")
                            and hostname.lower().endswith(
                                name[1:]
                            )
                        ):
                            wildcard_match = True
                            break

                    if not wildcard_match:

                        result["suspicious_indicators"].append(
                            "Hostname not directly present in certificate SANs"
                        )

    except ssl.SSLCertVerificationError as exc:

        result["errors"].append(
            f"Certificate verification failed: {str(exc)}"
        )

    except ssl.SSLError as exc:

        result["errors"].append(
            f"TLS connection failed: {str(exc)}"
        )

    except socket.timeout:

        result["errors"].append(
            "TLS connection timed out"
        )

    except OSError as exc:

        result["errors"].append(
            f"Network connection failed: {str(exc)}"
        )

    except Exception as exc:

        result["errors"].append(
            f"TLS analysis failed: {str(exc)}"
        )

    return result
