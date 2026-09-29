from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class SyncEventCreate(BaseModel):
    idempotency_key: str
    device_id: Optional[str] = None
    entity_type: str
    entity_id: str
    action: str
    payload: Dict[str, Any]

class SyncEventResponse(BaseModel):
    id: str
    idempotency_key: str
    entity_type: str
    entity_id: str
    sync_status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class NotificationResponse(BaseModel):
    id: str
    user_id: str
    channel: str
    title: str
    message: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

class LocationConsentRequest(BaseModel):
    granted: bool
    accuracy_meters: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
