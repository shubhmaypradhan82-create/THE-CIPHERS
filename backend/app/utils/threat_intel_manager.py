import os
import requests


class ThreatIntelProvider:

    name = "base"

    def lookup(self, ioc_type, value):
        raise NotImplementedError


class LocalProvider(ThreatIntelProvider):

    name = "local"

    def lookup(self, ioc_type, value):

        return {
            "provider": self.name,
            "ioc_type": ioc_type,
            "value": value,
            "status": "unknown",
            "malicious": None,
            "confidence": "low",
            "details": "No local threat reputation database configured."
        }


class VirusTotalProvider(ThreatIntelProvider):

    name = "virustotal"

    BASE_URL = "https://www.virustotal.com/api/v3"

    def __init__(self):

        self.api_key = os.getenv(
            "VIRUSTOTAL_API_KEY"
        )

        self.timeout = float(os.getenv("FORENSIC_INTEL_TIMEOUT", "5"))

    def lookup(self, ioc_type, value):

        if not self.api_key:

            return {
                "provider": self.name,
                "ioc_type": ioc_type,
                "value": value,
                "status": "not_configured",
                "malicious": None,
                "confidence": "none",
                "details": "VIRUSTOTAL_API_KEY is not configured."
            }

        endpoint = None

        if ioc_type == "domain":

            endpoint = (
                f"{self.BASE_URL}/domains/{value}"
            )

        elif ioc_type == "ipv4":

            endpoint = (
                f"{self.BASE_URL}/ip_addresses/{value}"
            )

        elif ioc_type == "url":

            return self.lookup_url(
                value
            )

        else:

            return {
                "provider": self.name,
                "ioc_type": ioc_type,
                "value": value,
                "status": "unsupported",
                "malicious": None,
                "confidence": "none",
                "details": "IOC type is not supported by this adapter."
            }

        headers = {
            "x-apikey": self.api_key,
            "Accept": "application/json"
        }

        try:

            response = requests.get(
                endpoint,
                headers=headers,
                timeout=self.timeout
            )

            if response.status_code == 404:

                return {
                    "provider": self.name,
                    "ioc_type": ioc_type,
                    "value": value,
                    "status": "not_found",
                    "malicious": None,
                    "confidence": "none",
                    "details": "IOC was not found in VirusTotal."
                }

            if response.status_code == 401:

                return {
                    "provider": self.name,
                    "ioc_type": ioc_type,
                    "value": value,
                    "status": "authentication_error",
                    "malicious": None,
                    "confidence": "none",
                    "details": "VirusTotal API key was rejected."
                }

            if response.status_code == 429:

                return {
                    "provider": self.name,
                    "ioc_type": ioc_type,
                    "value": value,
                    "status": "rate_limited",
                    "malicious": None,
                    "confidence": "none",
                    "details": "VirusTotal rate limit reached."
                }

            response.raise_for_status()

            payload = response.json()

            return self.parse_report(
                ioc_type,
                value,
                payload
            )

        except requests.exceptions.Timeout:

            return {
                "provider": self.name,
                "ioc_type": ioc_type,
                "value": value,
                "status": "timeout",
                "malicious": None,
                "confidence": "none",
                "details": "VirusTotal request timed out."
            }

        except requests.exceptions.RequestException as exc:

            return {
                "provider": self.name,
                "ioc_type": ioc_type,
                "value": value,
                "status": "error",
                "malicious": None,
                "confidence": "none",
                "details": str(exc)
            }

    def lookup_url(self, value):

        # VirusTotal URL objects use a URL-safe identifier.
        import base64

        url_id = (
            base64.urlsafe_b64encode(
                value.encode()
            )
            .decode()
            .rstrip("=")
        )

        endpoint = (
            f"{self.BASE_URL}/urls/{url_id}"
        )

        headers = {
            "x-apikey": self.api_key,
            "Accept": "application/json"
        }

        try:

            response = requests.get(
                endpoint,
                headers=headers,
                timeout=self.timeout
            )

            if response.status_code == 404:

                return {
                    "provider": self.name,
                    "ioc_type": "url",
                    "value": value,
                    "status": "not_found",
                    "malicious": None,
                    "confidence": "none",
                    "details": "URL was not found in VirusTotal."
                }

            if response.status_code == 401:

                return {
                    "provider": self.name,
                    "ioc_type": "url",
                    "value": value,
                    "status": "authentication_error",
                    "malicious": None,
                    "confidence": "none",
                    "details": "VirusTotal API key was rejected."
                }

            if response.status_code == 429:

                return {
                    "provider": self.name,
                    "ioc_type": "url",
                    "value": value,
                    "status": "rate_limited",
                    "malicious": None,
                    "confidence": "none",
                    "details": "VirusTotal rate limit reached."
                }

            response.raise_for_status()

            payload = response.json()

            return self.parse_report(
                "url",
                value,
                payload
            )

        except requests.exceptions.Timeout:

            return {
                "provider": self.name,
                "ioc_type": "url",
                "value": value,
                "status": "timeout",
                "malicious": None,
                "confidence": "none",
                "details": "VirusTotal request timed out."
            }

        except requests.exceptions.RequestException as exc:

            return {
                "provider": self.name,
                "ioc_type": "url",
                "value": value,
                "status": "error",
                "malicious": None,
                "confidence": "none",
                "details": str(exc)
            }

    def parse_report(
        self,
        ioc_type,
        value,
        payload
    ):

        data = payload.get(
            "data",
            {}
        )

        attributes = data.get(
            "attributes",
            {}
        )

        reputation = attributes.get(
            "reputation"
        )

        last_analysis_stats = attributes.get(
            "last_analysis_stats",
            {}
        )

        malicious_count = int(
            last_analysis_stats.get(
                "malicious",
                0
            ) or 0
        )

        suspicious_count = int(
            last_analysis_stats.get(
                "suspicious",
                0
            ) or 0
        )

        harmless_count = int(
            last_analysis_stats.get(
                "harmless",
                0
            ) or 0
        )

        undetected_count = int(
            last_analysis_stats.get(
                "undetected",
                0
            ) or 0
        )

        total_engines = (
            malicious_count
            + suspicious_count
            + harmless_count
            + undetected_count
        )

        malicious = None
        confidence = "medium"

        if malicious_count > 0:

            malicious = True

            if malicious_count >= 3:
                confidence = "high"

        elif (
            total_engines > 0
            and malicious_count == 0
            and suspicious_count == 0
        ):

            malicious = False
            confidence = "medium"

        return {
            "provider": self.name,
            "ioc_type": ioc_type,
            "value": value,
            "status": "success",
            "malicious": malicious,
            "confidence": confidence,
            "details": {
                "reputation": reputation,
                "malicious_detections":
                    malicious_count,
                "suspicious_detections":
                    suspicious_count,
                "harmless_detections":
                    harmless_count,
                "undetected":
                    undetected_count
            }
        }


