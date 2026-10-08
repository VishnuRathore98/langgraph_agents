from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="/home/vpsr/Desktop/python/Agents/langgraph_agents/chat_agent/.env",
        extra="allow",
    )

    OPEN_ROUTER_MODEL: str | None = ""
    OPEN_ROUTER_API_KEY: str | None = ""
    OPEN_ROUTER_EMBEDDING_MODEL: str | None = ""
    OPEN_ROUTER_BASE_URL: str | None = ""
    LANGSMITH_TRACING: str | None = ""
    LANGSMITH_ENDPOINT: str | None = ""
    LANGSMITH_API_KEY: str | None = ""
    LANGSMITH_PROJECT: str | None = ""
    OPEN_WEATHER_BASE_URL: str | None = ""
    OPEN_WEATHER_API_KEY: str | None = ""
    ALPHA_VANTAGE_STOCK_BASE_URL: str | None = ""
    ALPHA_VANTAGE_STOCK_API_KEY: str | None = ""
    TAVILY_API_KEY: str | None = ""

    HUGGINGFACE_API_KEY: str | None = ""
    HUGGINGFACE_EMBEDDING_MODEL: str | None = ""


settings = Settings()
