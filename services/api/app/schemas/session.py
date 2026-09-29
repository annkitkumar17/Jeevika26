from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class ChatMessageSchema(BaseModel):
    id: str
    sender: str  # user, assistant, system
    text: str
    audio_url: Optional[str] = None
    is_confirmed: Optional[bool] = False
    timestamp: Optional[str] = None

class SessionCreate(BaseModel):
    beneficiary_id: str
    channel: str = "web_voice"
    language: str = "hi"

class SessionTranscriptUpload(BaseModel):
    question_key: str
    transcript_text: str
    audio_duration_seconds: Optional[float] = None
    audio_format: Optional[str] = "audio/webm"
    is_confirmed: bool = True

class SessionComplete(BaseModel):
    extract_profile: bool = True

class ClarificationRequest(BaseModel):
    field_key: str # e.g. "workExperience", "mobility", "traditionalSkill"
    clarification_question: str
    response_text: str

class ProfileConfirmationRequest(BaseModel):
    confirmed_fields: Dict[str, Any]

class FieldProvenanceResponse(BaseModel):
    field_name: str
    extracted_value: Any
    confidence_score: float # 0.0 to 1.0
    evidence_snippet: str
    extractor_version: str
    confirmation_state: str # unconfirmed, confirmed, modified, needs_clarification

class SessionResponse(BaseModel):
    id: str
    beneficiary_id: str
    channel: str
    language: str
    status: str
    current_question_index: int
    answers: Dict[str, Any]
    messages: List[Dict[str, Any]]
    audio_metadata: Optional[Dict[str, Any]]
    started_at: datetime
    completed_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
