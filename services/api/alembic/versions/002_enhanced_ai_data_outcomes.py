"""Enhanced AI, Verified Data, Case Workflow and Outcomes

Revision ID: 002_enhanced_ai_data_outcomes
Revises: 001_initial_schema
Create Date: 2026-09-29 00:25:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '002_enhanced_ai_data_outcomes'
down_revision: Union[str, None] = '001_initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Data Sources and Imports
    op.create_table(
        'data_sources',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(255), unique=True, nullable=False, index=True),
        sa.Column('owner', sa.String(255), nullable=False),
        sa.Column('base_url', sa.String(500), nullable=True),
        sa.Column('access_method', sa.String(50), default='manual_import', nullable=False),
        sa.Column('licence_or_access_basis', sa.String(255), nullable=False),
        sa.Column('last_sync_at', sa.DateTime(), nullable=True),
        sa.Column('last_success_at', sa.DateTime(), nullable=True),
        sa.Column('sync_status', sa.String(50), default='active', nullable=False),
        sa.Column('version', sa.String(50), default='v1.0.0', nullable=False),
        sa.Column('checksum', sa.String(128), nullable=True),
        sa.Column('meta_info', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'data_import_batches',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('source_id', sa.String(36), nullable=False, index=True),
        sa.Column('import_type', sa.String(50), nullable=False),
        sa.Column('status', sa.String(50), default='pending_review', nullable=False),
        sa.Column('records_count', sa.Integer(), default=0, nullable=False),
        sa.Column('valid_count', sa.Integer(), default=0, nullable=False),
        sa.Column('error_count', sa.Integer(), default=0, nullable=False),
        sa.Column('validation_errors', sa.JSON(), nullable=False),
        sa.Column('payload_snapshot', sa.JSON(), nullable=False),
        sa.Column('imported_by', sa.String(36), nullable=False),
        sa.Column('published_by', sa.String(36), nullable=True),
        sa.Column('published_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 2. Skills and Occupations
    op.create_table(
        'skill_concepts',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('canonical_name', sa.String(255), unique=True, nullable=False, index=True),
        sa.Column('sector', sa.String(100), nullable=False, index=True),
        sa.Column('category', sa.String(100), default='technical', nullable=False),
        sa.Column('aliases', sa.JSON(), nullable=False),
        sa.Column('embedding_id', sa.String(100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'occupation_concepts',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('title', sa.String(255), unique=True, nullable=False, index=True),
        sa.Column('nco_code', sa.String(50), nullable=True),
        sa.Column('sector', sa.String(100), nullable=False),
        sa.Column('is_traditional', sa.String(10), default='no', nullable=False),
        sa.Column('aliases', sa.JSON(), nullable=False),
        sa.Column('associated_skill_ids', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'beneficiary_skill_evidences',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('beneficiary_id', sa.String(36), sa.ForeignKey('beneficiaries.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('skill_name', sa.String(255), nullable=False),
        sa.Column('canonical_skill_id', sa.String(36), nullable=True),
        sa.Column('evidence_type', sa.String(50), default='voice_stated', nullable=False),
        sa.Column('years_experience', sa.Float(), default=1.0, nullable=False),
        sa.Column('proficiency_level', sa.String(50), default='intermediate', nullable=False),
        sa.Column('confidence_score', sa.Float(), default=0.85, nullable=False),
        sa.Column('source_session_id', sa.String(36), nullable=True),
        sa.Column('extracted_snippet', sa.Text(), nullable=True),
        sa.Column('verification_status', sa.String(50), default='unverified', nullable=False),
        sa.Column('verified_by', sa.String(36), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 3. RPL & Gap
    op.create_table(
        'rpl_assessments',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('beneficiary_id', sa.String(36), sa.ForeignKey('beneficiaries.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('target_qualification_id', sa.String(36), sa.ForeignKey('qualifications.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('status', sa.String(50), default='eligible', nullable=False),
        sa.Column('current_skill_evidence', sa.JSON(), nullable=False),
        sa.Column('missing_nos_units', sa.JSON(), nullable=False),
        sa.Column('bridge_modules', sa.JSON(), nullable=False),
        sa.Column('estimated_bridge_hours', sa.Integer(), default=40, nullable=False),
        sa.Column('assessor_id', sa.String(36), nullable=True),
        sa.Column('assessment_date', sa.DateTime(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'skill_gaps',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('beneficiary_id', sa.String(36), sa.ForeignKey('beneficiaries.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('qualification_id', sa.String(36), sa.ForeignKey('qualifications.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('nos_unit_id', sa.String(100), nullable=True),
        sa.Column('gap_type', sa.String(50), default='technical_depth', nullable=False),
        sa.Column('severity', sa.String(50), default='medium', nullable=False),
        sa.Column('evidence', sa.Text(), nullable=True),
        sa.Column('recommended_intervention', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 4. Employers and Opportunities
    op.create_table(
        'employers',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, index=True),
        sa.Column('sector', sa.String(100), nullable=False),
        sa.Column('registration_type', sa.String(50), default='MSME', nullable=False),
        sa.Column('state', sa.String(100), default='Uttar Pradesh', nullable=False),
        sa.Column('district', sa.String(100), default='Lucknow', nullable=False),
        sa.Column('block', sa.String(100), default='Sadar', nullable=False),
        sa.Column('contact_person', sa.String(100), nullable=True),
        sa.Column('contact_phone', sa.String(20), nullable=True),
        sa.Column('is_verified', sa.Boolean(), default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'opportunity_signals',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('sector', sa.String(100), nullable=False, index=True),
        sa.Column('district', sa.String(100), nullable=False, index=True),
        sa.Column('block', sa.String(100), nullable=True),
        sa.Column('demand_level', sa.String(50), default='moderate', nullable=False),
        sa.Column('openings_count', sa.Integer(), nullable=True),
        sa.Column('source_name', sa.String(255), nullable=False),
        sa.Column('evidence_url', sa.String(500), nullable=True),
        sa.Column('observed_date', sa.String(50), nullable=False),
        sa.Column('expiry_date', sa.String(50), nullable=True),
        sa.Column('confidence_score', sa.Float(), default=0.85, nullable=False),
        sa.Column('verification_status', sa.String(50), default='verified', nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'job_opportunities',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('employer_id', sa.String(36), sa.ForeignKey('employers.id', ondelete='SET NULL'), nullable=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('role_type', sa.String(50), default='wage_employment', nullable=False),
        sa.Column('sector', sa.String(100), nullable=False),
        sa.Column('qp_code', sa.String(50), nullable=True),
        sa.Column('district', sa.String(100), default='Lucknow', nullable=False),
        sa.Column('block', sa.String(100), default='Sadar', nullable=False),
        sa.Column('wage_min_inr', sa.Float(), nullable=True),
        sa.Column('wage_max_inr', sa.Float(), nullable=True),
        sa.Column('vacancies', sa.Integer(), default=1, nullable=False),
        sa.Column('source_id', sa.String(36), nullable=True),
        sa.Column('observed_date', sa.String(50), nullable=False),
        sa.Column('expiry_date', sa.String(50), nullable=True),
        sa.Column('verification_status', sa.String(50), default='verified', nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 5. Workflow: Review Tasks, Referrals, Case Events
    op.create_table(
        'review_tasks',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('beneficiary_id', sa.String(36), sa.ForeignKey('beneficiaries.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('assigned_facilitator_id', sa.String(36), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('task_type', sa.String(50), default='recommendation_review', nullable=False),
        sa.Column('priority', sa.String(20), default='normal', nullable=False),
        sa.Column('status', sa.String(50), default='pending', nullable=False),
        sa.Column('trigger_reason', sa.String(255), nullable=False),
        sa.Column('decision', sa.String(50), nullable=True),
        sa.Column('decision_notes', sa.Text(), nullable=True),
        sa.Column('sla_due_at', sa.DateTime(), nullable=True),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'referrals',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('idempotency_key', sa.String(100), unique=True, nullable=True, index=True),
        sa.Column('beneficiary_id', sa.String(36), sa.ForeignKey('beneficiaries.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('target_type', sa.String(50), default='training_centre', nullable=False),
        sa.Column('target_id', sa.String(36), nullable=False),
        sa.Column('pathway_id', sa.String(36), nullable=True),
        sa.Column('facilitator_id', sa.String(36), nullable=False),
        sa.Column('status', sa.String(50), default='dispatched', nullable=False),
        sa.Column('counseling_summary', sa.Text(), nullable=True),
        sa.Column('provider_feedback', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'case_events',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('beneficiary_id', sa.String(36), sa.ForeignKey('beneficiaries.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('actor_id', sa.String(36), nullable=False),
        sa.Column('actor_role', sa.String(50), nullable=False),
        sa.Column('event_type', sa.String(50), nullable=False),
        sa.Column('event_description', sa.String(500), nullable=False),
        sa.Column('event_payload', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 6. Outcomes Breakdown Tables
    op.create_table(
        'training_progress',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('beneficiary_id', sa.String(36), sa.ForeignKey('beneficiaries.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('training_centre_id', sa.String(36), nullable=False),
        sa.Column('qp_code', sa.String(50), nullable=False),
        sa.Column('attendance_percentage', sa.Float(), default=0.0, nullable=False),
        sa.Column('modules_completed', sa.Integer(), default=0, nullable=False),
        sa.Column('assessment_status', sa.String(50), default='in_training', nullable=False),
        sa.Column('certification_number', sa.String(100), nullable=True),
        sa.Column('dropout_reason', sa.String(255), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'employment_outcomes',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('beneficiary_id', sa.String(36), sa.ForeignKey('beneficiaries.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('employer_name', sa.String(255), nullable=False),
        sa.Column('role_title', sa.String(255), nullable=False),
        sa.Column('joining_date', sa.String(50), nullable=False),
        sa.Column('monthly_wage_inr', sa.Float(), nullable=True),
        sa.Column('verification_method', sa.String(50), default='facilitator_call', nullable=False),
        sa.Column('retention_status_30_days', sa.String(50), default='pending', nullable=False),
        sa.Column('retention_status_90_days', sa.String(50), default='pending', nullable=False),
        sa.Column('retention_status_180_days', sa.String(50), default='pending', nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'enterprise_outcomes',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('beneficiary_id', sa.String(36), sa.ForeignKey('beneficiaries.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('enterprise_name', sa.String(255), nullable=False),
        sa.Column('activity_type', sa.String(255), nullable=False),
        sa.Column('udyam_or_shg_id', sa.String(100), nullable=True),
        sa.Column('credit_scheme_linked', sa.String(100), nullable=True),
        sa.Column('loan_amount_sanctioned_inr', sa.Float(), nullable=True),
        sa.Column('monthly_estimated_revenue_inr', sa.Float(), nullable=True),
        sa.Column('operational_status', sa.String(50), default='active', nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'follow_ups',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('beneficiary_id', sa.String(36), sa.ForeignKey('beneficiaries.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('milestone', sa.String(20), nullable=False),
        sa.Column('scheduled_date', sa.String(50), nullable=False),
        sa.Column('status', sa.String(50), default='scheduled', nullable=False),
        sa.Column('assigned_facilitator_id', sa.String(36), nullable=True),
        sa.Column('outcome_summary', sa.Text(), nullable=True),
        sa.Column('is_retained', sa.Boolean(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 7. Consent, Privacy & Audit
    op.create_table(
        'purpose_consents',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('purpose', sa.String(100), nullable=False, index=True),
        sa.Column('is_granted', sa.Boolean(), default=True, nullable=False),
        sa.Column('version', sa.String(20), default='v1.0', nullable=False),
        sa.Column('consent_text', sa.Text(), nullable=False),
        sa.Column('language', sa.String(10), default='hi', nullable=False),
        sa.Column('granted_at', sa.DateTime(), nullable=False),
        sa.Column('withdrawn_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'privacy_requests',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('request_type', sa.String(50), nullable=False),
        sa.Column('status', sa.String(50), default='pending', nullable=False),
        sa.Column('requested_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('export_payload', sa.JSON(), nullable=True),
    )

    op.create_table(
        'audit_events',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('actor_id', sa.String(36), nullable=False, index=True),
        sa.Column('actor_role', sa.String(50), nullable=False),
        sa.Column('action', sa.String(100), nullable=False, index=True),
        sa.Column('resource_type', sa.String(100), nullable=False),
        sa.Column('resource_id', sa.String(36), nullable=True),
        sa.Column('ip_address', sa.String(50), nullable=True),
        sa.Column('details', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 8. Notifications, Sync & Security tokens
    op.create_table(
        'notifications',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('channel', sa.String(50), default='in_app', nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('status', sa.String(50), default='queued', nullable=False),
        sa.Column('provider_response', sa.JSON(), nullable=True),
        sa.Column('read_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'sync_events',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('idempotency_key', sa.String(100), unique=True, nullable=False, index=True),
        sa.Column('device_id', sa.String(100), nullable=True),
        sa.Column('entity_type', sa.String(50), nullable=False),
        sa.Column('entity_id', sa.String(36), nullable=False),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('payload', sa.JSON(), nullable=False),
        sa.Column('sync_status', sa.String(50), default='applied', nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'token_blocklist',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('jti', sa.String(100), unique=True, nullable=False, index=True),
        sa.Column('revoked_at', sa.DateTime(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'password_reset_tokens',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('token', sa.String(100), unique=True, nullable=False, index=True),
        sa.Column('is_used', sa.Boolean(), default=False, nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('password_reset_tokens')
    op.drop_table('token_blocklist')
    op.drop_table('sync_events')
    op.drop_table('notifications')
    op.drop_table('audit_events')
    op.drop_table('privacy_requests')
    op.drop_table('purpose_consents')
    op.drop_table('follow_ups')
    op.drop_table('enterprise_outcomes')
    op.drop_table('employment_outcomes')
    op.drop_table('training_progress')
    op.drop_table('case_events')
    op.drop_table('referrals')
    op.drop_table('review_tasks')
    op.drop_table('job_opportunities')
    op.drop_table('opportunity_signals')
    op.drop_table('employers')
    op.drop_table('skill_gaps')
    op.drop_table('rpl_assessments')
    op.drop_table('beneficiary_skill_evidences')
    op.drop_table('occupation_concepts')
    op.drop_table('skill_concepts')
    op.drop_table('data_import_batches')
    op.drop_table('data_sources')
