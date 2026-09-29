import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    beneficiary_id = Column(String(36), ForeignKey("beneficiaries.id", ondelete="CASCADE"), nullable=False)
    qualification_id = Column(String(36), ForeignKey("qualifications.id", ondelete="CASCADE"), nullable=False)
    
    rank = Column(Integer, nullable=False)
    match_score = Column(Float, nullable=False)  # 0 to 100
    
    # Pathway Pipeline Score Breakdown (Weights: Aspiration 20%, Skills 20%, Entry 15%, Local Opportunity 15%, Centre Access 10%, Mobility 10%, RPL 5%, Outcomes 5%)
    score_breakdown = Column(JSON, default=dict, nullable=False)
    
    fit_reason = Column(String(500), nullable=False)
    fit_details = Column(JSON, default=list, nullable=False) # why_this_fits
    skill_gaps = Column(JSON, default=list, nullable=False)
    evidence = Column(JSON, default=list, nullable=False) # authoritative evidence list
    unknowns = Column(JSON, default=list, nullable=False) # missing or unverified data flags
    risks = Column(JSON, default=list, nullable=False) # identified constraint flags
    next_actions = Column(JSON, default=list, nullable=False)
    
    human_review_required = Column(Boolean, default=False, nullable=False)
    human_validated = Column(Boolean, default=False, nullable=False)
    
    local_opportunity_signal = Column(String(100), default="High local demand", nullable=False)
    nearest_centre_id = Column(String(36), nullable=True)
    nearest_centre_distance_km = Column(Float, nullable=True)
    
    rpl_eligible = Column(Boolean, default=True, nullable=False)
    risk_factor = Column(String(255), nullable=True)
    status = Column(String(50), default="generated", nullable=False)  # generated, selected, enrolled, rejected
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    beneficiary = relationship("Beneficiary", back_populates="recommendations")
    qualification = relationship("Qualification", back_populates="recommendations")
