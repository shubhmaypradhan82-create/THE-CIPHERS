import os
import requests
from urllib.parse import urlparse


def analyze_redirects(url):

    result = {
        "original_url": url,
        "final_url": None,
        "redirect_count": 0,
        "redirect_chain": [],
        "domain_changes": [],
        "protocol_changes": [],
        "suspicious_indicators": [],
        "errors": []
    }

    if not url:
        result["errors"].append(
            "No URL provided"
        )
        return result

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    try:

        response = requests.get(
            url,
            allow_redirects=True,
            timeout=float(os.getenv("FORENSIC_HTTP_TIMEOUT", "3")),
            headers={
                "User-Agent":
                "ForensicEngine/1.0"
            }
        )

        result["final_url"] = response.url

        history = response.history

        result["redirect_count"] = len(history)

        previous_url = url

        for index, redirect in enumerate(history):

            current_url = redirect.url
            next_url = redirect.headers.get(
                "Location"
            )

            if not next_url:
                next_url = response.url

            previous_parsed = urlparse(
                current_url
            )

            next_parsed = urlparse(
                next_url
            )

            current_domain = (
                previous_parsed.hostname
            )

            next_domain = (
                next_parsed.hostname
            )

            current_protocol = (
                previous_parsed.scheme
            )

            next_protocol = (
                next_parsed.scheme
            )

            result["redirect_chain"].append({
                "step": index + 1,
                "status_code":
                    redirect.status_code,
                "from": current_url,
                "to": next_url,
                "from_domain":
                    current_domain,
                "to_domain":
                    next_domain,
                "from_protocol":
                    current_protocol,
                "to_protocol":
                    next_protocol
            })

            if (
                current_domain
                and next_domain
                and current_domain.lower()
                != next_domain.lower()
            ):

                result["domain_changes"].append({
                    "from":
                        current_domain,
                    "to":
                        next_domain
                })

            if (
                current_protocol
                and next_protocol
                and current_protocol
                != next_protocol
            ):

                result["protocol_changes"].append({
                    "from":
                        current_protocol,
                    "to":
                        next_protocol
                })

            previous_url = next_url

        # ======================================
        # SUSPICIOUS REDIRECT CONDITIONS
        # ======================================

        if result["redirect_count"] >= 5:

            result["suspicious_indicators"].append(
                "Large redirect chain detected"
            )

        if result["redirect_count"] >= 10:

            result["suspicious_indicators"].append(
                "Excessive number of redirects"
            )

        if len(result["domain_changes"]) >= 2:

            result["suspicious_indicators"].append(
                "Multiple domain changes detected"
            )

        original_domain = urlparse(
            url
        ).hostname

        final_domain = urlparse(
            result["final_url"]
        ).hostname

        if (
            original_domain
            and final_domain
            and original_domain.lower()
            != final_domain.lower()
        ):

            result["suspicious_indicators"].append(
                "Final URL uses a different domain"
            )

        # ======================================
        # HTTP TO HTTPS
        # ======================================

        if (
            urlparse(url).scheme == "http"
            and result["final_url"]
            and urlparse(
                result["final_url"]
            ).scheme == "https"
        ):

            result["suspicious_indicators"].append(
                "URL upgraded from HTTP to HTTPS"
            )

    except requests.exceptions.Timeout:

        result["errors"].append(
            "Redirect analysis timed out"
        )

    except requests.exceptions.TooManyRedirects:

        result["errors"].append(
            "Too many redirects"
        )

    except requests.exceptions.RequestException as e:

        result["errors"].append(
            f"HTTP request failed: {str(e)}"
        )

    except Exception as e:

        result["errors"].append(
            f"Redirect analysis failed: {str(e)}"
        )

    return result
