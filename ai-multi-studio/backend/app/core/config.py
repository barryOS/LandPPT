from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "AI Multi Studio Backend"
    api_prefix: str = "/api"
    sora_api_key: str = ""
    gemini_api_key: str = ""
    sora_base_url: str = "https://api.sora2.example.com"
    gemini_base_url: str = "https://generativelanguage.googleapis.com"


settings = Settings()
