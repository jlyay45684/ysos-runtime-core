from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Runtime Orchestrator"
    app_version: str = "0.1.0"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="AIO_")


settings = Settings()
