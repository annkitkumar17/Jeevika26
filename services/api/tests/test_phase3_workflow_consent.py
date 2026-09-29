import pytest
from app.models import Beneficiary, DataSource, Qualification

# 1. Admin Self-Registration Restriction
def test_admin_cannot_be_publicly_self_registered(client):
    res = client.post(
        "/api/v1/auth/register",
        json={
            "email": "hacker.admin@example.com",
            "password": "Password123!",
            "full_name": "Unauthorized Admin",
            "role": "admin"
        }
    )
    assert res.status_code == 403
    assert "admin accounts must be provisioned" in res.json()["detail"].lower()

# 2. Token Revocation and Password Reset Flow
def test_password_reset_flow(client, db_session):
    from app.services.auth import AuthService
    
    # Request reset
    token = AuthService.request_password_reset(db_session, "rajesh.kumar@example.com")
    assert len(token) > 10

    # Confirm reset with new password
    AuthService.confirm_password_reset(db_session, token, "NewSecurePassword456!")

    # Login with new password succeeds
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "rajesh.kumar@example.com", "password": "NewSecurePassword456!"}
    )
    assert login_res.status_code == 200

# 3. Profile Extraction, Clarification, Confirmation, and Provenance
def test_profile_extraction_clarification_and_provenance(client, beneficiary_token, db_session):
    ben = db_session.query(Beneficiary).first()

    # 1. Start session
    session_res = client.post(
        "/api/v1/sessions",
        headers={"Authorization": f"Bearer {beneficiary_token}"},
        json={"beneficiary_id": ben.id, "channel": "web_voice", "language": "hi"}
    )
    session_id = session_res.json()["id"]

    # 2. Extract profile
    extract_res = client.post(
        f"/api/v1/sessions/{session_id}/extract-profile",
        headers={"Authorization": f"Bearer {beneficiary_token}"}
    )
    assert extract_res.status_code == 200
    fields = extract_res.json()["extracted_fields"]
    assert "education" in fields
    assert fields["education"]["confidence_score"] > 0.8

    # 3. Submit clarification
    clarify_res = client.post(
        f"/api/v1/sessions/{session_id}/clarify",
        headers={"Authorization": f"Bearer {beneficiary_token}"},
        json={
            "field_key": "education",
            "clarification_question": "आपकी उच्चतम योग्यता क्या है?",
            "response_text": "कक्षा 12 उत्तीर्ण (विज्ञान)"
        }
    )
    assert clarify_res.status_code == 200
    assert clarify_res.json()["status"] == "clarification_recorded"

    # 4. Get Field Provenance
    prov_res = client.get(
        f"/api/v1/sessions/{session_id}/field-provenance",
        headers={"Authorization": f"Bearer {beneficiary_token}"}
    )
    assert prov_res.status_code == 200
    prov_list = prov_res.json()
    assert len(prov_list) >= 1

    # 5. Confirm Profile
    confirm_res = client.post(
        f"/api/v1/sessions/{session_id}/confirm-profile",
        headers={"Authorization": f"Bearer {beneficiary_token}"},
        json={"confirmed_fields": {"education": "Class 12", "current_work": "Solar pump maintenance"}}
    )
    assert confirm_res.status_code == 200
    assert confirm_res.json()["status"] == "profile_confirmed"

# 4. Recommendation Engine v2 Multi-factor Scoring and Evidence
def test_recommendation_engine_v2_evidence_and_unknowns(client, beneficiary_token, db_session):
    ben = db_session.query(Beneficiary).first()

    res = client.post(
        "/api/v1/recommendations/generate",
        headers={"Authorization": f"Bearer {beneficiary_token}"},
        json={"beneficiary_id": ben.id, "force_refresh": True}
    )
    assert res.status_code == 200
    recs = res.json()
    assert len(recs) == 3
    top_rec = recs[0]
    
    # Check v2 fields
    assert "score_breakdown" in top_rec
    assert "aspiration_match" in top_rec["score_breakdown"]
    assert "evidence" in top_rec
    assert len(top_rec["evidence"]) >= 1
    assert "skill_gaps" in top_rec
    assert "next_actions" in top_rec

