import base64
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
import app.main as main


def test_auth_and_text_analysis():
    client = TestClient(main.app)
    email = "integration-test@example.com"
    password = "secret123"
    r = client.post("/auth/register", json={"name": "Integration Test", "email": email, "password": password})
    assert r.status_code in (200, 409)
    auth = base64.b64encode(f"{email}:{password}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}
    assert client.get("/auth/me", headers=headers).status_code == 200
    r = client.post("/analyze", headers=headers, json={"subject": "Urgent verify your account", "body": "Please verify your password"})
    assert r.status_code == 200
    assert "prediction" in r.json()


def test_forensic_url_route_and_storage(monkeypatch):
    client = TestClient(main.app)
    email = "forensic-test@example.com"
    password = "secret123"
    client.post("/auth/register", json={"name": "Forensic Test", "email": email, "password": password})
    auth = base64.b64encode(f"{email}:{password}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}
    fake = {"case": {"case_id": "CASE-TEST"}, "url_analysis": {"url": "https://example.com", "domain": "example.com"}, "risk_analysis": {"risk_score": 10, "risk_level": "LOW", "findings": []}, "ioc_analysis": {"summary": {"primary_count": 0, "supporting_count": 0}}, "correlation": {"entity_count": 1, "relationship_count": 1, "findings": []}, "timeline": []}
    monkeypatch.setattr(main, "analyze_single_url", lambda url: fake)
    r = client.post("/forensics/url", headers=headers, json={"url": "https://example.com"})
    assert r.status_code == 200
    assert r.json()["case"]["case_id"] == "CASE-TEST"
    assert client.get("/forensics", headers=headers).status_code == 200


def test_local_ml_route_and_status():
    client = TestClient(main.app)
    email = "ml-test@example.com"
    password = "secret123"
    client.post("/auth/register", json={"name": "ML Test", "email": email, "password": password})
    auth = base64.b64encode(f"{email}:{password}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}
    status = client.get("/ai/status", headers=headers)
    assert status.status_code == 200
    assert status.json()["available"] is True
    r = client.post(
        "/ai/analyze",
        headers=headers,
        json={
            "subject": "Urgent account suspended",
            "body": "Verify your password immediately and click here.",
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["classification"] == "spam"
    assert 0 <= data["spam_probability"] <= 100
