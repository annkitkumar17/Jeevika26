import pytest
from app.models import Beneficiary

def test_generate_and_get_recommendations(client, beneficiary_token, db_session):
    ben = db_session.query(Beneficiary).first()

    # Generate recommendations
    gen_res = client.post(
        "/api/v1/recommendations/generate",
        headers={"Authorization": f"Bearer {beneficiary_token}"},
        json={
            "beneficiary_id": ben.id,
            "force_refresh": True
        }
    )
    assert gen_res.status_code == 200
    recs = gen_res.json()
    assert len(recs) == 3
    assert recs[0]["rank"] == 1
    assert recs[0]["match_score"] >= 70.0
    assert "Solar Pump Technician" in recs[0]["fit_reason"] or "pump" in recs[0]["fit_reason"].lower()

    # Fetch recommendations via GET
    get_res = client.get(
        f"/api/v1/recommendations?beneficiary_id={ben.id}",
        headers={"Authorization": f"Bearer {beneficiary_token}"}
    )
    assert get_res.status_code == 200
    data = get_res.json()
    assert len(data) == 3

def test_select_recommendation_pathway(client, beneficiary_token, db_session):
    ben = db_session.query(Beneficiary).first()

    # Ensure recs exist
    gen_res = client.post(
        "/api/v1/recommendations/generate",
        headers={"Authorization": f"Bearer {beneficiary_token}"},
        json={"beneficiary_id": ben.id}
    )
    top_rec_id = gen_res.json()[0]["id"]

    # Select recommendation
    sel_res = client.put(
        f"/api/v1/recommendations/{top_rec_id}/select",
        headers={"Authorization": f"Bearer {beneficiary_token}"}
    )
    assert sel_res.status_code == 200
    assert sel_res.json()["status"] == "selected"

    # Verify beneficiary is enrolled
    db_session.refresh(ben)
    assert ben.status == "enrolled"
    assert ben.enrolled_pathway_id == top_rec_id
