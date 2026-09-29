import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, JSON, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Qualification(Base):
    __tablename__ = "qualifications"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    qp_code = Column(String(50), unique=True, nullable=False, index=True) # e.g. "ELE/Q5901"
    qualification_code = Column(String(100), nullable=True, index=True) # NQR Official Code
    title = Column(String(255), nullable=False)
    sector = Column(String(100), nullable=False)
    nsqf_level = Column(Integer, nullable=False)
    version = Column(String(50), default="1.0", nullable=False)
    
    awarding_body = Column(String(255), default="Skill Council for Green Jobs", nullable=False)
    approval_date = Column(String(50), nullable=True)
    currency_start = Column(String(50), nullable=True)
    currency_end = Column(String(50), nullable=True)
    archive_status = Column(String(50), default="active", nullable=False) # active, archived, revised
    nsqc_status = Column(String(50), default="approved", nullable=False) # approved, pending, expired
    qualification_file_url = Column(String(500), nullable=True)
    
    # Provenance link
    source_id = Column(String(36), nullable=True, index=True) # Links to DataSource
    source_record_id = Column(String(100), nullable=True)
    last_verified_at = Column(DateTime, nullable=True)
    verification_status = Column(String(50), default="verified", nullable=False) # verified, pending_review, stale, rejected
    
    description = Column(Text, nullable=True)
    entry_requirements = Column(String(255), nullable=True)
    learning_outcomes = Column(JSON, default=list, nullable=False)
    nos_units = Column(JSON, default=list, nullable=False) # National Occupational Standards units
    assessment_requirements = Column(JSON, default=dict, nullable=False)
    rpl_available = Column(Boolean, default=True, nullable=False)
    
    duration_hours = Column(Integer, default=300, nullable=False)
    curriculum_modules = Column(JSON, default=list, nullable=False)
    potential_job_roles = Column(JSON, default=list, nullable=False)
    average_salary_range = Column(String(100), nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    recommendations = relationship("Recommendation", back_populates="qualification")
