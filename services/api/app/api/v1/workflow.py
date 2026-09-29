from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.core.database import get_db
from app.models.workflow import ReviewTask, Referral, CaseEvent
from app.models.beneficiary import Beneficiary
from app.models.outcome import FollowUp, TrainingProgress, EmploymentOutcome, EnterpriseOutcome
from app.schemas.workflow import (
    ReviewTaskCreate,
    ReviewTaskDecision,
    ReviewTaskResponse,
    ReferralCreate,
    ReferralProgressUpdate,
    ReferralResponse,
    CaseEventResponse,
    TrainingProgressCreate,
    TrainingProgressResponse,
    EmploymentOutcomeCreate,
    EmploymentOutcomeResponse,
    EnterpriseOutcomeCreate,
    EnterpriseOutcomeResponse,
    FollowUpResponse,
    FollowUpComplete,
)
from app.api.deps import get_current_user, require_facilitator_or_admin
from app.models.user import User

router = APIRouter(prefix="", tags=["Workflow & Reviews"])

# 1. Review Tasks
@router.get("/reviews/tasks", response_model=List[ReviewTaskResponse])
def list_review_tasks(
    status_filter: Optional[str] = None,
    priority_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_facilitator_or_admin)
):
    """
    List human-in-the-loop review tasks assigned to the facilitator or district.
    """
    query = db.query(ReviewTask)
    if current_user.role == "facilitator":
        query = query.filter(
            (ReviewTask.assigned_facilitator_id == current_user.id) |
            (ReviewTask.assigned_facilitator_id == None)
        )
    if status_filter:
        query = query.filter(ReviewTask.status == status_filter)
    if priority_filter:
        query = query.filter(ReviewTask.priority == priority_filter)
    return query.all()

@router.post("/reviews/tasks", response_model=ReviewTaskResponse, status_code=status.HTTP_201_CREATED)
def create_review_task(
    task_in: ReviewTaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_facilitator_or_admin)
):
    """
    Create a new manual review task for a case.
    """
    task = ReviewTask(
        beneficiary_id=task_in.beneficiary_id,
        assigned_facilitator_id=task_in.assigned_facilitator_id or current_user.id,
        task_type=task_in.task_type,
        priority=task_in.priority,
        trigger_reason=task_in.trigger_reason,
        status="pending"
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.put("/reviews/tasks/{id}/decision", response_model=ReviewTaskResponse)
def submit_review_decision(
    id: str,
    decision_in: ReviewTaskDecision,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_facilitator_or_admin)
):
    """
    Submit facilitator approval, modification, or rejection decision for a review task.
    """
    task = db.query(ReviewTask).filter(ReviewTask.id == id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review task not found.")

    task.decision = decision_in.decision
    task.decision_notes = decision_in.decision_notes
    task.status = "resolved" if decision_in.decision == "approved" else "modified"
    task.resolved_at = datetime.now(timezone.utc)

    # Log case event
    event = CaseEvent(
        beneficiary_id=task.beneficiary_id,
        actor_id=current_user.id,
        actor_role=current_user.role,
        event_type="human_review_decision",
        event_description=f"Facilitator {current_user.full_name or current_user.email} submitted decision: {decision_in.decision}",
        event_payload={"task_id": task.id, "decision": decision_in.decision, "notes": decision_in.decision_notes}
    )
    db.add(event)
    db.commit()
    db.refresh(task)
    return task

# 2. Referrals
@router.post("/referrals", response_model=ReferralResponse, status_code=status.HTTP_201_CREATED)
def create_referral(
    referral_in: ReferralCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_facilitator_or_admin)
):
    """
    Create a formal referral for a beneficiary to a training centre, employer, or enterprise scheme.
    Supports idempotency key to prevent duplicate dispatches.
    """
    if referral_in.idempotency_key:
        existing = db.query(Referral).filter(Referral.idempotency_key == referral_in.idempotency_key).first()
        if existing:
            return existing

    referral = Referral(
        idempotency_key=referral_in.idempotency_key,
        beneficiary_id=referral_in.beneficiary_id,
        target_type=referral_in.target_type,
        target_id=referral_in.target_id,
        pathway_id=referral_in.pathway_id,
        facilitator_id=current_user.id,
        counseling_summary=referral_in.counseling_summary,
        status="dispatched"
    )
    db.add(referral)

    # Auto-schedule 30/90/180-day follow-ups
    for milestone, days in [("30_day", 30), ("90_day", 90), ("180_day", 180)]:
        f_up = FollowUp(
            beneficiary_id=referral_in.beneficiary_id,
            milestone=milestone,
            scheduled_date=f"+{days} days from referral",
            status="scheduled",
            assigned_facilitator_id=current_user.id
        )
        db.add(f_up)

    # Case event
    event = CaseEvent(
        beneficiary_id=referral_in.beneficiary_id,
        actor_id=current_user.id,
        actor_role=current_user.role,
        event_type="referral_dispatched",
        event_description=f"Candidate referred to {referral_in.target_type} ({referral_in.target_id})",
        event_payload={"target_type": referral_in.target_type, "target_id": referral_in.target_id}
    )
    db.add(event)

    db.commit()
    db.refresh(referral)
    return referral

