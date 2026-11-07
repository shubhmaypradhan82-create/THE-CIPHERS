import json
from typing import Any, Dict, List

from app.modules.email_analyzer import analyze_email
from app.modules.url_analyzer import analyze_url
from app.modules.dns_analyzer import analyze_dns
from app.modules.ip_analyzer import analyze_ip
from app.modules.redirect_analyzer import analyze_redirects
from app.modules.http_analyzer import analyze_http
from app.modules.tls_analyzer import analyze_tls
from app.modules.ioc_analyzer import extract_iocs
from app.modules.email_correlation import correlate_email_with_urls
from app.utils.risk_engine import calculate_email_risk, calculate_combined_url_risk
from app.utils.case_manager import generate_case_id, build_case_summary
from app.utils.timeline_manager import build_url_timeline
from app.utils.threat_intel import enrich_iocs
from app.utils.email_infrastructure import correlate_email_infrastructure
from app.utils.case_risk_engine import calculate_case_risk
from app.utils.report_generator import generate_forensic_report
from app.modules.ioc_analyzer import extract_iocs
from .correlation.correlation_engine import CorrelationEngine
from .ml.detector import analyze_email_text


def _safe(fn, default=None, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as exc:
        return default if default is not None else {"error": str(exc)}


def analyze_single_url(url: str) -> Dict[str, Any]:
    """Run the original forensic URL pipeline in-process and return its full evidence graph."""
    url_data = analyze_url(url)
    domain = url_data.get("domain")
    ip_address = url_data.get("ip_address")

    dns_data = _safe(analyze_dns, {}, domain) if domain else None
    ip_data = _safe(analyze_ip, {}, ip_address) if ip_address else None
    redirect_data = _safe(analyze_redirects, {}, url)
    http_data = _safe(analyze_http, {}, url)
    tls_data = _safe(analyze_tls, {}, url)

    combined_evidence = {
        "url": url_data,
        "dns": dns_data,
        "ip": ip_data,
        "redirects": redirect_data,
        "http": http_data,
        "tls": tls_data,
    }
    ioc_data = _safe(extract_iocs, {}, combined_evidence)
    threat_intel_data = _safe(enrich_iocs, {}, ioc_data)

    correlation_data = _safe(
        lambda: CorrelationEngine().correlate(
            url_data=url_data,
            dns_data=dns_data,
            ip_data=ip_data,
            tls_data=tls_data,
        ),
        {},
    )
    risk_data = _safe(
        calculate_combined_url_risk,
        {"risk_score": 0, "risk_level": "LOW", "findings": []},
        url_data=url_data,
        redirect_data=redirect_data,
        http_data=http_data,
        tls_data=tls_data,
        ioc_data=ioc_data,
        correlation_data=correlation_data,
        threat_intel_data=threat_intel_data,
    )
    timeline = _safe(
        build_url_timeline,
        [],
        url=url,
        url_data=url_data,
        dns_data=dns_data,
        ip_data=ip_data,
        redirect_data=redirect_data,
        http_data=http_data,
        ioc_data=ioc_data,
        correlation_data=correlation_data,
        risk_data=risk_data,
    )
    case_id = generate_case_id(url)
    case = build_case_summary(
        case_id=case_id,
        investigation_type="url",
        target=url,
        risk_data=risk_data,
        ioc_data=ioc_data,
        correlation_data=correlation_data,
    )
    return {
        "case": case,
        "url_analysis": url_data,
        "risk_analysis": risk_data,
        "dns_analysis": dns_data,
        "ip_analysis": ip_data,
        "redirect_analysis": redirect_data,
        "http_analysis": http_data,
        "tls_analysis": tls_data,
        "ioc_analysis": ioc_data,
        "threat_intelligence": threat_intel_data,
        "correlation": correlation_data,
        "timeline": timeline,
    }


def analyze_email_file(path: str) -> Dict[str, Any]:
    """Run the original complete email->URL->correlation->case->report pipeline."""
    email_data = analyze_email(path)
    # Run the bundled trained ML model on the complete parsed email
    # (headers + body) so uploaded .eml files use the same AI layer as /analyze.
    ml_text = "\n".join([
        f"From: {email_data.get('from') or ''}",
        f"To: {email_data.get('to') or ''}",
        f"Reply-To: {email_data.get('reply_to') or ''}",
        f"Return-Path: {email_data.get('return_path') or ''}",
        f"Subject: {email_data.get('subject') or ''}",
        f"Authentication: {email_data.get('authentication') or ''}",
        f"Body:\n{email_data.get('body') or ''}",
    ])
    ml_analysis = analyze_email_text(ml_text)
    email_data["ml_analysis"] = ml_analysis
    email_risk = calculate_email_risk(email_data)
    email_iocs = extract_iocs(email_data)
    email_threat_intel = enrich_iocs(email_iocs)
    email_urls = list(dict.fromkeys(
        u.strip() for u in email_iocs.get("urls", [])
        if isinstance(u, str) and u.strip()
    ))
    analyzed_urls = []
    for url in email_urls:
        try:
            analyzed_urls.append(analyze_single_url(url))
        except Exception as exc:
            analyzed_urls.append({"url_analysis": {"url": url}, "error": str(exc)})

    email_correlation = correlate_email_with_urls(
        email_data=email_data, url_analyses=analyzed_urls
    )
    email_infrastructure = correlate_email_infrastructure(
        email_data=email_data, analyzed_urls=analyzed_urls
    )
    case_risk = calculate_case_risk(
        email_risk=email_risk,
        url_results=analyzed_urls,
        email_correlation=email_correlation,
        email_infrastructure=email_infrastructure,
    )
    case_id = generate_case_id(
        email_data.get("message_id") or email_data.get("subject") or email_data.get("from")
    )
    total_entities = sum(x.get("correlation", {}).get("entity_count", 0) for x in analyzed_urls)
    total_relationships = sum(x.get("correlation", {}).get("relationship_count", 0) for x in analyzed_urls)
    total_findings = sum(len(x.get("correlation", {}).get("findings", [])) for x in analyzed_urls)
    case_summary = build_case_summary(
        case_id=case_id,
        investigation_type="email",
        target=email_data.get("message_id") or email_data.get("subject") or "email",
        risk_data=email_risk,
        ioc_data=email_iocs,
        correlation_data={
            "entity_count": total_entities,
            "relationship_count": total_relationships,
            "findings": [{} for _ in range(total_findings)],
        },
        email_correlation=email_correlation,
    )
    # The original engine had a sequencing bug: it generated the report before case_summary existed.
    # Build the report only after the case is complete.
    timeline = []
    for item in analyzed_urls:
        timeline.extend(item.get("timeline", []))
    report = generate_forensic_report(
        case=case_summary,
        email_evidence=email_data,
        email_risk=email_risk,
        case_risk=case_risk,
        email_correlation=email_correlation,
        email_infrastructure=email_infrastructure,
        analyzed_urls=analyzed_urls,
        ioc_analysis=email_iocs,
        timeline=timeline,
    )
    url_risk_summary = []
    for item in analyzed_urls:
        ud, rd = item.get("url_analysis", {}), item.get("risk_analysis", {})
        url_risk_summary.append({
            "url": ud.get("url"), "domain": ud.get("domain"),
            "risk_score": rd.get("risk_score", 0), "risk_level": rd.get("risk_level", "LOW")
        })
    return {
        "case": case_summary,
        "email_evidence": email_data,
        "risk_analysis": email_risk,
        "case_risk": case_risk,
        "report": report,
        "ioc_analysis": email_iocs,
        "threat_intelligence": email_threat_intel,
        "email_url_correlation": email_correlation,
        "email_infrastructure": email_infrastructure,
        "analyzed_urls": analyzed_urls,
        "url_risk_summary": url_risk_summary,
        "ai": {
            "prediction": (
                "HIGH" if ml_analysis["classification"] == "spam"
                and ml_analysis["spam_probability"] >= 80 else
                "MEDIUM" if ml_analysis["classification"] == "spam"
                and ml_analysis["spam_probability"] >= 50 else
                "LOW" if ml_analysis["classification"] == "spam" else "SAFE"
            ),
            "confidence_score": max(
                ml_analysis["spam_probability"],
                ml_analysis["ham_probability"],
            ) / 100.0,
            "explanation": (
                f"Bundled ML model classified this email as "
                f"{ml_analysis['classification']} with "
                f"{ml_analysis['spam_probability']:.2f}% spam probability."
            ),
            "provider": "local-ml",
            "ml": ml_analysis,
        },
    }


def json_dumps(value: Any) -> str:
    return json.dumps(value, default=str, ensure_ascii=False)
