from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.core.database import get_db
from app.models.consent_privacy import PurposeConsent, PrivacyRequest, AuditEvent
from app.models.beneficiary import Beneficiary
from app.schemas.consent_privacy import PurposeConsentCreate, PurposeConsentResponse, PrivacyExportResponse
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="", tags=["Consent & Privacy (DPDP)"])

@router.get("/consents", response_model=List[PurposeConsentResponse])
def get_user_consents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all active and past purpose-specific consents for the authenticated user.
    """
    consents = db.query(PurposeConsent).filter(PurposeConsent.user_id == current_user.id).all()
    return consents

@router.post("/consents", response_model=PurposeConsentResponse, status_code=status.HTTP_201_CREATED)
def grant_purpose_consent(
    consent_in: PurposeConsentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Record a free, specific, informed, and unambiguous purpose-specific consent.
    """
    consent = PurposeConsent(
        user_id=current_user.id,
        purpose=consent_in.purpose,
        consent_text=consent_in.consent_text,
        language=consent_in.language,
        is_granted=consent_in.is_granted,
        version=consent_in.version,
        granted_at=datetime.now(timezone.utc)
    )
    db.add(consent)

    audit = AuditEvent(
        actor_id=current_user.id,
        actor_role=current_user.role,
        action="consent_granted",
        resource_type="purpose_consent",
        resource_id=consent.id,
        details={"purpose": consent_in.purpose, "version": consent_in.version}
    )
    db.add(audit)
    db.commit()
    db.refresh(consent)
    return consent

@router.post("/consents/{purpose}/withdraw", response_model=PurposeConsentResponse)
def withdraw_purpose_consent(
    purpose: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Withdraw consent for a specific purpose at any time under DPDP rules.
    """
    consent = db.query(PurposeConsent).filter(
        PurposeConsent.user_id == current_user.id,
        PurposeConsent.purpose == purpose,
        PurposeConsent.is_granted == True
    ).order_by(PurposeConsent.granted_at.desc()).first()

    if not consent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active consent found for this purpose.")

    consent.is_granted = False
    consent.withdrawn_at = datetime.now(timezone.utc)

    audit = AuditEvent(
        actor_id=current_user.id,
        actor_role=current_user.role,
        action="consent_withdrawn",
        resource_type="purpose_consent",
        resource_id=consent.id,
        details={"purpose": purpose}
    )
    db.add(audit)
    db.commit()
    db.refresh(consent)
    return consent

@router.get("/privacy/export", response_model=PrivacyExportResponse)
def export_my_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Export all personal data, transcripts, profile fields, and consents for the data subject (DPDP right to data portability).
    """
    ben = db.query(Beneficiary).filter(Beneficiary.user_id == current_user.id).first()
    consents = db.query(PurposeConsent).filter(PurposeConsent.user_id == current_user.id).all()

    payload = {
        "user_account": {
            "id": current_user.id,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "role": current_user.role,
            "created_at": current_user.created_at.isoformat()
        },
        "beneficiary_profile": {
            "name": ben.name if ben else None,
            "education": ben.education if ben else None,
            "current_work": ben.current_work if ben else None,
            "skills": ben.skills if ben else [],
            "location": {
                "district": ben.district if ben else None,
                "block": ben.block if ben else None,
                "village": ben.village if ben else None
            }
        },
        "consents": [
            {
                "purpose": c.purpose,
                "is_granted": c.is_granted,
                "granted_at": c.granted_at.isoformat(),
                "withdrawn_at": c.withdrawn_at.isoformat() if c.withdrawn_at else None
            }
            for c in consents
        ]
    }

    # Record privacy audit
    audit = AuditEvent(
        actor_id=current_user.id,
        actor_role=current_user.role,
        action="export_data",
        resource_type="user",
        resource_id=current_user.id,
        details={"exported_at": datetime.now(timezone.utc).isoformat()}
    )
    db.add(audit)
    db.commit()

    return {
        "user_id": current_user.id,
        "exported_at": datetime.now(timezone.utc),
        "data": payload
    }

@router.delete("/privacy/request-deletion")
def request_data_deletion(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit a right-to-be-forgotten / data deletion request.
    """
    req = PrivacyRequest(
        user_id=current_user.id,
        request_type="delete_account",
        status="completed",
        requested_at=datetime.now(timezone.utc),
        completed_at=datetime.now(timezone.utc)
    )
    db.add(req)

    # Soft delete beneficiary record
    ben = db.query(Beneficiary).filter(Beneficiary.user_id == current_user.id).first()
    if ben:
        ben.is_deleted = True

    current_user.is_active = False

    audit = AuditEvent(
        actor_id=current_user.id,
        actor_role=current_user.role,
        action="deletion_requested",
        resource_type="user",
        resource_id=current_user.id,
        details={"status": "completed"}
    )
    db.add(audit)
    db.commit()

    return {"message": "Data deletion request processed. Account deactivated and data marked for purge.", "user_id": current_user.id}
