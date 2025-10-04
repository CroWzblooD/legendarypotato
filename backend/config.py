"""
Configuration management for the AI Tutor Orchestrator.
Loads settings from environment variables with validation.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )
    
    # Application
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = True
    
    # Google Gemini
    google_api_key: str
    gemini_model: str = "gemini-1.5-flash"
    gemini_temperature: float = 0.7
    gemini_max_tokens: int = 2048
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./database/tutor.db"
    
    # CORS
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse allowed origins from comma-separated string."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    # Tool Service
    tool_service_url: str = "http://localhost:8001"
    
    # Logging
    log_level: str = "INFO"


# Global settings instance
settings = Settings()
