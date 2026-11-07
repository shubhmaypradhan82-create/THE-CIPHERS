
import os
import re
from urllib.parse import urlparse

import httpx

from .forensic_service import analyze_single_url
from .ml.detector import analyze_email_text
from .modules.ip_analyzer import analyze_ip

URL_RE = re.compile(r"https?://[^\s<>\"']+")
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
SUSPICIOUS_WORDS = {
    "urgent": 2, "verify your account": 4, "verify your password": 5,
    "account suspended": 5, "click here": 2, "password": 2,
    "bank details": 5, "send your password": 5, "limited time": 2,
    "action required": 2, "invoice": 1, "gift card": 3,
}


def extract_indicators(subject: str, body: str, explicit_url=None):
    text = f"{subject or ''} {body or ''}"
    urls = list(dict.fromkeys(URL_RE.findall(text)))
    if explicit_url:
        urls.append(explicit_url)
    urls = list(dict.fromkeys(urls))
    ips = list(dict.fromkeys(IP_RE.findall(text)))
    return urls, ips


def analyze_locally(subject, body, urls):
    text = f"{subject or ''} {body or ''}".lower()
    score = sum(weight for word, weight in SUSPICIOUS_WORDS.items() if word in text)
    for u in urls:
        try:
            parsed = urlparse(u.strip())
            host = parsed.hostname or ""
        except ValueError:
            host = ""
        if "@" in u or host.count(".") >= 3:
            score += 1
        if host in {"bit.ly", "tinyurl.com"}:
            score += 2
    if score >= 10:
        level = "CRITICAL"
    elif score >= 6:
        level = "HIGH"
    elif score >= 3:
        level = "MEDIUM"
    elif score >= 1:
        level = "LOW"
    else:
        level = "SAFE"
    return level, min(0.99, 0.55 + score * 0.045)


def _summary_from_forensic(results):
    urls = []
    ips = []
    for r in results:
        ud = r.get("url_analysis", {})
        rd = r.get("risk_analysis", {})
        url = ud.get("url")
        if url:
            urls.append({
                "url": url,
                "domain": ud.get("domain"),
                "risk_level": rd.get("risk_level", "unknown"),
                "risk_score": rd.get("risk_score", 0),
                "forensic": r,
            })
        ip = ud.get("ip_address")
        if ip and ip not in {x.get("ip_address") for x in ips}:
            ip_data = r.get("ip_analysis") or {}
            ips.append({
                "ip_address": ip,
                "valid": True,
                "country": ip_data.get("country"),
                "country_code": ip_data.get("country_code"),
                "region": ip_data.get("region"),
                "city": ip_data.get("city"),
                "latitude": ip_data.get("latitude"),
                "longitude": ip_data.get("longitude"),
                "timezone": ip_data.get("timezone"),
                "isp": ip_data.get("isp"),
                "asn": ip_data.get("asn"),
                "reputation": "unknown",
                "forensic": r,
            })
    return {
        "urls": urls,
        "ips": ips,
        "source": "in-process-forensic-engine",
        "forensic_results": results,
    }


async def call_cyber_engine(subject, body, urls, ips):
    engine_url = os.getenv("CYBER_ENGINE_URL")
    engine_key = os.getenv("CYBER_ENGINE_API_KEY")
    if engine_url:
        payload = {"subject": subject, "body": body, "urls": urls, "ips": ips}
        headers = {"Authorization": f"Bearer {engine_key}"} if engine_key else {}
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(engine_url, json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()
        data["source"] = data.get("source", "external-cybersecurity-engine")
        return data

    forensic_results = []
    for url in urls:
        try:
            forensic_results.append(analyze_single_url(url))
        except Exception as exc:
            forensic_results.append({"url_analysis": {"url": url}, "error": str(exc)})
    if forensic_results:
        return _summary_from_forensic(forensic_results)
    direct_ips = []
    for ip in ips:
        try:
            intel = analyze_ip(ip)
        except Exception as exc:
            intel = {"ip_address": ip, "errors": [str(exc)]}
        direct_ips.append({
            "ip_address": ip, "valid": True,
            "country": intel.get("country"), "country_code": intel.get("country_code"),
            "region": intel.get("region"), "city": intel.get("city"),
            "latitude": intel.get("latitude"), "longitude": intel.get("longitude"),
            "timezone": intel.get("timezone"), "isp": intel.get("isp"),
            "asn": intel.get("asn"), "reputation": "unknown",
            "errors": intel.get("errors", []),
        })
    return {"urls": [], "ips": direct_ips, "source": "in-process-forensic-engine"}


def _level_from_score(score: float) -> str:
    if score >= 85:
        return "CRITICAL"
    if score >= 65:
        return "HIGH"
    if score >= 35:
        return "MEDIUM"
    if score >= 15:
        return "LOW"
    return "SAFE"


async def call_ai(subject, body, engine):
    """Run the bundled ML model, then combine it with forensic evidence.

    AI_API_URL remains supported as an optional override. Without it, the
    bundled trained model is used in-process; no second server is required.
    """
    ai_url = os.getenv("AI_API_URL")
    ai_key = os.getenv("AI_API_KEY")
    combined_text = f"Subject: {subject or ''}\n\n{body or ''}".strip()

    if ai_url:
        payload = {"subject": subject, "body": body, "indicators": engine}
        headers = {"Authorization": f"Bearer {ai_key}"} if ai_key else {}
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(ai_url, json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()
        return {
            "prediction": data.get("prediction") or data.get("threat_level", "unknown"),
            "confidence_score": float(data.get("confidence_score", 0.5)),
            "explanation": data.get("explanation", "External AI model response"),
            "provider": "external-ai",
        }

    ml = analyze_email_text(combined_text)
    ml_score = float(ml["spam_probability"])

    forensic_scores = [
        float(u.get("risk_score", 0))
        for u in engine.get("urls", [])
        if isinstance(u, dict)
    ]
    forensic_score = max(forensic_scores, default=0.0)

    # Use the strongest evidence so a high-confidence ML classification is not
    # hidden by a missing/weak URL score, while forensic evidence can escalate risk.
    combined_score = max(ml_score, forensic_score)
    prediction = _level_from_score(combined_score)

    # Confidence is normalized to [0, 1] and reflects the stronger evidence.
    confidence = max(ml_score / 100.0, max(forensic_scores, default=0) / 100.0)
    confidence = min(0.99, max(0.50, confidence))

    explanation = (
        f"Bundled ML model classified the email as {ml['classification']} "
        f"with {ml['spam_probability']:.2f}% spam probability. "
        f"Forensic URL evidence reached {forensic_score:.0f}/100. "
        f"Combined threat level: {prediction}."
    )

    return {
        "prediction": prediction,
        "confidence_score": round(confidence, 4),
        "explanation": explanation,
        "provider": "local-ml+forensics",
        "ml": ml,
        "forensic_score": forensic_score,
        "combined_score": combined_score,
    }
