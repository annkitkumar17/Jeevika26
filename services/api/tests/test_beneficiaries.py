import pytest

def test_list_beneficiaries_as_facilitator(client, facilitator_token):
    response = client.get(
        "/api/v1/beneficiaries",
        headers={"Authorization": f"Bearer {facilitator_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["name"] == "Rajesh Kumar"

def test_create_beneficiary_profile(client, admin_token):
    response = client.post(
        "/api/v1/beneficiaries",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "name": "Pooja Verma",
            "phone": "+91 91234 56789",
            "gender": "female",
            "age": 24,
            "preferred_language": "hi",
            "state": "Uttar Pradesh",
            "district": "Lucknow",
            "block": "Mohanlalganj",
            "village": "Gosainganj",
            "latitude": 26.782,
            "longitude": 80.991,
            "education": "Class 12",
            "current_work": "Tailoring and stitching clothes at home",
            "experience_years": "2 years",
            "skills": ["Sewing", "Pattern Cutting", "Measurement"],
            "preferences": {"employment_type": "self_employment", "max_travel_km": 15, "migration": False},
            "consent": {"profile_creation": True, "recommendations": True, "follow_up": True}
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Pooja Verma"
    assert data["status"] == "profiled"
    assert "id" in data

def test_get_beneficiary_details(client, facilitator_token, db_session):
    from app.models import Beneficiary
    ben = db_session.query(Beneficiary).first()
    
    response = client.get(
        f"/api/v1/beneficiaries/{ben.id}",
        headers={"Authorization": f"Bearer {facilitator_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == ben.id
    assert data["name"] == ben.name

def test_update_beneficiary_profile(client, facilitator_token, db_session):
    from app.models import Beneficiary
    ben = db_session.query(Beneficiary).first()

    response = client.put(
        f"/api/v1/beneficiaries/{ben.id}",
        headers={"Authorization": f"Bearer {facilitator_token}"},
        json={
            "education": "Class 12 Pass",
            "skills": ["Mechanical repair", "Electrical diagnostics", "Solar installation"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["education"] == "Class 12 Pass"
    assert "Solar installation" in data["skills"]

def test_delete_beneficiary_soft(client, admin_token, db_session):
    from app.models import Beneficiary
    ben = db_session.query(Beneficiary).first()

    response = client.delete(
        f"/api/v1/beneficiaries/{ben.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == ben.id

    # Verify soft delete
    db_session.refresh(ben)
    assert ben.is_deleted is True
