from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    DATABASE_URL: str
    ANTHROPIC_API_KEY: str
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"
    OPEN_METEO_BASE_URL: str
    GLOFAS_API_KEY: str | None = None
    ENVIRONMENT: str = "dev"
    THRESHOLDS_CONFIG_PATH: Path = Path(__file__).parent.parent / "config" / "thresholds.yaml"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
