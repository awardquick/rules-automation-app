from pydantic import BaseModel, Field
from typing import Optional
import os

print("Environment variables:", dict(os.environ))  # Debug print


class Settings(BaseModel):
    env: str = Field(
        "development",
        json_schema_extra={"env": "ENV"}
    )
    database_url: str = Field(
        "postgresql://postgres:postgres@localhost:5432/rules_db",
        json_schema_extra={"env": "DATABASE_URL"}
    )
    debug: bool = Field(
        False,
        json_schema_extra={"env": "DEBUG"}
    )


settings = Settings()
print("Final database_url:", settings.database_url)  # Debug print
