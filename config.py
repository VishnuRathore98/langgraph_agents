from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    OPEN_ROUTER_API_KEY: str
    OPEN_ROUTER_MODEL: str


settings = Settings()
