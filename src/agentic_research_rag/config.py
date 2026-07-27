from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings and environment variables.
    Loaded automatically by pydantic-settings from a .env file.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: str = "development"
    log_level: str = "INFO"

    gemini_api_key: str | None = None
    groke_api_key: str | None = None
    groq_api_key: str | None = None
    perplexity_api_key: str | None = None
    pinecone_api_key: str | None = None
    pinecone_index_name: str = "agentic-research-index"
    # Local paths
    vector_db_path: str = "data/vector_db"
    reports_dir: str = "outputs/reports"


# Create a global settings instance to be imported across the app
settings = Settings()
