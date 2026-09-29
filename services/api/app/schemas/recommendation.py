from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.schemas.qualification import QualificationResponse

class RecommendationGenerateRequest(BaseModel):
    beneficiary_id: str
    force_refresh: bool = False

class RecommendationSelectRequest(BaseModel):
    pathway_id: str

class RecommendationResponse(BaseModel):
    id: str
    beneficiary_id: str
    qualification_id: str
    rank: int
    match_score: float
    
    score_breakdown: Dict[str, float] = Field(default_factory=dict)
    fit_reason: str
    fit_details: List[str] = Field(default_factory=list) # why_this_fits
    skill_gaps: List[str] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)
    unknowns: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list)
    
    human_review_required: bool = False
    human_validated: bool = False
    
    local_opportunity_signal: str
    nearest_centre_id: Optional[str] = None
    nearest_centre_distance_km: Optional[float] = None
    rpl_eligible: bool = True
    risk_factor: Optional[str] = None
    status: str
    created_at: datetime
    qualification: Optional[QualificationResponse] = None

    model_config = ConfigDict(from_attributes=True)
