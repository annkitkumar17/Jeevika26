import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON, Integer, Text, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Outcome(Base):
    __tablename__ = "outcomes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    beneficiary_id = Column(String(36), ForeignKey("beneficiaries.id", ondelete="CASCADE"), nullable=False)
    pathway_id = Column(String(36), nullable=False)
    
    stage = Column(String(50), default="counseling", nullable=False) # counseling, rpl_screening, bridge_training, assessment, placement, enterprise
    status = Column(String(50), default="in_progress", nullable=False) # in_progress, verified, completed, dropped
    
    facilitator_id = Column(String(36), nullable=True)
    facilitator_notes = Column(String(500), nullable=True)
    
    wage_or_revenue_inr = Column(Float, nullable=True)
    verification_documents = Column(JSON, default=list, nullable=False)
    follow_up_milestones = Column(JSON, default=dict, nullable=False) # {"30_day": "verified", "90_day": "pending", "180_day": "pending"}
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    beneficiary = relationship("Beneficiary", back_populates="outcomes")

class TrainingProgress(Base):
    __tablename__ = "training_progress"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    beneficiary_id = Column(String(36), ForeignKey("beneficiaries.id", ondelete="CASCADE"), nullable=False, index=True)
    training_centre_id = Column(String(36), nullable=False)
    qp_code = Column(String(50), nullable=False)
    
    attendance_percentage = Column(Float, default=0.0, nullable=False)
    modules_completed = Column(Integer, default=0, nullable=False)
    assessment_status = Column(String(50), default="in_training", nullable=False) # in_training, assessment_scheduled, passed, failed, dropout
    certification_number = Column(String(100), nullable=True)
    dropout_reason = Column(String(255), nullable=True)
    
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class EmploymentOutcome(Base):
    __tablename__ = "employment_outcomes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    beneficiary_id = Column(String(36), ForeignKey("beneficiaries.id", ondelete="CASCADE"), nullable=False, index=True)
    employer_name = Column(String(255), nullable=False)
    role_title = Column(String(255), nullable=False)
    joining_date = Column(String(50), nullable=False)
    monthly_wage_inr = Column(Float, nullable=True) # Voluntary reporting
    
    verification_method = Column(String(50), default="facilitator_call", nullable=False) # employer_letter, payslip, facilitator_call, self_report
    retention_status_30_days = Column(String(50), default="pending", nullable=False)
    retention_status_90_days = Column(String(50), default="pending", nullable=False)
    retention_status_180_days = Column(String(50), default="pending", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class EnterpriseOutcome(Base):
    __tablename__ = "enterprise_outcomes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    beneficiary_id = Column(String(36), ForeignKey("beneficiaries.id", ondelete="CASCADE"), nullable=False, index=True)
    enterprise_name = Column(String(255), nullable=False)
    activity_type = Column(String(255), nullable=False) # e.g. "Mobile Solar Pump Repair Service", "Pickle & Agro Processing Unit"
    udyam_or_shg_id = Column(String(100), nullable=True)
    
    credit_scheme_linked = Column(String(100), default="PM-FME / PM-MUDRA", nullable=True)
    loan_amount_sanctioned_inr = Column(Float, nullable=True)
    monthly_estimated_revenue_inr = Column(Float, nullable=True)
    operational_status = Column(String(50), default="active", nullable=False) # active, scaling, paused, closed
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class FollowUp(Base):
    __tablename__ = "follow_ups"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    beneficiary_id = Column(String(36), ForeignKey("beneficiaries.id", ondelete="CASCADE"), nullable=False, index=True)
    milestone = Column(String(20), nullable=False) # 30_day, 90_day, 180_day
    scheduled_date = Column(String(50), nullable=False)
    status = Column(String(50), default="scheduled", nullable=False) # scheduled, completed, missed, rescheduled
    
    assigned_facilitator_id = Column(String(36), nullable=True)
    outcome_summary = Column(Text, nullable=True)
    is_retained = Column(Boolean, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
