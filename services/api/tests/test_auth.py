import pytest

def test_register_new_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "sunita.devi@example.com",
            "password": "Password123!",
            "full_name": "Sunita Devi",
            "role": "beneficiary"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "sunita.devi@example.com"
    assert data["role"] == "beneficiary"
    assert "id" in data

def test_register_duplicate_email_fails(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "rajesh.kumar@example.com",
            "password": "Password123!",
            "full_name": "Duplicate Rajesh",
            "role": "beneficiary"
        }
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_login_success(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@jeevika.gov.in",
            "password": "AdminPass123!"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["role"] == "admin"

def test_login_invalid_password_fails(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@jeevika.gov.in",
            "password": "WrongPassword!"
        }
    )
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]

def test_refresh_token(client):
    # First login to get a real refresh token
    login_res = client.post(
        "/api/v1/auth/login",
        json={
            "email": "rajesh.kumar@example.com",
            "password": "BeneficiaryPass123!"
        }
    )
    refresh_token = login_res.json()["refresh_token"]

    # Refresh
    refresh_res = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert refresh_res.status_code == 200
    data = refresh_res.json()
    assert "access_token" in data

def test_get_current_user_me(client, beneficiary_token):
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {beneficiary_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "rajesh.kumar@example.com"
    assert data["role"] == "beneficiary"

def test_logout(client, beneficiary_token):
    response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {beneficiary_token}"}
    )
    assert response.status_code == 200
    assert "Successfully logged out" in response.json()["message"]