# 5. Human-in-the-loop Review Tasks and Decisions
def test_review_task_and_facilitator_decision(client, facilitator_token, db_session):
    ben = db_session.query(Beneficiary).first()

    # Create review task
    task_res = client.post(
        "/api/v1/reviews/tasks",
        headers={"Authorization": f"Bearer {facilitator_token}"},
        json={
            "beneficiary_id": ben.id,
            "task_type": "mobility_check",
            "priority": "high",
            "trigger_reason": "Candidate expressed interest in city centre outside 25km radius."
        }
    )
    assert task_res.status_code == 201
    task_id = task_res.json()["id"]

    # List review tasks
    list_res = client.get(
        "/api/v1/reviews/tasks",
        headers={"Authorization": f"Bearer {facilitator_token}"}
    )
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1

    # Submit decision
    dec_res = client.put(
        f"/api/v1/reviews/tasks/{task_id}/decision",
        headers={"Authorization": f"Bearer {facilitator_token}"},
        json={
            "decision": "approved",
            "decision_notes": "Facilitator confirmed candidate has daily bike transit to Mohanlalganj."
        }
    )
    assert dec_res.status_code == 200
    assert dec_res.json()["decision"] == "approved"
    assert dec_res.json()["status"] == "resolved"

# 6. Referral with Idempotency Key & Follow-ups
def test_referral_creation_and_idempotency(client, facilitator_token, db_session):
    ben = db_session.query(Beneficiary).first()

    ref_payload = {
        "idempotency_key": "ref-idem-unique-12345",
        "beneficiary_id": ben.id,
        "target_type": "training_centre",
        "target_id": "PMKK-SADAR-01",
        "pathway_id": "path-solar-01",
        "counseling_summary": "Beneficiary counseled for PM-KUSUM pump technician module."
    }

    # First dispatch
    res1 = client.post("/api/v1/referrals", headers={"Authorization": f"Bearer {facilitator_token}"}, json=ref_payload)
    assert res1.status_code == 201
    ref_id = res1.json()["id"]

    # Second duplicate dispatch with same idempotency key returns existing record without duplicate error
    res2 = client.post("/api/v1/referrals", headers={"Authorization": f"Bearer {facilitator_token}"}, json=ref_payload)
    assert res2.status_code in (200, 201)
    assert res2.json()["id"] == ref_id

    # Update progress
    prog_res = client.put(
        f"/api/v1/referrals/{ref_id}/progress",
        headers={"Authorization": f"Bearer {facilitator_token}"},
        json={"status": "candidate_contacted", "provider_feedback": "Orientation scheduled for Monday."}
    )
    assert prog_res.status_code == 200
    assert prog_res.json()["status"] == "candidate_contacted"

    # Case timeline
    time_res = client.get(
        f"/api/v1/cases/{ben.id}/timeline",
        headers={"Authorization": f"Bearer {facilitator_token}"}
    )
    assert time_res.status_code == 200
    events = time_res.json()
    assert len(events) >= 1

# 7. DPDP Purpose-Specific Consents, Withdrawal, Data Portability, and Audit
def test_dpdp_consents_and_data_export(client, beneficiary_token):
    # Grant consent
    grant_res = client.post(
        "/api/v1/consents",
        headers={"Authorization": f"Bearer {beneficiary_token}"},
        json={
            "purpose": "follow_up_retention",
            "consent_text": "I consent to 30, 90, and 180 day follow-up check-ins by PM-AJAY facilitators.",
            "language": "hi",
            "is_granted": True
        }
    )
    assert grant_res.status_code == 201
    assert grant_res.json()["purpose"] == "follow_up_retention"

    # List consents
    list_res = client.get("/api/v1/consents", headers={"Authorization": f"Bearer {beneficiary_token}"})
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1

    # Withdraw consent
    with_res = client.post("/api/v1/consents/follow_up_retention/withdraw", headers={"Authorization": f"Bearer {beneficiary_token}"})
    assert with_res.status_code == 200
    assert with_res.json()["is_granted"] is False

    # Privacy Export (Data Portability)
    exp_res = client.get("/api/v1/privacy/export", headers={"Authorization": f"Bearer {beneficiary_token}"})
    assert exp_res.status_code == 200
    assert "user_account" in exp_res.json()["data"]

