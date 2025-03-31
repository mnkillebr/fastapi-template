from pydantic import PostgresDsn, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # For an async SQLAlchemy engine with asyncpg, note the prefix "postgresql+asyncpg"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    ALEMBIC_LOCAL: str = Field(..., env="ALEMBIC_LOCAL")

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

settings = Settings()
