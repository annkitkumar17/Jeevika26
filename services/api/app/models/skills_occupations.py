import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, JSON, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base

class SkillConcept(Base):
    __tablename__ = "skill_concepts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    canonical_name = Column(String(255), unique=True, nullable=False, index=True)
    sector = Column(String(100), nullable=False, index=True)
    category = Column(String(100), default="technical", nullable=False) # technical, foundational, entrepreneurial, soft_skill
    
    # Multilingual & Dialect aliases: {"hi": ["पंप मरम्मत", "मोटर रिपेयर"], "bho": ["कल-पुर्जा बनावल"]}
    aliases = Column(JSON, default=dict, nullable=False)
    embedding_id = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class OccupationConcept(Base):
    __tablename__ = "occupation_concepts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), unique=True, nullable=False, index=True)
    nco_code = Column(String(50), nullable=True) # National Classification of Occupations
    sector = Column(String(100), nullable=False)
    is_traditional = Column(String(10), default="no", nullable=False) # yes, no
    aliases = Column(JSON, default=dict, nullable=False)
    associated_skill_ids = Column(JSON, default=list, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class BeneficiarySkillEvidence(Base):
    __tablename__ = "beneficiary_skill_evidences"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    beneficiary_id = Column(String(36), ForeignKey("beneficiaries.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_name = Column(String(255), nullable=False)
    canonical_skill_id = Column(String(36), nullable=True)
    
    evidence_type = Column(String(50), default="voice_stated", nullable=False) # voice_stated, facilitator_verified, prior_certificate, portfolio
    years_experience = Column(Float, default=1.0, nullable=False)
    proficiency_level = Column(String(50), default="intermediate", nullable=False) # beginner, intermediate, advanced, master
    confidence_score = Column(Float, default=0.85, nullable=False) # 0.0 to 1.0
    
    source_session_id = Column(String(36), nullable=True)
    extracted_snippet = Column(Text, nullable=True)
    verification_status = Column(String(50), default="unverified", nullable=False) # unverified, facilitator_verified, rejected
    verified_by = Column(String(36), nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
