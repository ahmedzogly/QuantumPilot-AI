"""
Core configuration - DDD + 12-factor
"""
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "QuantumPilot AI"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "dev-secret-change-in-prod"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ALGORITHM: str = "HS256"
    
    # Database
    POSTGRES_USER: str = "quantumpilot"
    POSTGRES_PASSWORD: str = "quantumpilot"
    POSTGRES_DB: str = "quantumpilot_db"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Redis & RabbitMQ
    REDIS_URL: str = "redis://redis:6379/0"
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672/"
    
    # IBM Quantum
    IBM_TOKEN: str = os.getenv("IBM_TOKEN", "")
    IBM_CRN: str = os.getenv("IBM_CRN", "")
    IBM_CHANNEL: str = "ibm_cloud"
    
    # AI Engine
    NEURALUCB_HIDDEN_DIM: int = 128
    NEURALUCB_ALPHA: float = 1.0
    NEURALUCB_LAMBDA: float = 1.0
    
    # Model paths
    GRANITE_MODEL_PATH: str = "Qiskit/granite-8b-qiskit"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://frontend:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
