from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class TrainingCentreBase(BaseModel):
    centre_code: str
    name: str
    centre_type: str = "PMKK"
    address: str
    state: str = "Uttar Pradesh"
    district: str = "Lucknow"
    block: str = "Sadar"
    pincode: Optional[str] = None
    latitude: float
    longitude: float
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    offered_courses: List[str] = Field(default_factory=list)
    batch_status: str = "Admissions Open"
    next_batch_date: Optional[str] = None

class TrainingCentreNearbyRequest(BaseModel):
    latitude: float
    longitude: float
    radius_km: float = 50.0
    limit: int = 10

class TrainingCentreResponse(TrainingCentreBase):
    id: str
    distance_km: Optional[float] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
