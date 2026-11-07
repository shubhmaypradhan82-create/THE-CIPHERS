from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    # Optional browser-observed public IP. This is used only as a supplemental
    # value in local development where the backend sees 127.0.0.1.
    client_ip: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class InvestigationCreate(BaseModel):
    title: str
    description: Optional[str] = None
    user_id: Optional[int] = None

class ProfileUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=100)

class InvestigationUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class InvestigationResponse(InvestigationCreate):
    id: int
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AnalyzeRequest(BaseModel):
    sender: str = ""
    recipient: str = ""
    subject: str = ""
    body: str = ""
    url: Optional[str] = None
    investigation_id: Optional[int] = None

class ForensicURLRequest(BaseModel):
    url: str = Field(min_length=1, max_length=4096)
    investigation_id: Optional[int] = None

class ForensicAnalysisResponse(BaseModel):
    id: int
    email_id: Optional[int]
    investigation_id: Optional[int]
    case_id: str
    analysis_type: str
    result_json: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AnalyzeResponse(BaseModel):
    email_id: int
    threat_level: str
    confidence_score: float
    prediction: str
    explanation: str
    urls: List[Dict[str, Any]]
    ips: List[Dict[str, Any]]
    cybersecurity_engine: Dict[str, Any]
    ai: Dict[str, Any]

class EmailResponse(BaseModel):
    id: int
    sender: str
    recipient: str
    subject: Optional[str]
    body: Optional[str]
    threat_level: str
    investigation_id: Optional[int]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AIResultResponse(BaseModel):
    id: int
    email_id: int
    prediction: str
    confidence_score: Optional[float]
    explanation: Optional[str]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
