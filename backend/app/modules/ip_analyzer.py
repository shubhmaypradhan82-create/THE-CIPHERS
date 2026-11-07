import ipaddress
import os
import socket
import requests

try:
    from ipwhois import IPWhois
except ImportError:
    IPWhois = None


def _is_public_ip(value: str) -> bool:
    try:
        ip = ipaddress.ip_address(value)
        return ip.is_global
    except ValueError:
        return False


def _geo_lookup(ip_address: str):
    # Two lightweight public-IP providers are used as fallbacks. Results are
    # approximate and should be treated as network/ISP location, not a person's
    # physical location.
    for url, parser in [
        (f"https://ipwho.is/{ip_address}", lambda d: {
            "country": d.get("country"), "country_code": d.get("country_code"),
            "region": d.get("region"), "city": d.get("city"),
            "latitude": d.get("latitude"), "longitude": d.get("longitude"),
            "timezone": (d.get("timezone") or {}).get("id") if isinstance(d.get("timezone"), dict) else d.get("timezone"),
            "isp": (d.get("connection") or {}).get("isp") if isinstance(d.get("connection"), dict) else None,
        }),
        (f"http://ip-api.com/json/{ip_address}?fields=status,message,country,countryCode,regionName,city,lat,lon,timezone,isp", lambda d: {
            "country": d.get("country"), "country_code": d.get("countryCode"),
            "region": d.get("regionName"), "city": d.get("city"),
            "latitude": d.get("lat"), "longitude": d.get("lon"),
            "timezone": d.get("timezone"), "isp": d.get("isp"),
        }),
    ]:
        try:
            data = requests.get(url, timeout=5).json()
            if data.get("success", True) is False or data.get("status") == "fail":
                continue
            parsed = parser(data)
            if parsed.get("country") or parsed.get("city") or parsed.get("latitude") is not None:
                return parsed
        except Exception:
            continue
    return {}


def analyze_ip(ip_address):
    result = {
        "ip_address": ip_address, "reverse_dns": None, "asn": None,
        "asn_description": None, "network": None, "country": None,
        "country_code": None, "region": None, "city": None,
        "latitude": None, "longitude": None, "timezone": None, "isp": None,
        "errors": []
    }

    if not _is_public_ip(ip_address):
        result["errors"].append("Private, loopback, reserved, or invalid IP; public geolocation is unavailable.")
        return result

    try:
        result.update(_geo_lookup(ip_address))
        if not any(result.get(k) for k in ("country", "city", "latitude", "longitude")):
            result["errors"].append("Geolocation lookup returned no location data.")
    except Exception as e:
        result["errors"].append(f"Geolocation lookup failed: {e}")

    try:
        result["reverse_dns"] = socket.gethostbyaddr(ip_address)[0]
    except Exception as e:
        result["errors"].append(f"Reverse DNS lookup failed: {e}")

    try:
        if os.getenv("FORENSIC_IP_INTEL", "false").lower() not in {"1", "true", "yes"}:
            raise RuntimeError("live IP intelligence disabled; set FORENSIC_IP_INTEL=true to enable RDAP")
        if IPWhois is None:
            raise RuntimeError("ipwhois package is not installed; install backend requirements")
        data = IPWhois(ip_address).lookup_rdap(depth=1)
        result["asn"] = data.get("asn")
        result["asn_description"] = data.get("asn_description")
        result["network"] = data.get("network", {}).get("name")
        # RDAP country is a useful fallback when the geolocation provider has no country.
        if not result.get("country"):
            result["country"] = data.get("network", {}).get("country")
    except Exception as e:
        result["errors"].append(f"IP intelligence lookup failed: {e}")

    return result
