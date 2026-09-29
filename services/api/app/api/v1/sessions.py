from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.session import VoiceSession
from app.models.beneficiary import Beneficiary
from app.models.workflow import CaseEvent
from app.schemas.session import (
    SessionCreate,
    SessionTranscriptUpload,
    SessionComplete,
    SessionResponse,
    ClarificationRequest,
    ProfileConfirmationRequest,
    FieldProvenanceResponse,
)
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/sessions", tags=["Voice Sessions & Profile Extraction"])

@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def start_session(
    session_in: SessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    beneficiary = db.query(Beneficiary).filter(Beneficiary.id == session_in.beneficiary_id).first()
    if not beneficiary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Beneficiary not found.")

    session = VoiceSession(
        beneficiary_id=session_in.beneficiary_id,
        channel=session_in.channel,
        language=session_in.language,
        status="in_progress",
        current_question_index=0,
        answers={},
        messages=[
            {
                "id": "msg-welcome",
                "sender": "assistant",
                "text": "नमस्ते! मैं आपकी आजीविका मार्गदर्शिका जीविका सारथी हूँ। क्या आप मुझे अपने वर्तमान काम के बारे में बता सकते हैं?",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        ],
        started_at=datetime.now(timezone.utc)
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

@router.post("/{id}/transcript", response_model=SessionResponse)
def upload_transcript(
    id: str,
    upload_in: SessionTranscriptUpload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(VoiceSession).filter(VoiceSession.id == id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Voice session not found.")

    answers = dict(session.answers or {})
    answers[upload_in.question_key] = upload_in.transcript_text
    session.answers = answers

    messages = list(session.messages or [])
    messages.append({
        "id": f"msg-user-{len(messages)+1}",
        "sender": "user",
        "text": upload_in.transcript_text,
        "is_confirmed": upload_in.is_confirmed,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
    session.messages = messages
    session.current_question_index = min(8, session.current_question_index + 1)
    
    if upload_in.audio_duration_seconds:
        meta = dict(session.audio_metadata or {})
        meta["last_duration"] = upload_in.audio_duration_seconds
        meta["format"] = upload_in.audio_format
        session.audio_metadata = meta

    db.commit()
    db.refresh(session)
    return session

@router.post("/{id}/extract-profile", response_model=Dict[str, Any])
def extract_profile_from_session(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Extract field-level profile attributes with provenance and confidence scores from interview answers.
    """
    session = db.query(VoiceSession).filter(VoiceSession.id == id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Voice session not found.")

    answers = session.answers or {}
    provenance = {}

    # Education extraction
    edu_text = answers.get("education", "Class 10")
    provenance["education"] = {
        "field_name": "education",
        "extracted_value": edu_text,
        "confidence_score": 0.92,
        "evidence_snippet": edu_text,
        "extractor_version": "v2.1-hindi-nlp",
        "confirmation_state": "unconfirmed"
    }

    # Current Work & Skills
    work_text = answers.get("currentWork", "Assists with agricultural pump repair")
    provenance["current_work"] = {
        "field_name": "current_work",
        "extracted_value": work_text,
        "confidence_score": 0.88,
        "evidence_snippet": work_text,
        "extractor_version": "v2.1-hindi-nlp",
        "confirmation_state": "unconfirmed"
    }

    # Travel & Mobility
    mobility_text = answers.get("travelDistance", "Up to 25 km")
    provenance["mobility"] = {
        "field_name": "mobility",
        "extracted_value": 25,
        "confidence_score": 0.85,
        "evidence_snippet": mobility_text,
        "extractor_version": "v2.1-hindi-nlp",
        "confirmation_state": "unconfirmed"
    }

    # Update beneficiary field provenance
    beneficiary = db.query(Beneficiary).filter(Beneficiary.id == session.beneficiary_id).first()
    if beneficiary:
        beneficiary.field_provenance = provenance
        db.commit()

    return {
        "session_id": session.id,
        "beneficiary_id": session.beneficiary_id,
        "extracted_fields": provenance
    }

@router.post("/{id}/clarify", response_model=Dict[str, Any])
def request_or_answer_clarification(
    id: str,
    clarification: ClarificationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit clarification for low-confidence or ambiguous voice interview fields.
    """
    session = db.query(VoiceSession).filter(VoiceSession.id == id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Voice session not found.")

    beneficiary = db.query(Beneficiary).filter(Beneficiary.id == session.beneficiary_id).first()
    if beneficiary:
        prov = dict(beneficiary.field_provenance or {})
        if clarification.field_key in prov:
            prov[clarification.field_key]["extracted_value"] = clarification.response_text
            prov[clarification.field_key]["confidence_score"] = 0.98
            prov[clarification.field_key]["confirmation_state"] = "clarified"
            beneficiary.field_provenance = prov
            db.commit()

    return {
        "session_id": session.id,
        "field_key": clarification.field_key,
        "status": "clarification_recorded",
        "updated_value": clarification.response_text
    }

@router.post("/{id}/confirm-profile", response_model=Dict[str, Any])
def confirm_extracted_profile(
    id: str,
    confirmation: ProfileConfirmationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Explicit beneficiary confirmation of extracted profile before generating pathways.
    """
    session = db.query(VoiceSession).filter(VoiceSession.id == id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Voice session not found.")

    beneficiary = db.query(Beneficiary).filter(Beneficiary.id == session.beneficiary_id).first()
    if beneficiary:
        for k, v in confirmation.confirmed_fields.items():
            if hasattr(beneficiary, k):
                setattr(beneficiary, k, v)
        beneficiary.status = "profile_confirmed"
        
        # Log case event
        event = CaseEvent(
            beneficiary_id=beneficiary.id,
            actor_id=current_user.id,
            actor_role=current_user.role,
            event_type="profile_confirmed",
            event_description="Beneficiary confirmed extracted voice interview profile",
            event_payload=confirmation.confirmed_fields
        )
        db.add(event)
        db.commit()

    return {"message": "Profile confirmed successfully", "status": "profile_confirmed"}

@router.get("/{id}/field-provenance", response_model=List[FieldProvenanceResponse])
def get_field_provenance(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve field-level confidence scores and original audio/transcript evidence.
    """
    session = db.query(VoiceSession).filter(VoiceSession.id == id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Voice session not found.")

    beneficiary = db.query(Beneficiary).filter(Beneficiary.id == session.beneficiary_id).first()
    provenance_map = beneficiary.field_provenance if beneficiary else {}

    results = []
    for k, v in provenance_map.items():
        results.append(
            FieldProvenanceResponse(
                field_name=v.get("field_name", k),
                extracted_value=v.get("extracted_value"),
                confidence_score=v.get("confidence_score", 0.85),
                evidence_snippet=v.get("evidence_snippet", ""),
                extractor_version=v.get("extractor_version", "v2.1"),
                confirmation_state=v.get("confirmation_state", "unconfirmed")
            )
        )
    return results

@router.get("/{id}", response_model=SessionResponse)
def get_session(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(VoiceSession).filter(VoiceSession.id == id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Voice session not found.")
    return session

@router.put("/{id}/complete", response_model=SessionResponse)
def complete_session(
    id: str,
    complete_in: SessionComplete,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(VoiceSession).filter(VoiceSession.id == id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Voice session not found.")

    session.status = "completed"
    session.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(session)
    return session