# 8. Location Consent and Manual Fallback
def test_location_consent_and_manual_fallback(client, beneficiary_token, db_session):
    ben = db_session.query(Beneficiary).first()

    # Location consent
    loc_res = client.post(
        f"/api/v1/beneficiaries/{ben.id}/location-consent",
        headers={"Authorization": f"Bearer {beneficiary_token}"},
        json={"granted": True, "latitude": 26.850, "longitude": 80.950, "accuracy_meters": 15.0}
    )
    assert loc_res.status_code == 200
    assert loc_res.json()["latitude"] == 26.850

    # Manual location fallback
    man_res = client.put(
        f"/api/v1/beneficiaries/{ben.id}/location?district=Lucknow&block=Mohanlalganj&village=Nagram",
        headers={"Authorization": f"Bearer {beneficiary_token}"}
    )
    assert man_res.status_code == 200
    assert man_res.json()["village"] == "Nagram"

# 9. Data Sources Registry, Validation, Publishing, Quality and Audit
def test_data_ingestion_and_audit(client, admin_token):
    # 1. Register Data Source
    source_res = client.post(
        "/api/v1/admin/data-sources",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "name": "State Skill Development Mission (SSDM) Registry",
            "owner": "UPSDM",
            "access_method": "approved_export",
            "licence_or_access_basis": "State Government Circular 2026/04"
        }
    )
    assert source_res.status_code == 201
    source_id = source_res.json()["id"]

    # 2. Validate import batch
    val_res = client.post(
        "/api/v1/admin/imports/validate",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "source_id": source_id,
            "import_type": "qualifications",
            "records": [
                {
                    "qp_code": "AGR/Q1102",
                    "title": "Micro Irrigation Technician",
                    "sector": "Agriculture",
                    "nsqf_level": 4
                },
                {
                    "qp_code": "", # Invalid (missing code)
                    "title": "Invalid QP",
                    "nsqf_level": 15 # Invalid level
                }
            ]
        }
    )
    assert val_res.status_code == 200
    val_data = val_res.json()
    assert val_data["valid_count"] == 1
    assert val_data["error_count"] == 1
    batch_id = val_data["batch_id"]

    # 3. Publish valid records
    pub_res = client.post(
        f"/api/v1/admin/imports/{batch_id}/publish",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert pub_res.status_code == 200
    assert "Successfully published" in pub_res.json()["message"]

    # 4. Data Quality diagnostics
    dq_res = client.get("/api/v1/admin/data-quality", headers={"Authorization": f"Bearer {admin_token}"})
    assert dq_res.status_code == 200
    assert "qualifications" in dq_res.json()

    # 5. Audit Events
    audit_res = client.get("/api/v1/admin/audit-events", headers={"Authorization": f"Bearer {admin_token}"})
    assert audit_res.status_code == 200
    assert len(audit_res.json()) >= 1

# 10. Offline Sync Events
def test_offline_sync_events(client, beneficiary_token):
    sync_res = client.post(
        "/api/v1/sync/events",
        headers={"Authorization": f"Bearer {beneficiary_token}"},
        json={
            "idempotency_key": "sync-offline-event-001",
            "device_id": "tablet-kiosk-sadar-04",
            "entity_type": "voice_transcript",
            "entity_id": "session-123",
            "action": "append",
            "payload": {"transcript": "कृषि कार्य में संलग्न हूँ।"}
        }
    )
    assert sync_res.status_code == 201
    assert sync_res.json()["sync_status"] == "applied"

# 11. Outcomes: Training Progress, Employment, Enterprise, and Follow-ups
def test_outcomes_tracking_and_milestones(client, facilitator_token, db_session):
    ben = db_session.query(Beneficiary).first()

    # Training progress
    tp_res = client.post(
        "/api/v1/outcomes/training-progress",
        headers={"Authorization": f"Bearer {facilitator_token}"},
        json={
            "idempotency_key": "tp-001",
            "beneficiary_id": ben.id,
            "training_centre_id": "PMKK-SADAR-01",
            "qp_code": "AGR/Q1101",
            "attendance_percentage": 92.5,
            "assessment_status": "passed",
            "certification_number": "PM-AJAY-CERT-9901"
        }
    )
    assert tp_res.status_code == 201
    assert tp_res.json()["assessment_status"] == "passed"

    # Employment outcome
    emp_res = client.post(
        "/api/v1/outcomes/employment",
        headers={"Authorization": f"Bearer {facilitator_token}"},
        json={
            "idempotency_key": "emp-001",
            "beneficiary_id": ben.id,
            "employer_name": "UP State Solar EPC",
            "role_title": "Solar Microgrid Maintenance Technician",
            "monthly_wage_inr": 18500.0,
            "joining_date": "2026-03-01",
            "verification_method": "facilitator_call"
        }
    )
    assert emp_res.status_code == 201
    assert emp_res.json()["role_title"] == "Solar Microgrid Maintenance Technician"

    # Enterprise outcome
    ent_res = client.post(
        "/api/v1/outcomes/enterprise",
        headers={"Authorization": f"Bearer {facilitator_token}"},
        json={
            "idempotency_key": "ent-001",
            "beneficiary_id": ben.id,
            "enterprise_name": "Kisan Solar Repair Unit",
            "activity_type": "Pump & inverter servicing",
            "udyam_or_shg_id": "UDYAM-UP-01-0091",
            "credit_scheme_linked": "PM-MUDRA",
            "loan_amount_sanctioned_inr": 50000.0,
            "monthly_estimated_revenue_inr": 22000.0
        }
    )
    assert ent_res.status_code == 201
    assert ent_res.json()["activity_type"] == "Pump & inverter servicing"

    # Dispatch referral to generate follow-ups
    client.post(
        "/api/v1/referrals",
        headers={"Authorization": f"Bearer {facilitator_token}"},
        json={
            "beneficiary_id": ben.id,
            "target_type": "training_centre",
            "target_id": "PMKK-SADAR-01",
            "pathway_id": "path-solar-01",
            "counseling_summary": "Beneficiary enrolled in solar training module."
        }
    )

    # List and complete follow-up
    fups_res = client.get(
        f"/api/v1/outcomes/follow-ups?beneficiary_id={ben.id}",
        headers={"Authorization": f"Bearer {facilitator_token}"}
    )
    assert fups_res.status_code == 200
    fups = fups_res.json()
    assert len(fups) >= 1
    fup_id = fups[0]["id"]

    comp_fup = client.put(
        f"/api/v1/outcomes/follow-ups/{fup_id}/complete",
        headers={"Authorization": f"Bearer {facilitator_token}"},
        json={
            "status": "completed",
            "outcome_summary": "Candidate confirmed wage payment received on time and good work environment.",
            "is_retained": True
        }
    )
    assert comp_fup.status_code == 200
    assert comp_fup.json()["status"] == "completed"

# 12. Local Opportunities Nearby Search & Discovery
def test_opportunities_nearby_and_listing(client, beneficiary_token):
    res = client.get(
        "/api/v1/opportunities/signals?district=Lucknow",
        headers={"Authorization": f"Bearer {beneficiary_token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)

    nearby_res = client.get(
        "/api/v1/opportunities/nearby?district=Lucknow&sector=Green Jobs / Solar",
        headers={"Authorization": f"Bearer {beneficiary_token}"}
    )
    assert nearby_res.status_code == 200
    nearby_data = nearby_res.json()
    assert isinstance(nearby_data, list)

# 13. Privacy Deletion Request
def test_privacy_request_deletion(client, beneficiary_token):
    del_res = client.delete(
        "/api/v1/privacy/request-deletion?reason=Candidate opted out of digital records",
        headers={"Authorization": f"Bearer {beneficiary_token}"}
    )
    assert del_res.status_code == 200
    assert "Data deletion request processed" in del_res.json()["message"]
