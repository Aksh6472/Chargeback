"""
Chargeback Evidence AI - Application Configuration
Centralized configuration management with Pydantic Settings.
Contains only settings definitions and configuration values.
"""

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # App Information
    APP_NAME: str = "Chargeback Evidence AI"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Directories
    ROOT_DIR: Path = PROJECT_ROOT
    DATA_DIR: Path = PROJECT_ROOT / "data"
    UPLOADS_DIR: Path = PROJECT_ROOT / "data" / "uploads"
    REPORTS_DIR: Path = PROJECT_ROOT / "reports" / "generated_packets"
    MODELS_DIR: Path = PROJECT_ROOT / "models"

    # API Configuration
    FASTAPI_HOST: str = "0.0.0.0"
    FASTAPI_PORT: int = 8000
    BACKEND_API_URL: str = "http://localhost:8000"

    # Streamlit Configuration
    STREAMLIT_SERVER_PORT: int = 8501

    # Gemini API
    GEMINI_API_KEY: Optional[str] = "demo_key_placeholder"
    GEMINI_MODEL: str = "gemini-1.5-flash"

    # Supabase & PostgreSQL
    SUPABASE_URL: Optional[str] = "https://placeholder-project.supabase.co"
    SUPABASE_KEY: Optional[str] = "placeholder-anon-key"
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = None
    DATABASE_URL: Optional[str] = None

    # n8n Orchestration
    N8N_WEBHOOK_URL: str = "http://localhost:5678/webhook/chargeback-evidence-pipeline"

    # Tesseract OCR
    TESSERACT_CMD: str = "tesseract"

    # ML Model Config
    XGB_MODEL_PATH: Path = PROJECT_ROOT / "models" / "evidence_xgb_model.json"
    MODEL_METADATA_PATH: Path = PROJECT_ROOT / "models" / "model_metadata.json"

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
