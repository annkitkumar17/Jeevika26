import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, JSON, Text
from app.core.database import Base

class TrainingCentre(Base):
    __tablename__ = "training_centres"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    centre_code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    centre_type = Column(String(100), default="PMKK", nullable=False)  # PMKK, ITI, DDU-GKY, RSETI, NGO
    
    address = Column(Text, nullable=False)
    state = Column(String(100), default="Uttar Pradesh", nullable=False)
    district = Column(String(100), default="Lucknow", nullable=False)
    block = Column(String(100), default="Sadar", nullable=False)
    pincode = Column(String(10), nullable=True)
    
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    contact_person = Column(String(100), nullable=True)
    contact_phone = Column(String(20), nullable=True)
    offered_courses = Column(JSON, default=list, nullable=False)  # list of QP codes
    batch_status = Column(String(50), default="Admissions Open", nullable=False)
    next_batch_date = Column(String(50), nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
