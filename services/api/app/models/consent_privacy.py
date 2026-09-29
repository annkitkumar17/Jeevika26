import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, JSON, Text, ForeignKey, Boolean
from app.core.database import Base

class PurposeConsent(Base):
    __tablename__ = "purpose_consents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    purpose = Column(String(100), nullable=False, index=True) # profile_creation, recommendation_generation, facilitator_sharing, follow_up_retention, location_proximity
    
    is_granted = Column(Boolean, default=True, nullable=False)
    version = Column(String(20), default="v1.0", nullable=False)
    consent_text = Column(Text, nullable=False)
    language = Column(String(10), default="hi", nullable=False)
    
    granted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    withdrawn_at = Column(DateTime, nullable=True)

class PrivacyRequest(Base):
    __tablename__ = "privacy_requests"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    request_type = Column(String(50), nullable=False) # export_data, delete_account, correct_data
    status = Column(String(50), default="pending", nullable=False) # pending, processing, completed, rejected
    
    requested_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime, nullable=True)
    export_payload = Column(JSON, default=dict, nullable=True)

class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    actor_id = Column(String(36), nullable=False, index=True)
    actor_role = Column(String(50), nullable=False)
    action = Column(String(100), nullable=False, index=True) # sensitive_read, export_data, consent_withdrawn, user_provisioned, import_published, profile_updated
    
    resource_type = Column(String(100), nullable=False) # beneficiary, user, data_import, consent
    resource_id = Column(String(36), nullable=True)
    ip_address = Column(String(50), nullable=True)
    details = Column(JSON, default=dict, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
