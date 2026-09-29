import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, JSON, Text, ForeignKey, Integer, Boolean
from app.core.database import Base

class ReviewTask(Base):
    __tablename__ = "review_tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    beneficiary_id = Column(String(36), ForeignKey("beneficiaries.id", ondelete="CASCADE"), nullable=False, index=True)
    assigned_facilitator_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    task_type = Column(String(50), default="recommendation_review", nullable=False) # recommendation_review, profile_clarification, mobility_check, sensitive_case
    priority = Column(String(20), default="normal", nullable=False) # urgent, high, normal, low
    status = Column(String(50), default="pending", nullable=False) # pending, in_review, approved, modified, rejected
    
    trigger_reason = Column(String(255), nullable=False) # e.g. "Low extraction confidence on work experience", "Travel distance > 25km"
    decision = Column(String(50), nullable=True) # approved, modified, rejected, referred
    decision_notes = Column(Text, nullable=True)
    sla_due_at = Column(DateTime, nullable=True)
    
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class Referral(Base):
    __tablename__ = "referrals"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    idempotency_key = Column(String(100), unique=True, nullable=True, index=True)
    beneficiary_id = Column(String(36), ForeignKey("beneficiaries.id", ondelete="CASCADE"), nullable=False, index=True)
    target_type = Column(String(50), default="training_centre", nullable=False) # training_centre, employer, enterprise_scheme, rpl_assessor
    target_id = Column(String(36), nullable=False)
    
    pathway_id = Column(String(36), nullable=True)
    facilitator_id = Column(String(36), nullable=False)
    status = Column(String(50), default="dispatched", nullable=False) # dispatched, accepted, candidate_contacted, enrolled, rejected, completed
    
    counseling_summary = Column(Text, nullable=True)
    provider_feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

class CaseEvent(Base):
    __tablename__ = "case_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    beneficiary_id = Column(String(36), ForeignKey("beneficiaries.id", ondelete="CASCADE"), nullable=False, index=True)
    actor_id = Column(String(36), nullable=False) # User ID who performed the action
    actor_role = Column(String(50), nullable=False) # beneficiary, facilitator, admin, system
    
    event_type = Column(String(50), nullable=False) # intake_completed, profile_confirmed, pathway_recommended, human_reviewed, referral_dispatched, batch_enrolled, outcome_verified
    event_description = Column(String(500), nullable=False)
    event_payload = Column(JSON, default=dict, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
