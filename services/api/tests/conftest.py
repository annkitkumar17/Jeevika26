import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
import sys

# Ensure root api folder is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["ENVIRONMENT"] = "testing"

from app.main import app
from app.core.database import Base, get_db
from app.core.security import create_access_token, get_password_hash
from app.models import User, Beneficiary, Qualification, TrainingCentre
from app.services.recommendation_engine import RecommendationEngine

# In-memory SQLite DB for clean isolated testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Seed initial qualifications and centres
    RecommendationEngine._seed_default_qualifications(db)
    RecommendationEngine._seed_default_training_centres(db)
    
    # Seed test users
    admin_user = User(
        email="admin@jeevika.gov.in",
        hashed_password=get_password_hash("AdminPass123!"),
        full_name="District Admin Sadar",
        role="admin"
    )
    facilitator_user = User(
        email="facilitator@jeevika.gov.in",
        hashed_password=get_password_hash("FacilPass123!"),
        full_name="Amit Singh VLE",
        role="facilitator"
    )
    beneficiary_user = User(
        email="rajesh.kumar@example.com",
        hashed_password=get_password_hash("BeneficiaryPass123!"),
        full_name="Rajesh Kumar",
        role="beneficiary"
    )
    db.add_all([admin_user, facilitator_user, beneficiary_user])
    db.commit()
    
    # Seed test beneficiary profile
    test_ben = Beneficiary(
        user_id=beneficiary_user.id,
        name="Rajesh Kumar",
        phone="+91 98765 12345",
        gender="male",
        age=28,
        preferred_language="hi",
        state="Uttar Pradesh",
        district="Lucknow",
        block="Sadar",
        village="Rampur Demo",
        latitude=26.8467,
        longitude=80.9462,
        education="Class 10",
        current_work="Assists with agricultural pump repair",
        experience_years="3 years",
        skills=["Basic mechanical repair", "Tool handling", "Customer interaction"],
        preferences={"employment_type": "self_employment", "max_travel_km": 25, "migration": False},
        consent={"profile_creation": True, "recommendations": True, "follow_up": True},
        status="profiled"
    )
    db.add(test_ben)
    db.commit()

    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def admin_token(db_session):
    user = db_session.query(User).filter(User.email == "admin@jeevika.gov.in").first()
    return create_access_token(subject=user.id, role=user.role)

@pytest.fixture(scope="function")
def facilitator_token(db_session):
    user = db_session.query(User).filter(User.email == "facilitator@jeevika.gov.in").first()
    return create_access_token(subject=user.id, role=user.role)

@pytest.fixture(scope="function")
def beneficiary_token(db_session):
    user = db_session.query(User).filter(User.email == "rajesh.kumar@example.com").first()
    return create_access_token(subject=user.id, role=user.role)
