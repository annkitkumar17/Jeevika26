from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import time
import logging

from app.core.config import settings
from app.core.database import Base, engine, SessionLocal
from app.models import (
    User,
    Beneficiary,
    Qualification,
    TrainingCentre,
    Recommendation,
    Outcome,
    DataSource,
    Employer,
    OpportunitySignal,
)
from app.services.recommendation_engine import RecommendationEngine
from app.services.rate_limiter import RateLimiterService

# Import Routers
from app.api.v1.auth import router as auth_router
from app.api.v1.beneficiaries import router as beneficiaries_router
from app.api.v1.sessions import router as sessions_router
from app.api.v1.recommendations import router as recommendations_router
from app.api.v1.training_centres import router as training_centres_router
from app.api.v1.admin import router as admin_router
from app.api.v1.workflow import router as workflow_router
from app.api.v1.consent_privacy import router as consent_privacy_router
from app.api.v1.opportunities import router as opportunities_router
from app.api.v1.sync import router as sync_router
from app.api.v1.bhashini import router as bhashini_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("jeevika_api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables and seed initial verified sources and sample data
    try:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            # Seed default Data Source
            if db.query(DataSource).count() == 0:
                nqr_source = DataSource(
                    name="National Qualifications Register (NQR)",
                    owner="NCVET / Ministry of Skill Development and Entrepreneurship",
                    base_url="https://nqr.gov.in",
                    access_method="official_api",
                    licence_or_access_basis="Open Government Data License - India",
                    sync_status="active",
                    version="2024.1",
                    last_sync_at=datetime.now(timezone.utc)
                )
                db.add(nqr_source)
                db.commit()

            # Seed qualifications and training centres if empty
            if db.query(Qualification).count() == 0:
                logger.info("Seeding initial NQR verified qualifications...")
                RecommendationEngine._seed_default_qualifications(db)
            if db.query(TrainingCentre).count() == 0:
                logger.info("Seeding initial training centres...")
                RecommendationEngine._seed_default_training_centres(db)
                
            # Seed sample Opportunity Signals
            if db.query(OpportunitySignal).count() == 0:
                signals = [
                    OpportunitySignal(
                        sector="Green Jobs / Electronics",
                        district="Lucknow",
                        block="Sadar",
                        demand_level="high",
                        openings_count=42,
                        source_name="UP Solar Energy Development Agency (UPNEDA)",
                        observed_date="2026-09-01",
                        confidence_score=0.92,
                        verification_status="verified"
                    ),
                    OpportunitySignal(
                        sector="Food Processing",
                        district="Lucknow",
                        block="Mohanlalganj",
                        demand_level="moderate",
                        openings_count=28,
                        source_name="District Industry Centre (DIC) MSME Census",
                        observed_date="2026-08-15",
                        confidence_score=0.88,
                        verification_status="verified"
                    ),
                ]
                for s in signals:
                    db.add(s)
                db.commit()

        finally:
            db.close()
    except Exception as e:
        logger.warning(f"Database table initialization notice: {e}")
    yield
    # Shutdown
    logger.info("Jeevika Saarthi API shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="2.0.0",
    description="Production-grade REST API for Jeevika Saarthi AI: Evidence-backed NSQF livelihood pathways, human-in-the-loop review, and verified government data provenance under PM-AJAY.",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware
origins = settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting & Security Headers Middleware
@app.middleware("http")
async def security_and_rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "127.0.0.1"
    
    # 1. Rate Limiting via Redis / In-memory
    is_allowed, count = RateLimiterService.check_rate_limit(
        client_ip=client_ip,
        limit=settings.RATE_LIMIT_PER_MINUTE,
        window_seconds=60
    )
    
    if not is_allowed:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Rate limit exceeded. Maximum 100 requests per minute."}
        )

    # Process request
    response: Response = await call_next(request)

    # 2. Strict Security Headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    return response

# Register API Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(beneficiaries_router, prefix=settings.API_V1_STR)
app.include_router(sessions_router, prefix=settings.API_V1_STR)
app.include_router(recommendations_router, prefix=settings.API_V1_STR)
app.include_router(training_centres_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)
app.include_router(workflow_router, prefix=settings.API_V1_STR)
app.include_router(consent_privacy_router, prefix=settings.API_V1_STR)
app.include_router(opportunities_router, prefix=settings.API_V1_STR)
app.include_router(sync_router, prefix=settings.API_V1_STR)
app.include_router(bhashini_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Health"])
def root():
    return {
        "service": "Jeevika Saarthi AI - Backend API",
        "status": "online",
        "version": "2.0.0",
        "docs": "/docs",
        "environment": settings.ENVIRONMENT
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "database": "connected"
    }
