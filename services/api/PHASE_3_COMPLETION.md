# Phase 3 — Enhanced AI, Verified Data, Case Workflow and Outcomes
## Completion Report & Architecture Reference

### 1. Executive Summary
Phase 3 elevates the **Jeevika Saarthi AI** platform from a basic profile-and-course recommender into an **evidence-backed, human-supervised livelihood pathway platform** aligned with PM-AJAY and DPDP principles.

---

### 2. Critical Corrections Implemented

#### 1. External Data Availability & Source Registry
* **Zero Undocumented API Assumptions**: Support for official APIs, documented exports, and controlled admin CSV/JSON imports.
* **`DataSource` Model**: Tracks `owner`, `base_url`, `access_method`, `licence_or_access_basis`, `last_sync_at`, `version`, `checksum`, and `sync_status`.
* **Authoritative NQR Evidence**: Qualifications store `qualification_code`, `version`, `approval_date`, `currency_start`, `currency_end`, `archive_status`, `nsqc_status`, `entry_requirements`, `nos_units`, `rpl_available`, and `verification_status`.
* **NSQF Verification Guard**: Recommendations cannot claim "NSQF verified" unless `verification_status == "verified"` and linked to an authoritative source record.

#### 2. Recommendation Claims & Evidence-Backed Explainability
* **Recommendation Engine v2 Formula**:
  $$\text{Score} = (\text{aspiration\_match} \times 0.20) + (\text{skill\_match} \times 0.20) + (\text{entry\_fit} \times 0.15) + (\text{local\_opportunity} \times 0.15) + (\text{centre\_access} \times 0.10) + (\text{mobility\_fit} \times 0.10) + (\text{rpl\_bridge\_fit} \times 0.05) + (\text{outcomes\_signal} \times 0.05)$$
* **Structured Evidence & Unknowns**: Every recommendation outputs:
  * `why_this_fits`: Array of explainable criteria matches.
  * `skill_gaps`: Missing NOS units and recommended bridge modules.
  * `evidence`: Direct citations of NQR qualifications and verified centre delivery.
  * `unknowns`: Explicitly distinguishes missing data (e.g. market wages, placement records) from zero scores.
  * `risks`: Highlights travel, care, migration, or prerequisite risks.
  * `next_actions`: Clear sequential steps for candidate & facilitator.
  * `human_review_required`: Flagged when uncertainty or mobility constraints exceed thresholds.

#### 3. Security, Privacy & DPDP Compliance
* **Redis-Backed Rate Limiting**: Distributed sliding window rate limiter with in-memory fallback.
* **Token Rotation & Revocation**: Refresh tokens are revoked upon use or logout, preventing replay attacks.
* **Password Reset & Backoff**: Secure reset token generation and account lockout protections.
* **Role-Based Access & Ownership**: Strict route-level checks ensuring beneficiaries can only read their own data and facilitators cannot alter unassigned cases.
* **Admin Provisioning**: Public self-registration as `admin` is forbidden (returns HTTP 403). Admin accounts must be created through `/api/v1/admin/users/provision`.
* **DPDP Consent**: Purpose-specific consent records (`profile_analysis`, `local_referral`, `follow_up_retention`, `location_processing`), granular withdrawal, data export, and deletion workflows.
* **Sensitive Log Redaction**: Raw audio, Aadhaar numbers, and caste certificate images are never logged or stored unencrypted.

---

### 3. Core Database Models & Schema Additions

1. **`DataSource` & `DataImportBatch`** (`app/models/data_source.py`):
   * Full provenance tracking, checksum verification, schema validation, and rollback capability.
2. **`SkillConcept`, `OccupationConcept`, `BeneficiarySkillEvidence`** (`app/models/skills_occupations.py`):
   * Field-level extraction provenance, confidence scoring, dialect terms, and source session linkage.
3. **`RPLAssessment` & `SkillGap`** (`app/models/rpl_gap.py`):
   * Recognition of Prior Learning gap analysis, missing NOS units, bridge module mapping, and assessor sign-off.
4. **`OpportunitySignal`, `Employer`, `JobOpportunity`** (`app/models/opportunity.py`):
   * District-level economic signals, verified local job listings, and wage ranges.
5. **`ReviewTask`, `Referral`, `CaseEvent`** (`app/models/workflow.py`):
   * Human-in-the-loop task routing, idempotent referral creation (`idempotency_key`), and immutable audit event timelines.
6. **`TrainingProgress`, `EmploymentOutcome`, `EnterpriseOutcome`, `FollowUp`** (`app/models/outcome.py`):
   * Attendance, module completion, certification, wage employment, micro-enterprise launches (MUDRA/PM-FME), and 30/90/180-day follow-up retention.
7. **`ConsentRecord`, `PrivacyRequest`, `AuditEvent`** (`app/models/consent_privacy.py`):
   * DPDP-compliant data subject rights, consent withdrawal, data export, and deletion logs.
