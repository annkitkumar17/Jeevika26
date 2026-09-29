from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class PurposeConsentCreate(BaseModel):
    purpose: str # profile_creation, recommendation_generation, facilitator_sharing, follow_up_retention, location_proximity
    consent_text: str
    language: str = "hi"
    is_granted: bool = True
    version: str = "v1.0"

class PurposeConsentResponse(PurposeConsentCreate):
    id: str
    user_id: str
    granted_at: datetime
    withdrawn_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class PrivacyExportResponse(BaseModel):
    user_id: str
    exported_at: datetime
    data: Dict[str, Any]

class AuditEventResponse(BaseModel):
    id: str
    actor_id: str
    actor_role: str
    action: str
    resource_type: str
    resource_id: Optional[str]
    details: Dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