@router.get("/referrals", response_model=List[ReferralResponse])
def list_referrals(
    beneficiary_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List candidate referrals.
    """
    query = db.query(Referral)
    if current_user.role == "beneficiary":
        ben = db.query(Beneficiary).filter(Beneficiary.user_id == current_user.id).first()
        if ben:
            query = query.filter(Referral.beneficiary_id == ben.id)
    elif beneficiary_id:
        query = query.filter(Referral.beneficiary_id == beneficiary_id)
    return query.all()

@router.put("/referrals/{id}/progress", response_model=ReferralResponse)
def update_referral_progress(
    id: str,
    progress_in: ReferralProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_facilitator_or_admin)
):
    """
    Update referral progress (candidate contacted, enrolled, completed).
    """
    referral = db.query(Referral).filter(Referral.id == id).first()
    if not referral:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Referral not found.")

    referral.status = progress_in.status
    if progress_in.provider_feedback:
        referral.provider_feedback = progress_in.provider_feedback

    event = CaseEvent(
        beneficiary_id=referral.beneficiary_id,
        actor_id=current_user.id,
        actor_role=current_user.role,
        event_type="referral_status_update",
        event_description=f"Referral status updated to {progress_in.status}",
        event_payload={"status": progress_in.status, "feedback": progress_in.provider_feedback}
    )
    db.add(event)
    db.commit()
    db.refresh(referral)
    return referral

# 3. Case Timeline
@router.get("/cases/{beneficiary_id}/timeline", response_model=List[CaseEventResponse])
def get_case_timeline(
    beneficiary_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get the immutable audit trail and historical timeline of all events for a beneficiary case.
    """
    if current_user.role == "beneficiary":
        ben = db.query(Beneficiary).filter(Beneficiary.user_id == current_user.id).first()
        if not ben or ben.id != beneficiary_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")

    events = db.query(CaseEvent).filter(CaseEvent.beneficiary_id == beneficiary_id).order_by(CaseEvent.created_at.asc()).all()
    return events

# 4. Outcomes & Milestone Tracking
@router.post("/outcomes/training-progress", response_model=TrainingProgressResponse, status_code=status.HTTP_201_CREATED)
def create_training_progress(
    progress_in: TrainingProgressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_facilitator_or_admin)
):
    """
    Log training centre attendance, module completion, and assessment results.
    """
    tp = TrainingProgress(
        beneficiary_id=progress_in.beneficiary_id,
        training_centre_id=progress_in.training_centre_id,
        qp_code=progress_in.qp_code,
        attendance_percentage=progress_in.attendance_percentage,
        modules_completed=progress_in.modules_completed,
        assessment_status=progress_in.assessment_status,
        certification_number=progress_in.certification_number,
        dropout_reason=progress_in.dropout_reason,
    )
    db.add(tp)
    
    event = CaseEvent(
        beneficiary_id=progress_in.beneficiary_id,
        actor_id=current_user.id,
        actor_role=current_user.role,
        event_type="training_progress_logged",
        event_description=f"Training attendance: {progress_in.attendance_percentage}%, status: {progress_in.assessment_status}",
        event_payload={"qp_code": progress_in.qp_code, "assessment": progress_in.assessment_status}
    )
    db.add(event)
    db.commit()
    db.refresh(tp)
    return tp

