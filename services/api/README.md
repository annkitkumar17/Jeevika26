# Jeevika Saarthi AI - Backend API (Phase 2)

Production-ready FastAPI backend service with PostgreSQL/PostGIS database, Redis caching, JWT token authentication, NSQF recommendation engine, and geospatial proximity queries for PM-AJAY.

## Tech Stack
- **Framework**: Python 3.11+, FastAPI 0.109+
- **Database & ORM**: PostgreSQL 16 + PostGIS 3.4, SQLAlchemy 2.0+, GeoAlchemy2
- **Validation**: Pydantic 2.5+ & Pydantic Settings
- **Migrations**: Alembic 1.13+
- **Authentication**: JWT (python-jose) + Password Hashing (passlib/bcrypt)
- **Testing**: Pytest, Pytest-Asyncio, HTTPX

---

## Quick Start Guide

### 1. Environment Setup
```bash
cd services/api
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

pip install -r requirements.txt
```

### 2. Start PostgreSQL & Redis Containers
```bash
docker-compose up -d db redis
```

### 3. Run Database Migrations
```bash
alembic upgrade head
```

### 4. Start Development Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- API is live at: `http://localhost:8000`
- Interactive Swagger UI Docs: `http://localhost:8000/docs`
- ReDoc Docs: `http://localhost:8000/redoc`

---

## Running Automated Tests

Run the test suite with coverage:
```bash
pytest -v --cov=app
```

---

## API Endpoints Summary

### Authentication (`/api/v1/auth`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | Register new user | No |
| `POST` | `/api/v1/auth/login` | Login with email/password (returns JWT) | No |
| `POST` | `/api/v1/auth/refresh` | Refresh access token | No |
| `POST` | `/api/v1/auth/logout` | Logout session | Yes |
| `GET` | `/api/v1/auth/me` | Current user profile | Yes |

### Beneficiaries (`/api/v1/beneficiaries`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/beneficiaries` | List beneficiaries (with filters) | Yes |
| `POST` | `/api/v1/beneficiaries` | Create beneficiary profile | Yes |
| `GET` | `/api/v1/beneficiaries/{id}` | Get beneficiary details | Yes |
| `PUT` | `/api/v1/beneficiaries/{id}` | Update beneficiary profile | Yes |
| `DELETE` | `/api/v1/beneficiaries/{id}` | Soft delete profile | Yes |

### Voice Sessions (`/api/v1/sessions`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/sessions` | Start new voice interview session | Yes |
| `POST` | `/api/v1/sessions/{id}/transcript` | Upload recognized answer transcript | Yes |
| `GET` | `/api/v1/sessions/{id}` | Get session details & messages | Yes |
| `PUT` | `/api/v1/sessions/{id}/complete` | Complete session & extract profile | Yes |

### Recommendations (`/api/v1/recommendations`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/recommendations` | Get ranked NSQF recommendations | Yes |
| `POST` | `/api/v1/recommendations/generate` | Generate/refresh 3 pathway recommendations | Yes |
| `PUT` | `/api/v1/recommendations/{id}/select` | Select active pathway goal | Yes |

### Training Centres (`/api/v1/training-centres`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/training-centres` | List all centres (PMKK, ITI, RSETI) | Yes |
| `GET` | `/api/v1/training-centres/nearby` | Geospatial proximity search (Haversine) | Yes |
| `GET` | `/api/v1/training-centres/{id}` | Get training centre details | Yes |

### Admin & Analytics (`/api/v1/admin`)
| Method | Endpoint | Description | Role Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/admin/metrics` | Real-time district KPIs & charts | Facilitator / Admin |
| `GET` | `/api/v1/admin/reports` | Exportable report datasets | Facilitator / Admin |
| `GET` | `/api/v1/admin/users` | List system users | Admin |

---

## Security & Reliability Features
1. **JWT Authentication & RBAC**: Access and refresh tokens with expiration and role checking (`beneficiary`, `facilitator`, `admin`).
2. **Password Security**: Passlib with bcrypt hashing.
3. **Rate Limiting**: 100 requests per minute per IP.
4. **CORS Security**: Configured for `http://localhost:3000`.
5. **Security Headers**: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection`, `Strict-Transport-Security`.
6. **SQL Injection Prevention**: Full ORM usage via SQLAlchemy 2.0 with parameterized queries.
7. **Pydantic Validation**: Strict schema parsing with field constraints.
