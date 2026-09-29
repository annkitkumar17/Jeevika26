from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.recommendation import Recommendation
from app.models.beneficiary import Beneficiary
from app.schemas.recommendation import (
    RecommendationGenerateRequest,
    RecommendationSelectRequest,
    RecommendationResponse,
)
from app.services.recommendation_engine import RecommendationEngine
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("", response_model=List[RecommendationResponse])
def get_recommendations(
    beneficiary_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get ranked livelihood recommendations for a beneficiary.
    """
    target_beneficiary_id = beneficiary_id
    if not target_beneficiary_id and current_user.role == "beneficiary":
        beneficiary = db.query(Beneficiary).filter(Beneficiary.user_id == current_user.id).first()
        if beneficiary:
            target_beneficiary_id = beneficiary.id
            
    if not target_beneficiary_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="beneficiary_id query parameter is required."
        )

    recommendations = (
        db.query(Recommendation)
        .filter(Recommendation.beneficiary_id == target_beneficiary_id)
        .order_by(Recommendation.rank)
        .all()
    )

    # If none generated yet, auto-generate from profile
    if not recommendations:
        recommendations = RecommendationEngine.generate_recommendations(db, target_beneficiary_id)

    return recommendations

@router.post("/generate", response_model=List[RecommendationResponse])
def generate_recommendations(
    request: RecommendationGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Trigger the NSQF recommendation engine to generate or refresh 3 tailored livelihood pathways.
    """
    beneficiary = db.query(Beneficiary).filter(Beneficiary.id == request.beneficiary_id).first()
    if not beneficiary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Beneficiary profile not found.")

    recommendations = RecommendationEngine.generate_recommendations(
        db, request.beneficiary_id, force_refresh=request.force_refresh
    )
    return recommendations

@router.put("/{id}/select", response_model=RecommendationResponse)
def select_recommendation(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Select an NSQF livelihood pathway as the beneficiary's active skilling goal.
    """
    recommendation = db.query(Recommendation).filter(Recommendation.id == id).first()
    if not recommendation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found.")

    # Mark this recommendation as selected
    recommendation.status = "selected"

    # Update beneficiary's active enrolled pathway
    beneficiary = db.query(Beneficiary).filter(Beneficiary.id == recommendation.beneficiary_id).first()
    if beneficiary:
        beneficiary.enrolled_pathway_id = recommendation.id
        beneficiary.status = "enrolled"

    db.commit()
    db.refresh(recommendation)
    return recommendation
