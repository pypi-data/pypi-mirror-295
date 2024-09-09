from pydantic import Field

from pydantic_settings import BaseSettings, SettingsConfigDict

class DefaultSettings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')
    environment: str
    app_name: str = Field(..., alias="application_name")