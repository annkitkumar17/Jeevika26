from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.models.beneficiary import Beneficiary
from app.models.consent_privacy import PurposeConsent
from app.schemas.beneficiary import BeneficiaryCreate, BeneficiaryUpdate, BeneficiaryResponse
from app.schemas.sync_notification import LocationConsentRequest
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/beneficiaries", tags=["Beneficiaries"])

@router.get("", response_model=List[BeneficiaryResponse])
def list_beneficiaries(
    skip: int = 0,
    limit: int = Query(default=50, le=100),
    district: Optional[str] = None,
    block: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Beneficiary).filter(Beneficiary.is_deleted == False)
    
    if current_user.role == "beneficiary":
        query = query.filter(Beneficiary.user_id == current_user.id)
    elif current_user.role == "facilitator":
        query = query.filter(
            (Beneficiary.assigned_facilitator_id == current_user.id) |
            (Beneficiary.assigned_facilitator_id == None)
        )
    
    if district:
        query = query.filter(Beneficiary.district.ilike(f"%{district}%"))
    if block:
        query = query.filter(Beneficiary.block.ilike(f"%{block}%"))
    if status:
        query = query.filter(Beneficiary.status == status)
    if search:
        query = query.filter(
            or_(
                Beneficiary.name.ilike(f"%{search}%"),
                Beneficiary.current_work.ilike(f"%{search}%"),
                Beneficiary.village.ilike(f"%{search}%")
            )
        )
        
    beneficiaries = query.offset(skip).limit(limit).all()
    return beneficiaries

@router.post("", response_model=BeneficiaryResponse, status_code=status.HTTP_201_CREATED)
def create_beneficiary(
    beneficiary_in: BeneficiaryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = beneficiary_in.user_id or current_user.id
    
    existing = db.query(Beneficiary).filter(Beneficiary.user_id == user_id, Beneficiary.is_deleted == False).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A beneficiary profile is already associated with this user."
        )

    beneficiary = Beneficiary(
        user_id=user_id,
        name=beneficiary_in.name,
        phone=beneficiary_in.phone,
        gender=beneficiary_in.gender,
        age=beneficiary_in.age,
        preferred_language=beneficiary_in.preferred_language,
        state=beneficiary_in.state,
        district=beneficiary_in.district,
        block=beneficiary_in.block,
        village=beneficiary_in.village,
        latitude=beneficiary_in.latitude,
        longitude=beneficiary_in.longitude,
        education=beneficiary_in.education,
        current_work=beneficiary_in.current_work,
        experience_years=beneficiary_in.experience_years,
        skills=beneficiary_in.skills or [],
        preferences=beneficiary_in.preferences or {},
        consent=beneficiary_in.consent or {},
        status="profiled",
        data_status="demo_seeded"
    )
    db.add(beneficiary)
    db.commit()
    db.refresh(beneficiary)
    return beneficiary

@router.get("/{id}", response_model=BeneficiaryResponse)
def get_beneficiary(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    beneficiary = db.query(Beneficiary).filter(Beneficiary.id == id, Beneficiary.is_deleted == False).first()
    if not beneficiary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Beneficiary profile not found.")
    
    if current_user.role == "beneficiary" and beneficiary.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to this profile.")
        
    return beneficiary

@router.put("/{id}", response_model=BeneficiaryResponse)
def update_beneficiary(
    id: str,
    beneficiary_update: BeneficiaryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    beneficiary = db.query(Beneficiary).filter(Beneficiary.id == id, Beneficiary.is_deleted == False).first()
    if not beneficiary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Beneficiary profile not found.")
        
    if current_user.role == "beneficiary" and beneficiary.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")

    update_data = beneficiary_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(beneficiary, field, value)

    db.commit()
    db.refresh(beneficiary)
    return beneficiary

@router.post("/{id}/location-consent", response_model=BeneficiaryResponse)
def set_location_consent(
    id: str,
    consent_req: LocationConsentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Record explicit permission for approximate GPS location and update coordinates.
    """
    beneficiary = db.query(Beneficiary).filter(Beneficiary.id == id, Beneficiary.is_deleted == False).first()
    if not beneficiary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Beneficiary not found.")

    beneficiary.location_consent_granted = consent_req.granted
    if consent_req.granted and consent_req.latitude and consent_req.longitude:
        beneficiary.latitude = consent_req.latitude
        beneficiary.longitude = consent_req.longitude
        beneficiary.location_accuracy_meters = consent_req.accuracy_meters

    db.commit()
    db.refresh(beneficiary)
    return beneficiary

@router.put("/{id}/location", response_model=BeneficiaryResponse)
def set_manual_location(
    id: str,
    district: str,
    block: str,
    village: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Manual village/block/district selection fallback when GPS is denied or unavailable.
    """
    beneficiary = db.query(Beneficiary).filter(Beneficiary.id == id, Beneficiary.is_deleted == False).first()
    if not beneficiary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Beneficiary not found.")

    beneficiary.district = district
    beneficiary.block = block
    beneficiary.village = village
    db.commit()
    db.refresh(beneficiary)
    return beneficiary

@router.delete("/{id}")
def delete_beneficiary(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    beneficiary = db.query(Beneficiary).filter(Beneficiary.id == id, Beneficiary.is_deleted == False).first()
    if not beneficiary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Beneficiary profile not found.")

    if current_user.role == "beneficiary" and beneficiary.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")

    beneficiary.is_deleted = True
    db.commit()
    return {"message": "Beneficiary profile deleted successfully", "id": id}
