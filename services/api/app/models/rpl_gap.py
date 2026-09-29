import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, JSON, Text, ForeignKey, Integer
from app.core.database import Base

class RPLAssessment(Base):
    __tablename__ = "rpl_assessments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    beneficiary_id = Column(String(36), ForeignKey("beneficiaries.id", ondelete="CASCADE"), nullable=False, index=True)
    target_qualification_id = Column(String(36), ForeignKey("qualifications.id", ondelete="CASCADE"), nullable=False, index=True)
    
    status = Column(String(50), default="eligible", nullable=False) # eligible, in_screening, certified, bridge_needed, not_eligible
    current_skill_evidence = Column(JSON, default=list, nullable=False)
    missing_nos_units = Column(JSON, default=list, nullable=False)
    bridge_modules = Column(JSON, default=list, nullable=False)
    
    estimated_bridge_hours = Column(Integer, default=40, nullable=False)
    assessor_id = Column(String(36), nullable=True) # Facilitator / Certified Assessor
    assessment_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class SkillGap(Base):
    __tablename__ = "skill_gaps"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    beneficiary_id = Column(String(36), ForeignKey("beneficiaries.id", ondelete="CASCADE"), nullable=False, index=True)
    qualification_id = Column(String(36), ForeignKey("qualifications.id", ondelete="CASCADE"), nullable=False, index=True)
    nos_unit_id = Column(String(100), nullable=True)
    
    gap_type = Column(String(50), default="technical_depth", nullable=False) # technical_depth, safety_standard, certification_formal, digital_literacy
    severity = Column(String(50), default="medium", nullable=False) # low, medium, high, blocker
    evidence = Column(Text, nullable=True)
    recommended_intervention = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
