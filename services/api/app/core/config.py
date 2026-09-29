from typing import List, Union, Optional
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
import json

class Settings(BaseSettings):
    PROJECT_NAME: str = "Jeevika Saarthi AI - Backend API"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    
    # JWT & Auth
    SECRET_KEY: str = "jeevika-saarthi-super-secret-jwt-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres_password"
    POSTGRES_DB: str = "jeevika_db"
    POSTGRES_PORT: int = 5432
    
    DATABASE_URL: Optional[str] = None
    ASYNC_DATABASE_URL: Optional[str] = None
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Bhashini Speech & AI Pipeline
    BHASHINI_USER_ID: str = "4488e52b16-cd68-4ec5-b2f7-0469e5c91b69"
    BHASHINI_API_KEY: str = "4488e52b16-cd68-4ec5-b2f7-0469e5c91b69"
    BHASHINI_INFERENCE_KEY: str = "k3FEJN4_5onQnl6oOfmOFzz96DruoAmkhg4bduFKVi7W4X9sp59jAwzVvCl9fjbp"
    BHASHINI_PIPELINE_URL: str = "https://meity-auth.ulca.ai/ulca/apis/v0/model/getModelsPipeline"
    BHASHINI_INFERENCE_URL: str = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"
    
    # Security & Rate Limiting
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    RATE_LIMIT_PER_MINUTE: int = 100

    @field_validator("CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, str) and v.startswith("["):
            return json.loads(v)
        return v

    def get_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )

settings = Settings()
