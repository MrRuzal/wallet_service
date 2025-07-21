from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: SecretStr
    DB_NAME: str
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    APP_ENV: str = "dev"
    DEBUG: bool = False
    SQLALCHEMY_ECHO: bool = False

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD.get_secret_value()}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