8. **`OfflineSyncEvent` & `NotificationMessage`** (`app/models/notification_sync.py`):
   * Offline synchronization queue with idempotency keys and multi-channel notification abstraction.

---

### 4. API Endpoints Reference

#### Profile Extraction & Provenance
* `POST /api/v1/sessions/{id}/extract-profile`: Extracts structured fields with confidence scores and evidence snippets.
* `POST /api/v1/sessions/{id}/clarify`: Generates targeted clarification questions for ambiguous fields.
* `POST /api/v1/sessions/{id}/confirm-profile`: Facilitator/candidate explicit confirmation of profile fields.
* `GET  /api/v1/sessions/{id}/field-provenance`: Field-by-field provenance and confidence audit.

#### Recommendations & Pathways
* `POST /api/v1/recommendations/generate`: Recommendation Engine v2 with multi-factor scoring, risks, and evidence.
* `GET  /api/v1/recommendations/beneficiary/{id}`: Fetch ranked pathways.
* `POST /api/v1/recommendations/select`: Candidate pathway selection.

#### Workflow & Reviews
* `GET  /api/v1/reviews/tasks`: List pending review tasks.
* `POST /api/v1/reviews/tasks`: Create review task for high-risk/uncertain cases.
* `PUT  /api/v1/reviews/tasks/{id}/decision`: Facilitator approval/rejection/modification.
* `POST /api/v1/referrals`: Idempotent referral dispatch to training centres / employers.
* `GET  /api/v1/referrals`: List candidate referrals.
* `PUT  /api/v1/referrals/{id}/progress`: Update candidate training/placement progress.
* `GET  /api/v1/cases/{beneficiary_id}/timeline`: Immutable audit timeline.

#### Outcomes & Milestones
* `POST /api/v1/outcomes/training-progress`: Log attendance, module completion, certification.
* `POST /api/v1/outcomes/employment`: Record wage placement with voluntary wage reporting.
* `POST /api/v1/outcomes/enterprise`: Record micro-enterprise launch with MUDRA linkage.
* `GET  /api/v1/outcomes/follow-ups`: List 30/90/180-day follow-up schedules.
* `PUT  /api/v1/outcomes/follow-ups/{id}/complete`: Log follow-up check-in outcome.

#### Consent & Privacy
* `GET  /api/v1/consents`: List active consent declarations.
* `POST /api/v1/consents`: Grant purpose-specific consent.
* `POST /api/v1/consents/{purpose}/withdraw`: Withdraw consent for a specific purpose.
* `GET  /api/v1/privacy/export`: DPDP machine-readable data export.
* `DELETE /api/v1/privacy/request-deletion`: Right-to-be-forgotten request.

#### Data Ingestion & Admin Diagnostics
* `POST /api/v1/admin/data-sources`: Register external source.
* `POST /api/v1/admin/imports/validate`: Validate CSV/JSON batches against quality rules.
* `POST /api/v1/admin/imports/{id}/publish`: Publish validated records to production.
* `POST /api/v1/admin/imports/{id}/rollback`: Rollback import batch.
* `GET  /api/v1/admin/data-quality`: Diagnostic report for missing coordinates, stale qualifications, etc.
* `GET  /api/v1/admin/audit-events`: Admin audit trail.

#### Geolocation & Nearby Discovery
* `POST /api/v1/beneficiaries/{id}/location-consent`: Record explicit location consent.
* `PUT  /api/v1/beneficiaries/{id}/location`: Update coordinates with accuracy metadata.
* `GET  /api/v1/training-centres/nearby`: PostGIS / Haversine distance search.
* `GET  /api/v1/opportunities/nearby`: Local employer job listings.
* `GET  /api/v1/opportunities/signals`: District economic demand signals.

#### Synchronization
* `POST /api/v1/sync/events`: Offline synchronization event queue with idempotency.

---

### 5. Automated Test Suite Results

```text
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\admin\Desktop\Jeevika\services\api
configfile: pytest.ini
plugins: anyio-4.15.1, asyncio-1.4.0, cov-7.1.0

tests/test_admin.py (4 passed)
tests/test_auth.py (7 passed)
tests/test_beneficiaries.py (5 passed)
tests/test_phase3_workflow_consent.py (13 passed)
tests/test_recommendations.py (2 passed)
tests/test_services.py (4 passed)
tests/test_sessions.py (2 passed)
tests/test_training_centres.py (3 passed)

======================= 40 passed, 1 warning in 38.50s ========================
Coverage: 93% Total (2,269 statements, 160 missing)
```

---

### 6. List of Unavailable External Integrations
1. **Live Bhashini ASR/TTS Engine**: Real Bhashini credentials and pipeline await deployment; currently mocked with bilingual phonetic transcription simulation.
2. **Direct SIDH / NCS Production Webhooks**: No open public webhook endpoints exist; integrated via controlled admin batch ingestion and periodic schema sync adapters.
3. **Automated WhatsApp / IVR Gateway**: Production SMS/IVR gateways require DLT registration; abstracted behind `NotificationProvider` interface.
