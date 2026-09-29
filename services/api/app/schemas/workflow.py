from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class ReviewTaskCreate(BaseModel):
    beneficiary_id: str
    task_type: str = "recommendation_review"
    priority: str = "normal"
    trigger_reason: str
    assigned_facilitator_id: Optional[str] = None

class ReviewTaskDecision(BaseModel):
    decision: str # approved, modified, rejected, referred
    decision_notes: Optional[str] = None

class ReviewTaskResponse(BaseModel):
    id: str
    beneficiary_id: str
    assigned_facilitator_id: Optional[str]
    task_type: str
    priority: str
    status: str
    trigger_reason: str
    decision: Optional[str]
    decision_notes: Optional[str]
    sla_due_at: Optional[datetime]
    resolved_at: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ReferralCreate(BaseModel):
    idempotency_key: Optional[str] = None
    beneficiary_id: str
    target_type: str = "training_centre" # training_centre, employer, enterprise_scheme, rpl_assessor
    target_id: str
    pathway_id: Optional[str] = None
    counseling_summary: Optional[str] = None

class ReferralProgressUpdate(BaseModel):
    status: str # dispatched, accepted, candidate_contacted, enrolled, rejected, completed
    provider_feedback: Optional[str] = None

class ReferralResponse(BaseModel):
    id: str
    idempotency_key: Optional[str]
    beneficiary_id: str
    target_type: str
    target_id: str
    pathway_id: Optional[str]
    facilitator_id: str
    status: str
    counseling_summary: Optional[str]
    provider_feedback: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CaseEventResponse(BaseModel):
    id: str
    beneficiary_id: str
    actor_id: str
    actor_role: str
    event_type: str
    event_description: str
    event_payload: Dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TrainingProgressCreate(BaseModel):
    idempotency_key: Optional[str] = None
    beneficiary_id: str
    training_centre_id: str
    qp_code: str
    attendance_percentage: float = 0.0
    modules_completed: int = 0
    assessment_status: str = "in_training"
    certification_number: Optional[str] = None
    dropout_reason: Optional[str] = None

class TrainingProgressResponse(BaseModel):
    id: str
    beneficiary_id: str
    training_centre_id: str
    qp_code: str
    attendance_percentage: float
    modules_completed: int
    assessment_status: str
    certification_number: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class EmploymentOutcomeCreate(BaseModel):
    idempotency_key: Optional[str] = None
    beneficiary_id: str
    employer_name: str
    role_title: str
    joining_date: str
    monthly_wage_inr: Optional[float] = None
    verification_method: str = "facilitator_call"

class EmploymentOutcomeResponse(BaseModel):
    id: str
    beneficiary_id: str
    employer_name: str
    role_title: str
    joining_date: str
    monthly_wage_inr: Optional[float]
    verification_method: str
    retention_status_30_days: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class EnterpriseOutcomeCreate(BaseModel):
    idempotency_key: Optional[str] = None
    beneficiary_id: str
    enterprise_name: str
    activity_type: str
    udyam_or_shg_id: Optional[str] = None
    credit_scheme_linked: Optional[str] = "PM-FME / PM-MUDRA"
    loan_amount_sanctioned_inr: Optional[float] = None
    monthly_estimated_revenue_inr: Optional[float] = None

class EnterpriseOutcomeResponse(BaseModel):
    id: str
    beneficiary_id: str
    enterprise_name: str
    activity_type: str
    udyam_or_shg_id: Optional[str]
    loan_amount_sanctioned_inr: Optional[float]
    operational_status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class FollowUpResponse(BaseModel):
    id: str
    beneficiary_id: str
    milestone: str
    scheduled_date: str
    status: str
    assigned_facilitator_id: Optional[str]
    outcome_summary: Optional[str]
    is_retained: Optional[bool]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class FollowUpComplete(BaseModel):
    status: str = "completed"
    outcome_summary: Optional[str] = None
    is_retained: Optional[bool] = True
