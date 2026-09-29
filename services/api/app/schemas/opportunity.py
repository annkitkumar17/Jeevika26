from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class OpportunitySignalResponse(BaseModel):
    id: str
    sector: str
    district: str
    block: Optional[str]
    demand_level: str
    openings_count: Optional[int]
    source_name: str
    evidence_url: Optional[str]
    observed_date: str
    confidence_score: float
    verification_status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class JobOpportunityResponse(BaseModel):
    id: str
    employer_id: Optional[str]
    title: str
    role_type: str
    sector: str
    qp_code: Optional[str]
    district: str
    block: str
    wage_min_inr: Optional[float]
    wage_max_inr: Optional[float]
    vacancies: int
    observed_date: str
    verification_status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
