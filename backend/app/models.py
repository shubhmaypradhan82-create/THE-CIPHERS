from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)
    role = Column(String(50), default="analyst")
    is_active = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    investigations = relationship("Investigation", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True)
    ip_address = Column(String(64), nullable=True, index=True)
    user_agent = Column(String(500), nullable=True)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    user = relationship("User", back_populates="audit_logs")

class Investigation(Base):
    __tablename__ = "investigations"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="open")
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="investigations")
    emails = relationship("Email", back_populates="investigation")
    osint_data = relationship("OSINTData", back_populates="investigation")
    evidence_items = relationship("Evidence", back_populates="investigation")
    reports = relationship("Report", back_populates="investigation")

class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"), nullable=True)
    sender = Column(String(255), nullable=False)
    recipient = Column(String(255), nullable=False)
    subject = Column(String(500))
    body = Column(Text)
    threat_level = Column(String(50), default="safe")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    investigation = relationship("Investigation", back_populates="emails")
    headers = relationship("EmailHeader", back_populates="email", cascade="all, delete-orphan")
    urls = relationship("URL", back_populates="email", cascade="all, delete-orphan")
    ip_addresses = relationship("IPAddress", back_populates="email", cascade="all, delete-orphan")
    ai_results = relationship("AIResult", back_populates="email", cascade="all, delete-orphan")

class EmailHeader(Base):
    __tablename__ = "email_headers"
    id = Column(Integer, primary_key=True)
    email_id = Column(Integer, ForeignKey("emails.id"), nullable=False)
    header_name = Column(String(255), nullable=False)
    header_value = Column(Text)
    email = relationship("Email", back_populates="headers")

class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True)
    email_id = Column(Integer, ForeignKey("emails.id"), nullable=False)
    url = Column(Text, nullable=False)
    risk_level = Column(String(50), default="unknown")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    email = relationship("Email", back_populates="urls")
    domain = relationship("Domain", back_populates="url", uselist=False, cascade="all, delete-orphan")

class Domain(Base):
    __tablename__ = "domains"
    id = Column(Integer, primary_key=True)
    url_id = Column(Integer, ForeignKey("urls.id"), nullable=False)
    domain_name = Column(String(255), nullable=False)
    reputation = Column(String(100), default="unknown")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    url = relationship("URL", back_populates="domain")

class IPAddress(Base):
    __tablename__ = "ip_addresses"
    id = Column(Integer, primary_key=True)
    email_id = Column(Integer, ForeignKey("emails.id"), nullable=True)
    ip_address = Column(String(50), nullable=False)
    country = Column(String(100))
    city = Column(String(100))
    reputation = Column(String(100), default="unknown")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    email = relationship("Email", back_populates="ip_addresses")

class OSINTData(Base):
    __tablename__ = "osint_data"
    id = Column(Integer, primary_key=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"), nullable=False)
    source = Column(String(255), nullable=False)
    data = Column(Text)
    collected_at = Column(DateTime(timezone=True), server_default=func.now())
    investigation = relationship("Investigation", back_populates="osint_data")

class AIResult(Base):
    __tablename__ = "ai_results"
    id = Column(Integer, primary_key=True)
    email_id = Column(Integer, ForeignKey("emails.id"), nullable=False)
    prediction = Column(String(100), nullable=False)
    confidence_score = Column(Float)
    explanation = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    email = relationship("Email", back_populates="ai_results")

class Evidence(Base):
    __tablename__ = "evidence"
    id = Column(Integer, primary_key=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"), nullable=False)
    evidence_type = Column(String(100), nullable=False)
    description = Column(Text)
    file_path = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    investigation = relationship("Investigation", back_populates="evidence_items")

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"), nullable=False)
    title = Column(String(255), nullable=False)
    summary = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    investigation = relationship("Investigation", back_populates="reports")

class ForensicAnalysis(Base):
    __tablename__ = "forensic_analyses"
    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails.id"), nullable=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"), nullable=True, index=True)
    case_id = Column(String(100), nullable=False, index=True)
    analysis_type = Column(String(50), nullable=False)
    result_json = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    email = relationship("Email")
    investigation = relationship("Investigation")
