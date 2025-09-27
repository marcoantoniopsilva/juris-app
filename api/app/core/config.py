from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # App
    APP_BASE_URL: str = "http://localhost:8000"
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    POSTGRES_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/juridico"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # S3/MinIO
    S3_ENDPOINT: str = "http://localhost:9000"
    S3_BUCKET: str = "juridico-files"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_KMS_KEY_ID: str = ""
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # AI Providers
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    USE_OPENAI: bool = True
    LLM_PROVIDER: str = "openai"
    EMBEDDINGS_PROVIDER: str = "openai"
    RERANK_PROVIDER: str = "local"
    
    # Data Usage
    DATA_USAGE_OPT_OUT: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()