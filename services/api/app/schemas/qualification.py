from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any
from datetime import datetime

class QualificationBase(BaseModel):
    qp_code: str
    title: str
    sector: str
    nsqf_level: int
    description: Optional[str] = None
    entry_requirements: Optional[str] = None
    duration_hours: int = 300
    curriculum_modules: List[str] = Field(default_factory=list)
    potential_job_roles: List[str] = Field(default_factory=list)
    average_salary_range: Optional[str] = None

class QualificationCreate(QualificationBase):
    pass

class QualificationResponse(QualificationBase):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