class ThreatIntelManager:

    def __init__(self):

        self.providers = [
            LocalProvider(),
            VirusTotalProvider()
        ]

    def lookup(self, ioc_type, value):

        results = []

        for provider in self.providers:

            try:

                results.append(
                    provider.lookup(
                        ioc_type,
                        value
                    )
                )

            except Exception as exc:

                results.append({
                    "provider":
                        getattr(
                            provider,
                            "name",
                            "unknown"
                        ),
                    "ioc_type":
                        ioc_type,
                    "value":
                        value,
                    "status":
                        "error",
                    "malicious":
                        None,
                    "confidence":
                        "none",
                    "details":
                        str(exc)
                })

        return results

    def enrich(self, ioc_data=None):

        ioc_data = ioc_data or {}

        output = []

        all_iocs = (
            ioc_data.get(
                "primary_iocs",
                []
            )
            + ioc_data.get(
                "supporting_iocs",
                []
            )
        )

        seen = set()

        for item in all_iocs:

            ioc_type = item.get("type")
            value = item.get("value")

            if not ioc_type or not value:
                continue

            key = (
                ioc_type,
                value
            )

            if key in seen:
                continue

            seen.add(key)

            output.append({
                "ioc": {
                    "type": ioc_type,
                    "value": value
                },
                "provider_results":
                    self.lookup(
                        ioc_type,
                        value
                    )
            })

        return {
            "enabled": True,
            "ioc_results": output,
            "summary": {
                "ioc_count":
                    len(output),
                "providers": [
                    provider.name
                    for provider in self.providers
                ]
            }
        }
