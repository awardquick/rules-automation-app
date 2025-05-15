from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
import os

print("Environment variables:", dict(os.environ))  # Debug print


class Settings(BaseSettings):
    env: str = Field("development", env="ENV")
    database_url: str = Field(
        "postgresql://postgres:postgres@localhost:5432/rules_db", env="DATABASE_URL")
    debug: bool = Field(False, env="DEBUG")

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, v):
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes")
        return bool(v)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        validate_default=True
    )


settings = Settings()
print("Final database_url:", settings.database_url)  # Debug print
