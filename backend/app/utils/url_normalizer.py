from urllib.parse import (
    urlparse,
    unquote
)
import re


def normalize_url(url):

    result = {
        "original_url": url,
        "normalized_url": None,
        "decoded_url": None,
        "hostname": None,
        "is_encoded": False,
        "has_credentials": False,
        "is_punycode": False,
        "indicators": []
    }


    # ==========================================
    # ADD PROTOCOL IF MISSING
    # ==========================================

    working_url = url

    if not working_url.startswith(
        ("http://", "https://")
    ):

        working_url = "http://" + working_url


    # ==========================================
    # URL DECODE
    # ==========================================

    decoded_url = unquote(working_url)

    result["normalized_url"] = working_url
    result["decoded_url"] = decoded_url


    # Detect encoding
    if decoded_url != working_url:

        result["is_encoded"] = True

        result["indicators"].append(
            "URL contains encoded characters"
        )


    # ==========================================
    # PARSE URL
    # ==========================================

    parsed = urlparse(working_url)

    hostname = parsed.hostname

    result["hostname"] = hostname


    # ==========================================
    # USERNAME / PASSWORD
    # ==========================================

    if parsed.username or parsed.password:

        result["has_credentials"] = True

        result["indicators"].append(
            "URL contains embedded credentials"
        )


    # ==========================================
    # PUNYCODE
    # ==========================================

    if hostname and hostname.lower().startswith(
        "xn--"
    ):

        result["is_punycode"] = True

        result["indicators"].append(
            "Punycode domain detected"
        )


    # ==========================================
    # HEX / ESCAPED CHARACTERS
    # ==========================================

    if re.search(
        r"%[0-9a-fA-F]{2}",
        url
    ):

        if "URL contains encoded characters" not in result["indicators"]:

            result["indicators"].append(
                "Percent-encoded characters detected"
            )


    return result
