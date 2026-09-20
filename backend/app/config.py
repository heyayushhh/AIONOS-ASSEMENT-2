from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./helpdesk.db"
    n8n_chat_webhook_url: Optional[str] = ""
    n8n_create_ticket_webhook_url: Optional[str] = ""
    n8n_ticket_status_webhook_url: Optional[str] = ""
    gemini_api_key: Optional[str] = ""
    embedding_model: str = "all-MiniLM-L6-v2"
    cors_origins: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"
    demo_seed: bool = True


settings = Settings()
