"""Initial schema creation

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-09-28 23:55:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, index=True, nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('role', sa.String(50), nullable=False, default='beneficiary'),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 2. Qualifications table
    op.create_table(
        'qualifications',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('qp_code', sa.String(50), unique=True, index=True, nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('sector', sa.String(100), nullable=False),
        sa.Column('nsqf_level', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('entry_requirements', sa.String(255), nullable=True),
        sa.Column('duration_hours', sa.Integer(), default=300, nullable=False),
        sa.Column('curriculum_modules', sa.JSON(), nullable=False),
        sa.Column('potential_job_roles', sa.JSON(), nullable=False),
        sa.Column('average_salary_range', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 3. Training Centres table
    op.create_table(
        'training_centres',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('centre_code', sa.String(50), unique=True, index=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('centre_type', sa.String(100), default='PMKK', nullable=False),
        sa.Column('address', sa.Text(), nullable=False),
        sa.Column('state', sa.String(100), default='Uttar Pradesh', nullable=False),
        sa.Column('district', sa.String(100), default='Lucknow', nullable=False),
        sa.Column('block', sa.String(100), default='Sadar', nullable=False),
        sa.Column('pincode', sa.String(10), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('contact_person', sa.String(100), nullable=True),
        sa.Column('contact_phone', sa.String(20), nullable=True),
        sa.Column('offered_courses', sa.JSON(), nullable=False),
        sa.Column('batch_status', sa.String(50), default='Admissions Open', nullable=False),
        sa.Column('next_batch_date', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 4. Beneficiaries table
    op.create_table(
        'beneficiaries',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True, unique=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('gender', sa.String(20), nullable=True),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('preferred_language', sa.String(10), default='hi', nullable=False),
        sa.Column('state', sa.String(100), default='Uttar Pradesh', nullable=False),
        sa.Column('district', sa.String(100), default='Lucknow', nullable=False),
        sa.Column('block', sa.String(100), default='Sadar', nullable=False),
        sa.Column('village', sa.String(100), default='Rampur Demo', nullable=False),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('education', sa.String(100), nullable=True),
        sa.Column('current_work', sa.String(255), nullable=True),
        sa.Column('experience_years', sa.String(50), nullable=True),
        sa.Column('skills', sa.JSON(), nullable=False),
        sa.Column('preferences', sa.JSON(), nullable=False),
        sa.Column('consent', sa.JSON(), nullable=False),
        sa.Column('status', sa.String(50), default='profiled', nullable=False),
        sa.Column('enrolled_pathway_id', sa.String(36), nullable=True),
        sa.Column('data_status', sa.String(50), default='demo_seeded', nullable=False),
        sa.Column('is_deleted', sa.Boolean(), default=False, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 5. Voice Sessions table
    op.create_table(
        'voice_sessions',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('beneficiary_id', sa.String(36), sa.ForeignKey('beneficiaries.id', ondelete='CASCADE'), nullable=False),
        sa.Column('channel', sa.String(50), default='web_voice', nullable=False),
        sa.Column('language', sa.String(10), default='hi', nullable=False),
        sa.Column('status', sa.String(50), default='in_progress', nullable=False),
        sa.Column('current_question_index', sa.Integer(), default=0, nullable=False),
        sa.Column('answers', sa.JSON(), nullable=False),
        sa.Column('messages', sa.JSON(), nullable=False),
        sa.Column('audio_metadata', sa.JSON(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
    )

    # 6. Recommendations table
    op.create_table(
        'recommendations',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('beneficiary_id', sa.String(36), sa.ForeignKey('beneficiaries.id', ondelete='CASCADE'), nullable=False),
        sa.Column('qualification_id', sa.String(36), sa.ForeignKey('qualifications.id', ondelete='CASCADE'), nullable=False),
        sa.Column('rank', sa.Integer(), nullable=False),
        sa.Column('match_score', sa.Float(), nullable=False),
        sa.Column('fit_reason', sa.String(500), nullable=False),
        sa.Column('fit_details', sa.JSON(), nullable=False),
        sa.Column('skill_gaps', sa.JSON(), nullable=False),
        sa.Column('local_opportunity_signal', sa.String(100), default='High local demand', nullable=False),
        sa.Column('nearest_centre_id', sa.String(36), nullable=True),
        sa.Column('nearest_centre_distance_km', sa.Float(), nullable=True),
        sa.Column('rpl_eligible', sa.Boolean(), default=True, nullable=False),
        sa.Column('risk_factor', sa.String(255), nullable=True),
        sa.Column('status', sa.String(50), default='generated', nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 7. Outcomes table
    op.create_table(
        'outcomes',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('beneficiary_id', sa.String(36), sa.ForeignKey('beneficiaries.id', ondelete='CASCADE'), nullable=False),
        sa.Column('pathway_id', sa.String(36), nullable=False),
        sa.Column('stage', sa.String(50), default='counseling', nullable=False),
        sa.Column('status', sa.String(50), default='in_progress', nullable=False),
        sa.Column('facilitator_id', sa.String(36), nullable=True),
        sa.Column('facilitator_notes', sa.String(500), nullable=True),
        sa.Column('wage_or_revenue_inr', sa.Float(), nullable=True),
        sa.Column('verification_documents', sa.JSON(), nullable=False),
        sa.Column('follow_up_milestones', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('outcomes')
    op.drop_table('recommendations')
    op.drop_table('voice_sessions')
    op.drop_table('beneficiaries')
    op.drop_table('training_centres')
    op.drop_table('qualifications')
    op.drop_table('users')
