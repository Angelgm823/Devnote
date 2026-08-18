from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALG: str = Field(default="HS256", env="JWT_ALG")
    JWT_EXPIRES_MINUTES: int = Field(default=60 * 24, env="JWT_EXPIRES_MINUTES")
    PROJECT_NAME: str = "Devnote"
    ENVIRONTMENT: str = Field(..., env="ENVIRONTMENT")

    class Config:
        env_file = ".env"


settings = Settings()
