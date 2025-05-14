from pydantic import BaseSettings


class Settings(BaseSettings):
    env: str = Field("development", env="ENV")
    database_url: str = Field(..., env="DATABASE_URL")
    debug: bool = Field(False, env="DEBUG")

    class Config:
        env_file = ".env"


settings = Settings()
