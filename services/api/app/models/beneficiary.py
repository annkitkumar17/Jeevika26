import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, Float, ForeignKey, JSON, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base

class Beneficiary(Base):
    __tablename__ = "beneficiaries"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, unique=True)
    assigned_facilitator_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    gender = Column(String(20), nullable=True)
    age = Column(Integer, nullable=True)
    preferred_language = Column(String(10), default="hi", nullable=False)
    
    # Location
    state = Column(String(100), default="Uttar Pradesh", nullable=False)
    district = Column(String(100), default="Lucknow", nullable=False)
    block = Column(String(100), default="Sadar", nullable=False)
    village = Column(String(100), default="Rampur Demo", nullable=False)
    latitude = Column(Float, default=26.8467, nullable=True)
    longitude = Column(Float, default=80.9462, nullable=True)
    location_consent_granted = Column(Boolean, default=False, nullable=False)
    location_accuracy_meters = Column(Float, nullable=True)
    
    # Livelihood Profile
    education = Column(String(100), nullable=True)
    current_work = Column(String(255), nullable=True)
    traditional_occupation = Column(String(255), nullable=True)
    experience_years = Column(String(50), nullable=True)
    skills = Column(JSON, default=list, nullable=False)
    preferences = Column(JSON, default=dict, nullable=False)  # {"employment_type": "self_employment", "max_travel_km": 25, "migration": False}
    consent = Column(JSON, default=dict, nullable=False)
    
    # Field level extraction provenance & confidence
    field_provenance = Column(JSON, default=dict, nullable=False)
    
    status = Column(String(50), default="profiled", nullable=False)  # profiled, in_review, recommended, enrolled, completed
    enrolled_pathway_id = Column(String(36), nullable=True)
    data_status = Column(String(50), default="demo_seeded", nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", foreign_keys=[user_id], back_populates="beneficiary")
    assigned_facilitator = relationship("User", foreign_keys=[assigned_facilitator_id])
    sessions = relationship("VoiceSession", back_populates="beneficiary", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="beneficiary", cascade="all, delete-orphan")
    outcomes = relationship("Outcome", back_populates="beneficiary", cascade="all, delete-orphan")
