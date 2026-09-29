from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class RPLAssessmentResponse(BaseModel):
    id: str
    beneficiary_id: str
    target_qualification_id: str
    status: str
    current_skill_evidence: List[Dict[str, Any]]
    missing_nos_units: List[Dict[str, Any]]
    bridge_modules: List[Dict[str, Any]]
    estimated_bridge_hours: int
    assessor_id: Optional[str]
    notes: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SkillGapResponse(BaseModel):
    id: str
    beneficiary_id: str
    qualification_id: str
    nos_unit_id: Optional[str]
    gap_type: str
    severity: str
    evidence: Optional[str]
    recommended_intervention: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
