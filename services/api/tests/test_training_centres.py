import pytest

def test_list_training_centres(client, beneficiary_token):
    response = client.get(
        "/api/v1/training-centres",
        headers={"Authorization": f"Bearer {beneficiary_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    assert any(c["centre_type"] == "PMKK" for c in data)

def test_get_nearby_training_centres(client, beneficiary_token):
    # Search within 25km of Lucknow Sadar (26.8467, 80.9462)
    response = client.get(
        "/api/v1/training-centres/nearby?latitude=26.8467&longitude=80.9462&radius_km=25",
        headers={"Authorization": f"Bearer {beneficiary_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    # Check that distance is calculated and sorted
    assert "distance_km" in data[0]
    assert data[0]["distance_km"] < 25.0
    if len(data) > 1:
        assert data[0]["distance_km"] <= data[1]["distance_km"]

def test_get_training_centre_by_id(client, beneficiary_token, db_session):
    from app.models import TrainingCentre
    tc = db_session.query(TrainingCentre).first()

    response = client.get(
        f"/api/v1/training-centres/{tc.id}",
        headers={"Authorization": f"Bearer {beneficiary_token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == tc.id
    assert response.json()["name"] == tc.name
