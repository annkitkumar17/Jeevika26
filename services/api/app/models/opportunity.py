import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, JSON, Text, ForeignKey, Integer, Boolean
from app.core.database import Base

class Employer(Base):
    __tablename__ = "employers"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True)
    sector = Column(String(100), nullable=False)
    registration_type = Column(String(50), default="MSME", nullable=False) # MSME, Corporate, SHG_Federation, Cooperative, Govt_Contractor
    state = Column(String(100), default="Uttar Pradesh", nullable=False)
    district = Column(String(100), default="Lucknow", nullable=False)
    block = Column(String(100), default="Sadar", nullable=False)
    contact_person = Column(String(100), nullable=True)
    contact_phone = Column(String(20), nullable=True)
    is_verified = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class OpportunitySignal(Base):
    __tablename__ = "opportunity_signals"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sector = Column(String(100), nullable=False, index=True)
    district = Column(String(100), nullable=False, index=True)
    block = Column(String(100), nullable=True)
    
    demand_level = Column(String(50), default="moderate", nullable=False) # high, moderate, low, unknown
    openings_count = Column(Integer, nullable=True) # None indicates unknown
    source_name = Column(String(255), default="District Industry Centre Survey", nullable=False)
    evidence_url = Column(String(500), nullable=True)
    observed_date = Column(String(50), nullable=False)
    expiry_date = Column(String(50), nullable=True)
    
    confidence_score = Column(Float, default=0.85, nullable=False)
    verification_status = Column(String(50), default="verified", nullable=False) # verified, unverified, stale
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class JobOpportunity(Base):
    __tablename__ = "job_opportunities"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employer_id = Column(String(36), ForeignKey("employers.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    role_type = Column(String(50), default="wage_employment", nullable=False) # wage_employment, self_employment_contract, apprentice
    sector = Column(String(100), nullable=False)
    qp_code = Column(String(50), nullable=True)
    
    district = Column(String(100), default="Lucknow", nullable=False)
    block = Column(String(100), default="Sadar", nullable=False)
    wage_min_inr = Column(Float, nullable=True)
    wage_max_inr = Column(Float, nullable=True)
    vacancies = Column(Integer, default=1, nullable=False)
    
    source_id = Column(String(36), nullable=True)
    observed_date = Column(String(50), nullable=False)
    expiry_date = Column(String(50), nullable=True)
    verification_status = Column(String(50), default="verified", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
