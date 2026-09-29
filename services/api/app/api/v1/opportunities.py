from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.opportunity import OpportunitySignal, JobOpportunity
from app.schemas.opportunity import OpportunitySignalResponse, JobOpportunityResponse
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/opportunities", tags=["Local Market Opportunities"])

@router.get("/signals", response_model=List[OpportunitySignalResponse])
def list_opportunity_signals(
    district: Optional[str] = None,
    sector: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List verified district-level opportunity signals.
    """
    query = db.query(OpportunitySignal)
    if district:
        query = query.filter(OpportunitySignal.district.ilike(f"%{district}%"))
    if sector:
        query = query.filter(OpportunitySignal.sector.ilike(f"%{sector}%"))
    return query.all()

@router.get("/nearby", response_model=List[JobOpportunityResponse])
def get_nearby_job_opportunities(
    district: Optional[str] = Query(default="Lucknow"),
    sector: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List local verified employer job listings with wage ranges and vacancies.
    """
    query = db.query(JobOpportunity).filter(JobOpportunity.verification_status == "verified")
    if district:
        query = query.filter(JobOpportunity.district.ilike(f"%{district}%"))
    if sector:
        query = query.filter(JobOpportunity.sector.ilike(f"%{sector}%"))
    return query.all()
