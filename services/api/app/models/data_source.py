import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text, JSON, Integer
from app.core.database import Base

class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), unique=True, nullable=False, index=True) # e.g. "NQR Official NSQF Register", "PMKK Centre Registry"
    owner = Column(String(255), nullable=False) # e.g. "NCVET / MSDE", "NSDC"
    base_url = Column(String(500), nullable=True)
    access_method = Column(String(50), default="manual_import", nullable=False) # official_api, approved_export, manual_import
    licence_or_access_basis = Column(String(255), default="Government Open Data / PM-AJAY authorized", nullable=False)
    
    last_sync_at = Column(DateTime, nullable=True)
    last_success_at = Column(DateTime, nullable=True)
    sync_status = Column(String(50), default="active", nullable=False) # active, stale, sync_failed, pending_approval
    version = Column(String(50), default="v1.0.0", nullable=False)
    checksum = Column(String(128), nullable=True)
    
    meta_info = Column(JSON, default=dict, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class DataImportBatch(Base):
    __tablename__ = "data_import_batches"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String(36), nullable=False, index=True)
    import_type = Column(String(50), nullable=False) # qualifications, training_centres, opportunities
    status = Column(String(50), default="pending_review", nullable=False) # pending_review, validated, published, rolled_back, rejected
    
    records_count = Column(Integer, default=0, nullable=False)
    valid_count = Column(Integer, default=0, nullable=False)
    error_count = Column(Integer, default=0, nullable=False)
    
    validation_errors = Column(JSON, default=list, nullable=False)
    payload_snapshot = Column(JSON, default=list, nullable=False)
    
    imported_by = Column(String(36), nullable=False)
    published_by = Column(String(36), nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
