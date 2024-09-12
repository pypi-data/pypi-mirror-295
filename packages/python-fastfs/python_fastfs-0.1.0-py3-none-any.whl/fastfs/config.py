import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    base_dir: str = os.getcwd()
    port: int = 5001
    debug: bool = False

settings = Settings()

def get_settings() -> Settings:
    return settings