@router.post("/outcomes/employment", response_model=EmploymentOutcomeResponse, status_code=status.HTTP_201_CREATED)
def create_employment_outcome(
    emp_in: EmploymentOutcomeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_facilitator_or_admin)
):
    """
    Record placement/wage employment outcome with voluntary wage reporting.
    """
    emp = EmploymentOutcome(
        beneficiary_id=emp_in.beneficiary_id,
        employer_name=emp_in.employer_name,
        role_title=emp_in.role_title,
        joining_date=emp_in.joining_date,
        monthly_wage_inr=emp_in.monthly_wage_inr,
        verification_method=emp_in.verification_method,
        retention_status_30_days="verified"
    )
    db.add(emp)

    event = CaseEvent(
        beneficiary_id=emp_in.beneficiary_id,
        actor_id=current_user.id,
        actor_role=current_user.role,
        event_type="employment_placed",
        event_description=f"Placed as {emp_in.role_title} at {emp_in.employer_name}",
        event_payload={"employer": emp_in.employer_name, "role": emp_in.role_title}
    )
    db.add(event)
    db.commit()
    db.refresh(emp)
    return emp

@router.post("/outcomes/enterprise", response_model=EnterpriseOutcomeResponse, status_code=status.HTTP_201_CREATED)
def create_enterprise_outcome(
    ent_in: EnterpriseOutcomeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_facilitator_or_admin)
):
    """
    Record micro-enterprise launch with MUDRA/PM-FME credit linkage.
    """
    ent = EnterpriseOutcome(
        beneficiary_id=ent_in.beneficiary_id,
        enterprise_name=ent_in.enterprise_name,
        activity_type=ent_in.activity_type,
        udyam_or_shg_id=ent_in.udyam_or_shg_id,
        credit_scheme_linked=ent_in.credit_scheme_linked,
        loan_amount_sanctioned_inr=ent_in.loan_amount_sanctioned_inr,
        monthly_estimated_revenue_inr=ent_in.monthly_estimated_revenue_inr,
        operational_status="active"
    )
    db.add(ent)

    event = CaseEvent(
        beneficiary_id=ent_in.beneficiary_id,
        actor_id=current_user.id,
        actor_role=current_user.role,
        event_type="enterprise_launched",
        event_description=f"Launched enterprise {ent_in.enterprise_name} ({ent_in.activity_type})",
        event_payload={"enterprise": ent_in.enterprise_name, "scheme": ent_in.credit_scheme_linked}
    )
    db.add(event)
    db.commit()
    db.refresh(ent)
    return ent

@router.get("/outcomes/follow-ups", response_model=List[FollowUpResponse])
def list_follow_ups(
    beneficiary_id: Optional[str] = None,
    milestone: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List 30/90/180-day follow-up schedules.
    """
    query = db.query(FollowUp)
    if beneficiary_id:
        query = query.filter(FollowUp.beneficiary_id == beneficiary_id)
    if milestone:
        query = query.filter(FollowUp.milestone == milestone)
    return query.all()

@router.put("/outcomes/follow-ups/{id}/complete", response_model=FollowUpResponse)
def complete_follow_up(
    id: str,
    comp_in: FollowUpComplete,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_facilitator_or_admin)
):
    """
    Log completion of 30/90/180-day follow-up check-in.
    """
    fup = db.query(FollowUp).filter(FollowUp.id == id).first()
    if not fup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Follow-up not found.")
    
    fup.status = comp_in.status
    fup.outcome_summary = comp_in.outcome_summary
    fup.is_retained = comp_in.is_retained
    fup.completed_at = datetime.now(timezone.utc)
    
    event = CaseEvent(
        beneficiary_id=fup.beneficiary_id,
        actor_id=current_user.id,
        actor_role=current_user.role,
        event_type="follow_up_completed",
        event_description=f"Completed {fup.milestone} follow-up check-in",
        event_payload={"milestone": fup.milestone, "is_retained": comp_in.is_retained}
    )
    db.add(event)
    db.commit()
    db.refresh(fup)
    return fup

