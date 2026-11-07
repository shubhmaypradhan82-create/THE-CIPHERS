import re
import os
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def analyze_http(url):

    result = {
        "url": url,
        "status_code": None,
        "final_url": None,
        "server": None,
        "content_type": None,
        "content_length": None,
        "headers": {},
        "security_headers": {},
        "cookies": [],
        "content_analysis": {
            "title": None,
            "forms": 0,
            "password_fields": 0,
            "external_links": 0,
            "scripts": 0,
            "iframes": 0,
            "hidden_inputs": 0
        },
        "suspicious_indicators": [],
        "errors": []
    }

    if not url:
        result["errors"].append("No URL provided")
        return result

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    result["url"] = url

    try:
        response = requests.get(
            url,
            allow_redirects=True,
            timeout=float(os.getenv("FORENSIC_HTTP_TIMEOUT", "3")),
            headers={
                "User-Agent": "ForensicEngine/1.0"
            }
        )

        result["status_code"] = response.status_code
        result["final_url"] = response.url

        headers = response.headers

        result["server"] = headers.get("Server")
        result["content_type"] = headers.get("Content-Type")
        result["content_length"] = headers.get("Content-Length")

        for key, value in headers.items():
            result["headers"][key] = value

        security_header_names = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Referrer-Policy",
            "Permissions-Policy"
        ]

        for header_name in security_header_names:
            result["security_headers"][header_name] = (
                headers.get(header_name)
            )

        for cookie in response.cookies:
            result["cookies"].append({
                "name": cookie.name,
                "domain": cookie.domain,
                "path": cookie.path,
                "secure": cookie.secure,
                "httponly": cookie.has_nonstandard_attr("HttpOnly")
            })

        # ======================================
        # STATUS
        # ======================================

        if response.status_code >= 400:
            result["suspicious_indicators"].append(
                f"HTTP error status: {response.status_code}"
            )

        # ======================================
        # SECURITY HEADERS
        # ======================================

        scheme = urlparse(response.url).scheme

        if scheme == "https":

            if not headers.get("Strict-Transport-Security"):
                result["suspicious_indicators"].append(
                    "HTTPS response does not include HSTS"
                )

        if not headers.get("Content-Security-Policy"):
            result["suspicious_indicators"].append(
                "Content-Security-Policy header missing"
            )

        if not headers.get("X-Frame-Options"):
            result["suspicious_indicators"].append(
                "X-Frame-Options header missing"
            )

        if not headers.get("X-Content-Type-Options"):
            result["suspicious_indicators"].append(
                "X-Content-Type-Options header missing"
            )

        if not headers.get("Referrer-Policy"):
            result["suspicious_indicators"].append(
                "Referrer-Policy header missing"
            )

        # ======================================
        # HTML CONTENT ANALYSIS
        # ======================================

        content_type = (
            result["content_type"] or ""
        ).lower()

        if "text/html" in content_type:

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            # Title
            title = soup.title.string if soup.title else None

            if title:
                result["content_analysis"]["title"] = (
                    title.strip()
                )

            # Forms
            forms = soup.find_all("form")

            result["content_analysis"]["forms"] = len(forms)

            # Password fields
            password_fields = soup.find_all(
                "input",
                {
                    "type": re.compile(
                        r"^password$",
                        re.IGNORECASE
                    )
                }
            )

            result["content_analysis"][
                "password_fields"
            ] = len(password_fields)

            # Scripts
            scripts = soup.find_all("script")

            result["content_analysis"]["scripts"] = len(
                scripts
            )

            # IFrames
            iframes = soup.find_all("iframe")

            result["content_analysis"]["iframes"] = len(
                iframes
            )

            # Hidden inputs
            hidden_inputs = soup.find_all(
                "input",
                {
                    "type": re.compile(
                        r"^hidden$",
                        re.IGNORECASE
                    )
                }
            )

            result["content_analysis"][
                "hidden_inputs"
            ] = len(hidden_inputs)

            # External links
            page_host = (
                urlparse(
                    response.url
                ).hostname
            )

            external_links = 0

            for link in soup.find_all("a", href=True):

                href = link.get("href")

                if not href:
                    continue

                parsed_link = urlparse(href)

                if parsed_link.scheme not in (
                    "http",
                    "https"
                ):
                    continue

                link_host = parsed_link.hostname

                if (
                    page_host
                    and link_host
                    and link_host.lower()
                    != page_host.lower()
                ):
                    external_links += 1

            result["content_analysis"][
                "external_links"
            ] = external_links

            # ==================================
            # CONTENT INDICATORS
            # ==================================

            page_text = response.text.lower()

            login_words = [
                "login",
                "sign in",
                "signin",
                "verify your account",
                "enter your password",
                "confirm your password"
            ]

            matched_words = []

            for word in login_words:

                if word in page_text:
                    matched_words.append(word)

            if matched_words:

                result["suspicious_indicators"].append(
                    "Authentication-related content detected"
                )

            # Password form
            if (
                len(password_fields) > 0
                and len(forms) > 0
            ):

                result["suspicious_indicators"].append(
                    "Page contains a password submission form"
                )

            # Iframe presence
            if len(iframes) > 0:

                result["suspicious_indicators"].append(
                    "Page contains iframe elements"
                )

            # ==================================
            # SIMPLE OBFUSCATION SIGNALS
            # ==================================

            suspicious_js_patterns = [
                r"eval\s*\(",
                r"atob\s*\(",
                r"fromcharcode",
                r"document\.write\s*\("
            ]

            matched_js = []

            for pattern in suspicious_js_patterns:

                if re.search(
                    pattern,
                    response.text,
                    re.IGNORECASE
                ):

                    matched_js.append(pattern)

            if matched_js:

                result["suspicious_indicators"].append(
                    "Potentially obfuscated JavaScript pattern detected"
                )

    except requests.exceptions.Timeout:

        result["errors"].append(
            "HTTP request timed out"
        )

    except requests.exceptions.RequestException as exc:

        result["errors"].append(
            f"HTTP analysis failed: {str(exc)}"
        )

    except Exception as exc:

        result["errors"].append(
            f"Unexpected HTTP analysis error: {str(exc)}"
        )

    return result
