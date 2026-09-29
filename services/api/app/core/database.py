from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

def get_engine():
    db_url = settings.get_database_url()
    try:
        engine = create_engine(
            db_url,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
            connect_args={"connect_timeout": 1} if "postgresql" in db_url else {}
        )
        # Test connection
        with engine.connect() as conn:
            pass
        return engine
    except Exception as e:
        logger.warning(f"PostgreSQL connection failed ({e}). Falling back to SQLite local database for development/testing.")
        sqlite_engine = create_engine(
            "sqlite:///./jeevika_local.db",
            connect_args={"check_same_thread": False}
        )
        return sqlite_engine

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
