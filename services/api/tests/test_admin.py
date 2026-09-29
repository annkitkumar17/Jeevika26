import pytest

def test_admin_metrics_authorized(client, admin_token):
    response = client.get(
        "/api/v1/admin/metrics",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "kpis" in data
    assert "beneficiaries_profiled" in data["kpis"]
    assert "profiled_over_time" in data
    assert "top_sectors_by_block" in data
    assert "recommendation_categories" in data

def test_admin_metrics_forbidden_for_regular_beneficiary(client, beneficiary_token):
    response = client.get(
        "/api/v1/admin/metrics",
        headers={"Authorization": f"Bearer {beneficiary_token}"}
    )
    assert response.status_code == 403
    assert "privileges" in str(response.json()["detail"]).lower()

def test_admin_reports_generation(client, admin_token):
    response = client.get(
        "/api/v1/admin/reports?report_type=beneficiary_summary",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["report_type"] == "beneficiary_summary"
    assert "data" in data

def test_admin_list_users(client, admin_token):
    response = client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    assert any(u["role"] == "admin" for u in data)
