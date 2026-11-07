import json
import os
import tempfile
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import inspect, text
from .database import Base, engine, get_db
from . import models, schemas
from .security import hash_password, verify_password, get_current_user, authenticate_user, require_admin
from .engine import extract_indicators, call_cyber_engine, call_ai
from .ml.detector import model_status, analyze_email_text
from .forensic_service import analyze_single_url, analyze_email_file, json_dumps
from .modules.ip_analyzer import analyze_ip

Base.metadata.create_all(bind=engine)
app=FastAPI(title="AI-Powered Email Threat Detection & Forensic Intelligence API", version="4.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173","http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def client_ip(request: Request) -> str:
    # By default use the direct peer address. Do not trust forwarded headers unless
    # the deployment explicitly places CHIPERS behind a trusted proxy.
    return request.client.host if request.client else "unknown"

def audit(db: Session, user, request: Request, action: str, details: str = "", observed_ip: str | None = None):
    # In local development request.client.host is usually 127.0.0.1. When the
    # browser can determine its public IP, keep that as supplemental login
    # evidence so the admin console can provide approximate network location.
    ip = (observed_ip or "").strip() if observed_ip else ""
    if not ip:
        ip = client_ip(request)
    db.add(models.AuditLog(user_id=getattr(user, "id", None), action=action, ip_address=ip, user_agent=request.headers.get("user-agent", "")[:500], details=details[:2000] if details else None))

DEFAULT_ADMIN_EMAIL = "admin@chipers.in"
DEFAULT_ADMIN_PASSWORD = "CHIPERS@Admin2026!"

def ensure_schema():
    inspector = inspect(engine)
    columns = {c["name"] for c in inspector.get_columns("users")} if "users" in inspector.get_table_names() else set()
    if "is_active" not in columns:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN is_active INTEGER NOT NULL DEFAULT 1"))

def ensure_admin():
    email=os.getenv("ADMIN_EMAIL", DEFAULT_ADMIN_EMAIL).strip().lower()
    password=os.getenv("ADMIN_PASSWORD", DEFAULT_ADMIN_PASSWORD)
    if not email or not password:
        return
    db=get_db().__next__()
    try:
        user=db.query(models.User).filter(models.User.email==email).first()
        if not user:
            user=models.User(name=os.getenv("ADMIN_NAME", "CHIPERS Administrator"), email=email, password_hash=hash_password(password), role="admin")
            db.add(user)
        else:
            user.role="admin"
            # Keep the configured/preset administrator credential authoritative.
            user.password_hash=hash_password(password)
            user.is_active=1
        db.commit()
    finally:
        db.close()

ensure_schema()
ensure_admin()

@app.get("/")
def root(): return {"message":"Backend is running","docs":"/docs","forensic_engine":"in-process"}
@app.get("/health")
def health():
    return {
        "status": "ok",
        "forensic_engine": "ready",
        "local_ml": model_status(),
    }

@app.get("/ai/status")
def ai_status(user=Depends(get_current_user)):
    return model_status()

@app.post("/ai/analyze")
def ai_analyze(req: schemas.AnalyzeRequest, user=Depends(get_current_user)):
    text = "\n".join([
        f"From: {req.sender or ''}",
        f"To: {req.recipient or ''}",
        f"Subject: {req.subject or ''}",
        f"Body:\n{req.body or ''}",
    ]).strip()
    try:
        return analyze_email_text(text)
    except (TypeError, ValueError, FileNotFoundError, RuntimeError) as exc:
        raise HTTPException(422, str(exc)) from exc

@app.post("/auth/register", response_model=schemas.UserResponse)
def register(req: schemas.RegisterRequest, request: Request, db: Session=Depends(get_db)):
    email=req.email.lower()
    if db.query(models.User).filter(models.User.email==email).first():
        raise HTTPException(409,"User already exists")
    user=models.User(name=req.name, email=email, password_hash=hash_password(req.password), role="analyst")
    db.add(user); db.flush()
    audit(db, user, request, "register", "Analyst account created")
    db.commit(); db.refresh(user); return user

@app.post("/auth/login", response_model=schemas.UserResponse)
def login(req: schemas.LoginRequest, request: Request, db: Session=Depends(get_db)):
    user=authenticate_user(
        type("Creds", (), {"username": req.email, "password": req.password})(), db
    )
    if user.role == "admin":
        raise HTTPException(status_code=403, detail="Administrators must use the separate Admin login")
    audit(db, user, request, "login", "User login", req.client_ip)
    db.commit()
    return user

@app.post("/auth/admin-login", response_model=schemas.UserResponse)
def admin_login(req: schemas.LoginRequest, request: Request, db: Session=Depends(get_db)):
    configured_email=os.getenv("ADMIN_EMAIL", DEFAULT_ADMIN_EMAIL).strip().lower()
    configured_password=os.getenv("ADMIN_PASSWORD", DEFAULT_ADMIN_PASSWORD)
    if not configured_email or not configured_password or req.email.lower()!=configured_email or not hmac_compare(req.password, configured_password):
        raise HTTPException(status_code=401, detail="Invalid administrator credentials", headers={"WWW-Authenticate":"Basic"})
    user=db.query(models.User).filter(models.User.email==configured_email).first()
    if not user:
        user=models.User(name=os.getenv("ADMIN_NAME", "CHIPERS Administrator"),email=configured_email,password_hash=hash_password(configured_password),role="admin")
        db.add(user); db.flush()
    user.role="admin"
    user.is_active=1
    user.password_hash=hash_password(configured_password)
    audit(db,user,request,"admin_login","Administrator login", req.client_ip)
    db.commit(); db.refresh(user); return user

def hmac_compare(a: str, b: str) -> bool:
    import hmac
    return hmac.compare_digest(a.encode(), b.encode())

@app.get("/auth/me", response_model=schemas.UserResponse)
def me(user=Depends(get_current_user)): return user

@app.put("/auth/me", response_model=schemas.UserResponse)
def update_me(req: schemas.ProfileUpdate, db: Session=Depends(get_db), user=Depends(get_current_user)):
    user.name=req.name.strip()
    db.commit(); db.refresh(user)
    return user

@app.post("/auth/change-password")
def change_password(req: schemas.ChangePasswordRequest, request: Request, db: Session=Depends(get_db), user=Depends(get_current_user)):
    if not verify_password(req.current_password, user.password_hash or ""):
        raise HTTPException(400, "Current password is incorrect")
    if req.new_password == req.current_password:
        raise HTTPException(400, "New password must be different")
    user.password_hash = hash_password(req.new_password)
    audit(db, user, request, "password_change", "User changed password")
    db.commit()
    return {"message": "Password changed successfully"}

@app.post("/investigations", response_model=schemas.InvestigationResponse)
def create_investigation(req: schemas.InvestigationCreate, db: Session=Depends(get_db), user=Depends(get_current_user)):
    owner_id=req.user_id or user.id
    if owner_id != user.id and user.role != "admin": raise HTTPException(403,"You can only create investigations for yourself")
    item=models.Investigation(title=req.title,description=req.description,user_id=owner_id,status="open")
    db.add(item); db.commit(); db.refresh(item); return item

@app.get("/investigations", response_model=list[schemas.InvestigationResponse])
def investigations(db: Session=Depends(get_db), user=Depends(get_current_user)):
    q=db.query(models.Investigation)
    return q.filter(models.Investigation.user_id==user.id).all() if user.role!="admin" else q.all()

@app.patch("/investigations/{investigation_id}", response_model=schemas.InvestigationResponse)
def update_investigation(investigation_id:int, req: schemas.InvestigationUpdate, db: Session=Depends(get_db), user=Depends(get_current_user)):
    item=db.query(models.Investigation).filter(models.Investigation.id==investigation_id).first()
    if not item: raise HTTPException(404,"Investigation not found")
    if user.role!="admin" and item.user_id!=user.id: raise HTTPException(403,"Investigation access denied")
    if req.title is not None: item.title=req.title
    if req.description is not None: item.description=req.description
    if req.status is not None: item.status=req.status
    db.commit(); db.refresh(item); return item

@app.get("/dashboard/summary")
def dashboard_summary(db: Session=Depends(get_db), user=Depends(get_current_user)):
    emails_q=db.query(models.Email)
    inv_q=db.query(models.Investigation)
    fa_q=db.query(models.ForensicAnalysis)
    if user.role!="admin":
        inv_q=inv_q.filter(models.Investigation.user_id==user.id)
        emails_q=emails_q.outerjoin(models.Investigation).filter((models.Email.investigation_id==None)|(models.Investigation.user_id==user.id))
        fa_q=fa_q.outerjoin(models.Investigation).filter((models.ForensicAnalysis.investigation_id==None)|(models.Investigation.user_id==user.id))
    emails=emails_q.order_by(models.Email.id.desc()).limit(100).all()
    levels=[str(e.threat_level or '').upper() for e in emails]
    return {"total_emails":len(emails),"high_critical":sum(x in {"HIGH","CRITICAL"} for x in levels),"active_investigations":inv_q.filter(models.Investigation.status=="open").count(),"forensic_cases":fa_q.count(),"recent_emails":[{"id":e.id,"sender":e.sender,"subject":e.subject,"threat_level":e.threat_level,"created_at":e.created_at} for e in emails[:20]]}

@app.get("/threats")
def threats(q:str="", level:str="", db: Session=Depends(get_db), user=Depends(get_current_user)):
    query=db.query(models.Email)
    if user.role!="admin": query=query.outerjoin(models.Investigation).filter((models.Email.investigation_id==None)|(models.Investigation.user_id==user.id))
    if level: query=query.filter(models.Email.threat_level.ilike(level))
    if q:
        like=f"%{q}%"
        query=query.filter((models.Email.sender.ilike(like))|(models.Email.recipient.ilike(like))|(models.Email.subject.ilike(like))|(models.Email.body.ilike(like))|(models.Email.threat_level.ilike(like)))
    return [{"id":e.id,"sender":e.sender,"recipient":e.recipient,"subject":e.subject,"threat_level":e.threat_level,"investigation_id":e.investigation_id,"created_at":e.created_at} for e in query.order_by(models.Email.id.desc()).limit(200).all()]

@app.get("/geolocation")
def geolocation(db: Session=Depends(get_db), user=Depends(get_current_user)):
    query=db.query(models.IPAddress).join(models.Email,isouter=True)
    if user.role!="admin":
        query=query.outerjoin(models.Investigation,models.Email.investigation_id==models.Investigation.id).filter((models.Email.investigation_id==None)|(models.Investigation.user_id==user.id))
    rows=query.order_by(models.IPAddress.id.desc()).limit(500).all()

    # Enrich stored IP rows with the richer IP/URL evidence already produced by the forensic engine.
    forensic_by_email={}
    fa_query=db.query(models.ForensicAnalysis)
    if user.role!="admin":
        fa_query=fa_query.outerjoin(models.Investigation).filter((models.ForensicAnalysis.investigation_id==None)|(models.Investigation.user_id==user.id))
    for fa in fa_query.order_by(models.ForensicAnalysis.id.desc()).limit(500).all():
        if not fa.email_id: continue
        try: data=json.loads(fa.result_json)
        except Exception: continue
        forensic_by_email.setdefault(fa.email_id,[]).append(data)

    enriched=[]
    for r in rows:
        item={"ip_address":r.ip_address,"country":r.country,"city":r.city,"reputation":r.reputation,"count":1,"email_ids":[r.email_id] if r.email_id else [],"source_urls":[],"reverse_dns":None,"asn":None,"asn_description":None,"network":None,"region":None,"last_seen":r.created_at}
        for fr in forensic_by_email.get(r.email_id,[]):
            ipd=fr.get("ip_analysis") or {}
            if ipd.get("ip_address") and ipd.get("ip_address") != r.ip_address: continue
            item["country"] = item["country"] or ipd.get("country")
            item["reverse_dns"] = item["reverse_dns"] or ipd.get("reverse_dns")
            item["asn"] = item["asn"] or ipd.get("asn")
            item["asn_description"] = item["asn_description"] or ipd.get("asn_description")
            item["network"] = item["network"] or ipd.get("network")
            target=(fr.get("case") or {}).get("target") or (fr.get("url_analysis") or {}).get("url")
            if target and target not in item["source_urls"]: item["source_urls"].append(target)
            created=(fr.get("case") or {}).get("created_at")
            if created: item["last_seen"]=created
        enriched.append(item)

    from collections import Counter
    countries=Counter((r["country"] or "Unknown") for r in enriched)
    cities=Counter((r["city"] or "Unknown") for r in enriched)
    return {"ips":enriched,"countries":[{"country":k,"count":v} for k,v in countries.most_common()],"cities":[{"city":k,"count":v} for k,v in cities.most_common()]}

def _extract_pasted_email_headers(text: str):
    """Best-effort extraction of common RFC email headers from pasted text."""
    import re
    def get(name):
        m = re.search(rf"^\s*{re.escape(name)}\s*:\s*(.+)$", text or "", re.IGNORECASE | re.MULTILINE)
        return m.group(1).strip() if m else ""
    return get("From"), get("To"), get("Subject")

@app.post("/analyze", response_model=schemas.AnalyzeResponse)
async def analyze(req: schemas.AnalyzeRequest, db: Session=Depends(get_db), user=Depends(get_current_user)):
    if not req.sender and not req.url and not req.body and not req.subject: raise HTTPException(400,"Provide an email or URL to analyze")
    pasted_from, pasted_to, pasted_subject = _extract_pasted_email_headers(req.body)
    sender = req.sender.strip() or pasted_from or "unknown"
    recipient = req.recipient.strip() or pasted_to or "unknown"
    subject = req.subject.strip() or pasted_subject or "Threat analysis"
    urls, ips=extract_indicators(subject,req.body,req.url)
    cyber=await call_cyber_engine(subject,req.body,urls,ips)
    ai=await call_ai(subject,req.body,cyber)
    email=models.Email(sender=sender,recipient=recipient,subject=subject,body=req.body,threat_level=ai["prediction"],investigation_id=req.investigation_id)
    db.add(email); db.flush()
    for u in cyber.get("urls",[]):
        row=models.URL(email_id=email.id,url=u.get("url","") or "",risk_level=str(u.get("risk_level","unknown"))); db.add(row); db.flush()
        if u.get("domain"): db.add(models.Domain(url_id=row.id,domain_name=u["domain"],reputation=str(u.get("risk_level","unknown"))))
    for ip in cyber.get("ips",[]): db.add(models.IPAddress(email_id=email.id,ip_address=ip.get("ip_address",""),country=ip.get("country"),city=ip.get("city"),reputation=ip.get("reputation")))
    db.add(models.AIResult(email_id=email.id,prediction=ai["prediction"],confidence_score=ai["confidence_score"],explanation=ai["explanation"]))
    forensic_results=cyber.get("forensic_results",[])
    for fr in forensic_results:
        case_id=(fr.get("case") or {}).get("case_id") or "CASE-UNKNOWN"
        db.add(models.ForensicAnalysis(email_id=email.id,investigation_id=req.investigation_id,case_id=case_id,analysis_type="url",result_json=json_dumps(fr)))
    db.commit(); db.refresh(email)
    return schemas.AnalyzeResponse(email_id=email.id,threat_level=ai["prediction"],confidence_score=ai["confidence_score"],prediction=ai["prediction"],explanation=ai["explanation"],urls=cyber.get("urls",[]),ips=cyber.get("ips",[]),cybersecurity_engine=cyber,ai=ai)

@app.post("/forensics/url")
def forensic_url(req: schemas.ForensicURLRequest, db: Session=Depends(get_db), user=Depends(get_current_user)):
    try: result=analyze_single_url(req.url.strip())
    except Exception as exc: raise HTTPException(422,f"Forensic URL analysis failed: {exc}")
    if req.investigation_id:
        inv=db.query(models.Investigation).filter(models.Investigation.id==req.investigation_id).first()
        if not inv or (inv.user_id!=user.id and user.role!="admin"): raise HTTPException(403,"Investigation access denied")
    db.add(models.ForensicAnalysis(investigation_id=req.investigation_id,case_id=result["case"]["case_id"],analysis_type="url",result_json=json_dumps(result)))
    db.commit(); return result

@app.post("/forensics/email")
async def forensic_email(request: Request, db: Session=Depends(get_db), user=Depends(get_current_user)):
    try:
        form = await request.form()
    except Exception as exc:
        raise HTTPException(400, "Multipart form upload could not be parsed. Install python-multipart.") from exc
    file = form.get("file")
    investigation_raw = form.get("investigation_id")
    try:
        investigation_id = int(investigation_raw) if investigation_raw not in (None, "") else None
    except (TypeError, ValueError):
        raise HTTPException(400, "investigation_id must be an integer")
    if file is None or not hasattr(file, "filename"):
        raise HTTPException(400, "No email file uploaded")
    filename = str(file.filename or "")
    if not filename.lower().endswith(".eml"):
        raise HTTPException(400, "Upload an .eml email file")
    if investigation_id:
        inv=db.query(models.Investigation).filter(models.Investigation.id==investigation_id).first()
        if not inv or (inv.user_id!=user.id and user.role!="admin"): raise HTTPException(403,"Investigation access denied")
    content=await file.read()
    if len(content)>10*1024*1024: raise HTTPException(413,"Email file is too large (max 10 MB)")
    with tempfile.NamedTemporaryFile(delete=False,suffix=".eml") as tmp:
        tmp.write(content); path=tmp.name
    try: result=analyze_email_file(path)
    except Exception as exc: raise HTTPException(422,f"Forensic email analysis failed: {exc}")
    finally:
        try: os.unlink(path)
        except OSError: pass
    db.add(models.ForensicAnalysis(investigation_id=investigation_id,case_id=result["case"]["case_id"],analysis_type="email",result_json=json_dumps(result)))
    db.commit(); return result

@app.get("/forensics", response_model=list[schemas.ForensicAnalysisResponse])
def forensic_history(q:str="", db: Session=Depends(get_db), user=Depends(get_current_user)):
    query=db.query(models.ForensicAnalysis).order_by(models.ForensicAnalysis.id.desc())
    if user.role!="admin":
        query=query.filter(
            (models.ForensicAnalysis.investigation_id==None) |
            (models.ForensicAnalysis.investigation_id.in_(
                db.query(models.Investigation.id).filter(models.Investigation.user_id==user.id)
            ))
        )
    if q:
        like=f"%{q.strip()}%"
        query=query.filter(
            (models.ForensicAnalysis.case_id.ilike(like)) |
            (models.ForensicAnalysis.analysis_type.ilike(like))
        )
    return query.limit(100).all()

@app.get("/emails", response_model=list[schemas.EmailResponse])
def emails(q:str="", db: Session=Depends(get_db), user=Depends(get_current_user)):
    query=db.query(models.Email)
    if user.role!="admin":
        query=query.join(models.Investigation,isouter=True).filter(
            (models.Investigation.user_id==user.id) | (models.Email.investigation_id==None)
        )
    if q:
        like=f"%{q.strip()}%"
        query=query.filter(
            (models.Email.sender.ilike(like)) |
            (models.Email.recipient.ilike(like)) |
            (models.Email.subject.ilike(like)) |
            (models.Email.body.ilike(like)) |
            (models.Email.threat_level.ilike(like))
        )
    return query.order_by(models.Email.id.desc()).limit(100).all()

@app.get("/emails/{email_id}")
def email_detail(email_id:int, db:Session=Depends(get_db), user=Depends(get_current_user)):
    e=db.query(models.Email).filter(models.Email.id==email_id).first()
    if not e: raise HTTPException(404,"Email not found")
    if user.role!="admin" and e.investigation_id:
        inv=db.query(models.Investigation).filter(models.Investigation.id==e.investigation_id).first()
        if not inv or inv.user_id!=user.id: raise HTTPException(403,"Email access denied")
    fa_query=db.query(models.ForensicAnalysis).filter(models.ForensicAnalysis.email_id==e.id).order_by(models.ForensicAnalysis.id.desc())
    if user.role!="admin":
        fa_query=fa_query.outerjoin(models.Investigation).filter((models.ForensicAnalysis.investigation_id==None)|(models.Investigation.user_id==user.id))
    forensic_cases=[{"id":f.id,"email_id":f.email_id,"investigation_id":f.investigation_id,"case_id":f.case_id,"analysis_type":f.analysis_type,"result_json":f.result_json,"created_at":f.created_at} for f in fa_query.all()]
    return {"id":e.id,"sender":e.sender,"recipient":e.recipient,"subject":e.subject,"body":e.body,"threat_level":e.threat_level,"investigation_id":e.investigation_id,"created_at":e.created_at,"urls":[{"url":u.url,"risk_level":u.risk_level,"domain":u.domain.domain_name if u.domain else None} for u in e.urls],"ips":[{"ip_address":x.ip_address,"country":x.country,"city":x.city,"reputation":x.reputation,"created_at":x.created_at} for x in e.ip_addresses],"ai_results":[{"prediction":a.prediction,"confidence_score":a.confidence_score,"explanation":a.explanation,"created_at":a.created_at} for a in e.ai_results],"forensic_cases":forensic_cases}

@app.get("/reports")
def reports(db: Session=Depends(get_db), user=Depends(get_current_user)):
    q=db.query(models.ForensicAnalysis).order_by(models.ForensicAnalysis.id.desc())
    if user.role!="admin": q=q.outerjoin(models.Investigation).filter((models.ForensicAnalysis.investigation_id==None)|(models.Investigation.user_id==user.id))
    rows=[]
    for r in q.limit(100).all():
        try: data=json.loads(r.result_json)
        except Exception: data={}
        executive=data.get("executive_summary",{}) if isinstance(data,dict) else {}
        if not executive and isinstance(data,dict):
            executive=data.get("report",{}).get("executive_summary",{}) or data.get("case_risk",{}) or data.get("risk_analysis",{})
        rows.append({"id":r.id,"case_id":r.case_id,"analysis_type":r.analysis_type,"created_at":r.created_at,"title":f"Forensic Report — {r.case_id}","summary":executive.get("overall_risk") or data.get("risk_analysis",{}).get("risk_level") or data.get("case",{}).get("risk",{}).get("level") or "Analysis completed","executive_summary":executive})
    return rows

@app.post("/reports/from-forensic/{forensic_id}")
def report_from_forensic(forensic_id:int, db: Session=Depends(get_db), user=Depends(get_current_user)):
    r=db.query(models.ForensicAnalysis).filter(models.ForensicAnalysis.id==forensic_id).first()
    if not r: raise HTTPException(404,"Forensic analysis not found")
    if user.role!="admin" and r.investigation_id:
        inv=db.query(models.Investigation).filter(models.Investigation.id==r.investigation_id).first()
        if not inv or inv.user_id!=user.id: raise HTTPException(403,"Access denied")
    try: data=json.loads(r.result_json)
    except Exception: data={"raw":r.result_json}
    executive=data.get("executive_summary",{}) if isinstance(data,dict) else {}
    if not executive and isinstance(data,dict):
        executive=data.get("report",{}).get("executive_summary",{}) or data.get("case_risk",{}) or data.get("risk_analysis",{})
    return {"id":r.id,"case_id":r.case_id,"analysis_type":r.analysis_type,"created_at":r.created_at,"title":f"Forensic Report — {r.case_id}","summary":executive,"executive_summary":executive,"data":data}

@app.get("/admin/users")
def admin_users(db: Session=Depends(get_db), user=Depends(require_admin)):
    users=db.query(models.User).order_by(models.User.id.asc()).all()
    rows=[]
    for u in users:
        logs=db.query(models.AuditLog).filter(models.AuditLog.user_id==u.id).order_by(models.AuditLog.id.desc()).limit(100).all()
        login_logs=[x for x in logs if x.action in {"login","admin_login","register"}]
        last_ip = login_logs[0].ip_address if login_logs else None
        geo = analyze_ip(last_ip) if last_ip else {}
        rows.append({
            "id":u.id,"name":u.name,"email":u.email,"role":u.role,"created_at":u.created_at,
            "last_ip": last_ip,
            "last_seen": login_logs[0].created_at if login_logs else None,
            "login_count": sum(1 for x in logs if x.action in {"login","admin_login"}),
            "is_active": bool(u.is_active),
            "last_country": geo.get("country"),
            "last_country_code": geo.get("country_code"),
            "last_region": geo.get("region"),
            "last_city": geo.get("city"),
            "last_isp": geo.get("isp"),
        })
    return rows

@app.get("/admin/audit-logs")
def admin_audit_logs(limit:int=200, db: Session=Depends(get_db), user=Depends(require_admin)):
    limit=max(1,min(limit,500))
    rows=db.query(models.AuditLog, models.User).outerjoin(models.User, models.AuditLog.user_id==models.User.id).order_by(models.AuditLog.id.desc()).limit(limit).all()
    return [{"id":log.id,"user_id":log.user_id,"name":u.name if u else None,"email":u.email if u else None,"role":u.role if u else None,"action":log.action,"ip_address":log.ip_address,"user_agent":log.user_agent,"details":log.details,"created_at":log.created_at} for log,u in rows]


@app.post("/admin/users/{user_id}/reset-password")
def admin_reset_password(user_id:int, request: Request, db: Session=Depends(get_db), admin=Depends(require_admin)):
    target=db.query(models.User).filter(models.User.id==user_id).first()
    if not target: raise HTTPException(404, "User not found")
    if target.id == admin.id: raise HTTPException(400, "Use the administrator password configuration to change the admin password")
    import secrets, string
    alphabet=string.ascii_letters + string.digits + "!@#$%*-_"
    temporary="".join(secrets.choice(alphabet) for _ in range(16))
    target.password_hash=hash_password(temporary)
    audit(db, admin, request, "admin_password_reset", f"Reset password for user {target.email}")
    db.commit()
    return {"user_id":target.id, "email":target.email, "temporary_password":temporary, "message":"Temporary password generated. Give it to the user securely; it is shown only in this response."}

@app.delete("/admin/users/{user_id}")
def admin_delete_user(user_id:int, request: Request, db: Session=Depends(get_db), admin=Depends(require_admin)):
    target=db.query(models.User).filter(models.User.id==user_id).first()
    if not target: raise HTTPException(404, "User not found")
    if target.id == admin.id: raise HTTPException(400, "You cannot delete the administrator account currently in use")
    if target.role == "admin": raise HTTPException(403, "Administrator accounts cannot be removed from the user console")
    # Preserve investigations and audit history while removing the account identity.
    db.query(models.Investigation).filter(models.Investigation.user_id==target.id).update({models.Investigation.user_id:None}, synchronize_session=False)
    db.query(models.AuditLog).filter(models.AuditLog.user_id==target.id).update({models.AuditLog.user_id:None}, synchronize_session=False)
    audit(db, admin, request, "admin_delete_user", f"Removed user account {target.email}")
    email=target.email
    db.delete(target)
    db.commit()
    return {"message":"User account removed", "email":email}

@app.post("/admin/users/{user_id}/ban")
def admin_ban_user(user_id:int, request: Request, db: Session=Depends(get_db), admin=Depends(require_admin)):
    target=db.query(models.User).filter(models.User.id==user_id).first()
    if not target: raise HTTPException(404, "User not found")
    if target.id == admin.id or target.role == "admin": raise HTTPException(403, "Administrator accounts cannot be banned from the user console")
    target.is_active = 0
    audit(db, admin, request, "admin_ban_user", f"Banned user account {target.email}")
    db.commit()
    return {"message":"User banned", "user_id":target.id, "is_active":False}

@app.post("/admin/users/{user_id}/unban")
def admin_unban_user(user_id:int, request: Request, db: Session=Depends(get_db), admin=Depends(require_admin)):
    target=db.query(models.User).filter(models.User.id==user_id).first()
    if not target: raise HTTPException(404, "User not found")
    if target.role == "admin": raise HTTPException(403, "Administrator accounts are not managed here")
    target.is_active = 1
    audit(db, admin, request, "admin_unban_user", f"Unbanned user account {target.email}")
    db.commit()
    return {"message":"User unbanned", "user_id":target.id, "is_active":True}

@app.get("/admin/ip-intel")
def admin_ip_intel(ip:str, db: Session=Depends(get_db), admin=Depends(require_admin)):
    if not ip or len(ip)>64: raise HTTPException(400, "Invalid IP address")
    result=analyze_ip(ip)
    return result

@app.get("/ai-results", response_model=list[schemas.AIResultResponse])
def ai_results(db:Session=Depends(get_db), user=Depends(get_current_user)): return db.query(models.AIResult).order_by(models.AIResult.id.desc()).limit(100).all()
