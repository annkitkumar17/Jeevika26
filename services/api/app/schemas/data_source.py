from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class DataSourceCreate(BaseModel):
    name: str
    owner: str
    base_url: Optional[str] = None
    access_method: str = "manual_import" # official_api, approved_export, manual_import
    licence_or_access_basis: str = "Government Open Data / PM-AJAY authorized"
    version: str = "v1.0.0"
    checksum: Optional[str] = None
    meta_info: Dict[str, Any] = Field(default_factory=dict)

class DataSourceResponse(DataSourceCreate):
    id: str
    last_sync_at: Optional[datetime] = None
    last_success_at: Optional[datetime] = None
    sync_status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DataImportValidateRequest(BaseModel):
    source_id: str
    import_type: str # qualifications, training_centres, opportunities
    records: List[Dict[str, Any]]

class DataImportValidateResponse(BaseModel):
    batch_id: str
    import_type: str
    status: str
    records_count: int
    valid_count: int
    error_count: int
    errors: List[Dict[str, Any]]
    preview: List[Dict[str, Any]]
