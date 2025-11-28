import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Research RAG Assistant"
    API_V1_STR: str = "/api/v1"
    
    # Database
    SQLITE_URL: str = "sqlite+aiosqlite:///./data/sqlite/rag.db"
    
    # Vector DB
    CHROMA_PERSIST_DIRECTORY: str = "./data/chroma"
    
    # LLM (OpenRouter)
    OPENROUTER_API_KEY: str = "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"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    LLM_MODEL: str = "openai/gpt-oss-20b:free" # Default model, can be changed
    
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

settings = Settings()
