import pytest
from app.services.geospatial import GeoSpatialService
from app.core.security import get_password_hash, verify_password, create_access_token, decode_token

def test_haversine_distance_calculation():
    # Distance between Lucknow (26.8467, 80.9462) and Kanpur (26.4499, 80.3319) is roughly ~75-85 km
    dist = GeoSpatialService.haversine_distance_km(26.8467, 80.9462, 26.4499, 80.3319)
    assert 70.0 < dist < 90.0

def test_password_hashing_and_verification():
    password = "SuperSecretSecurePassword123!"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False

def test_token_creation_and_decoding():
    user_id = "user-test-12345"
    token = create_access_token(subject=user_id, role="facilitator")
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == user_id
    assert payload["role"] == "facilitator"
    assert payload["type"] == "access"

def test_expired_or_invalid_token_returns_none():
    invalid_token = "invalid.header.signature"
    assert decode_token(invalid_token) is None
