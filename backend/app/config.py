from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Set the base directory to the directory containing the .env file
BASE_DIR = Path(__file__).resolve().parents[2]

# Define the configuration model with the base settings
class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore")
    REDIS_URL: str = "redis://localhost:6379/0"
    DATABASE_URL: str = "codeless.sqlite"
    STORAGE_DIR: Path = BASE_DIR / "./storage"

# Create an instance of AppConfig
app_config = AppConfig()