from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.training_centre import TrainingCentre
from app.schemas.training_centre import TrainingCentreResponse, TrainingCentreBase
from app.services.geospatial import GeoSpatialService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/training-centres", tags=["Training Centres"])

@router.get("", response_model=List[TrainingCentreResponse])
def list_training_centres(
    district: Optional[str] = None,
    block: Optional[str] = None,
    centre_type: Optional[str] = None,
    course_code: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all affiliated training centres (PMKK, ITI, RSETI, DDU-GKY) with filters.
    """
    query = db.query(TrainingCentre)
    if district:
        query = query.filter(TrainingCentre.district.ilike(f"%{district}%"))
    if block:
        query = query.filter(TrainingCentre.block.ilike(f"%{block}%"))
    if centre_type:
        query = query.filter(TrainingCentre.centre_type == centre_type)
        
    centres = query.all()
    if course_code:
        centres = [c for c in centres if course_code in (c.offered_courses or [])]
    return centres

@router.get("/nearby", response_model=List[TrainingCentreResponse])
def get_nearby_training_centres(
    latitude: float = Query(..., ge=-90.0, le=90.0),
    longitude: float = Query(..., ge=-180.0, le=180.0),
    radius_km: float = Query(default=50.0, gt=0, le=500.0),
    limit: int = Query(default=10, gt=0, le=50),
    course_code: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Find nearby training centres within a radius using Haversine distance calculations.
    """
    nearby = GeoSpatialService.find_nearby_centres(
        db=db,
        lat=latitude,
        lon=longitude,
        radius_km=radius_km,
        limit=limit,
        course_filter=course_code
    )
    return nearby

@router.get("/{id}", response_model=TrainingCentreResponse)
def get_training_centre(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed information for a specific training centre by ID.
    """
    centre = db.query(TrainingCentre).filter(TrainingCentre.id == id).first()
    if not centre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Training centre not found.")
    return centre
