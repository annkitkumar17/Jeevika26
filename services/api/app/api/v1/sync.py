from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.core.database import get_db
from app.models.notification_sync import SyncEvent, Notification
from app.schemas.sync_notification import SyncEventCreate, SyncEventResponse, NotificationResponse
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="", tags=["Offline Sync & Notifications"])

@router.post("/sync/events", response_model=SyncEventResponse, status_code=status.HTTP_201_CREATED)
def sync_offline_event(
    event_in: SyncEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Ingest offline field-worker application synchronization events with idempotency keys.
    """
    existing = db.query(SyncEvent).filter(SyncEvent.idempotency_key == event_in.idempotency_key).first()
    if existing:
        return existing

    event = SyncEvent(
        idempotency_key=event_in.idempotency_key,
        device_id=event_in.device_id,
        entity_type=event_in.entity_type,
        entity_id=event_in.entity_id,
        action=event_in.action,
        payload=event_in.payload,
        sync_status="applied",
        created_at=datetime.now(timezone.utc)
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.get("/notifications", response_model=List[NotificationResponse])
def get_user_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get in-app notifications for the authenticated user.
    """
    notifications = db.query(Notification).filter(Notification.user_id == current_user.id).order_by(Notification.created_at.desc()).all()
    return notifications
