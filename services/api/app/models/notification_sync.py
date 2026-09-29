import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, JSON, Text, ForeignKey, Boolean
from app.core.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    channel = Column(String(50), default="in_app", nullable=False) # in_app, sms, whatsapp, ivr, email
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    
    status = Column(String(50), default="queued", nullable=False) # queued, sent, failed, read
    provider_response = Column(JSON, default=dict, nullable=True)
    read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class SyncEvent(Base):
    __tablename__ = "sync_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    idempotency_key = Column(String(100), unique=True, nullable=False, index=True)
    device_id = Column(String(100), nullable=True)
    entity_type = Column(String(50), nullable=False) # voice_transcript, referral, review_task, follow_up
    
    entity_id = Column(String(36), nullable=False)
    action = Column(String(50), nullable=False) # create, update, append
    payload = Column(JSON, default=dict, nullable=False)
    sync_status = Column(String(50), default="applied", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class TokenBlocklist(Base):
    __tablename__ = "token_blocklist"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    jti = Column(String(100), unique=True, nullable=False, index=True) # Token identifier or raw token hash
    revoked_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    expires_at = Column(DateTime, nullable=False)

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token = Column(String(100), unique=True, nullable=False, index=True)
    is_used = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
