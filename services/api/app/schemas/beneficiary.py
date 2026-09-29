from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class BeneficiaryLocation(BaseModel):
    state: str = "Uttar Pradesh"
    district: str = "Lucknow"
    block: str = "Sadar"
    village: str = "Rampur Demo"
    latitude: Optional[float] = 26.8467
    longitude: Optional[float] = 80.9462
    data_status: str = "demo_seeded"

class BeneficiaryPreferences(BaseModel):
    employment_type: str = "self_employment"  # wage_employment, self_employment, either
    max_travel_km: int = 25
    migration: bool = False

class BeneficiaryConsent(BaseModel):
    profile_creation: bool = True
    recommendations: bool = True
    follow_up: bool = True

class BeneficiaryBase(BaseModel):
    name: str
    phone: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    preferred_language: str = "hi"
    
    state: str = "Uttar Pradesh"
    district: str = "Lucknow"
    block: str = "Sadar"
    village: str = "Rampur Demo"
    latitude: Optional[float] = 26.8467
    longitude: Optional[float] = 80.9462
    
    education: Optional[str] = None
    current_work: Optional[str] = None
    experience_years: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    preferences: Dict[str, Any] = Field(default_factory=dict)
    consent: Dict[str, Any] = Field(default_factory=dict)

class BeneficiaryCreate(BeneficiaryBase):
    user_id: Optional[str] = None

class BeneficiaryUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    preferred_language: Optional[str] = None
    
    state: Optional[str] = None
    district: Optional[str] = None
    block: Optional[str] = None
    village: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    education: Optional[str] = None
    current_work: Optional[str] = None
    experience_years: Optional[str] = None
    skills: Optional[List[str]] = None
    preferences: Optional[Dict[str, Any]] = None
    consent: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    enrolled_pathway_id: Optional[str] = None

class BeneficiaryResponse(BeneficiaryBase):
    id: str
    user_id: Optional[str]
    status: str
    enrolled_pathway_id: Optional[str]
    data_status: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
