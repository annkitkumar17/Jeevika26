import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class VoiceSession(Base):
    __tablename__ = "voice_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    beneficiary_id = Column(String(36), ForeignKey("beneficiaries.id", ondelete="CASCADE"), nullable=False)
    
    channel = Column(String(50), default="web_voice", nullable=False)  # web_voice, ivr, whatsapp, kiosk
    language = Column(String(10), default="hi", nullable=False)
    status = Column(String(50), default="in_progress", nullable=False)  # in_progress, completed, abandoned
    current_question_index = Column(Integer, default=0, nullable=False)
    
    answers = Column(JSON, default=dict, nullable=False)
    messages = Column(JSON, default=list, nullable=False)  # list of chat bubbles
    audio_metadata = Column(JSON, default=dict, nullable=True)  # duration, sample_rate, codec
    
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime, nullable=True)

    beneficiary = relationship("Beneficiary", back_populates="sessions")
