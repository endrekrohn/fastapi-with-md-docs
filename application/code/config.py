from typing import Any
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    ENVIRONMENT: str = "production"
    IS_DEV: bool | None = None

    @validator("IS_DEV", pre=True)
    def fill_environment_dev(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, bool):
            return v
        _env = values.get("ENVIRONMENT")
        return _env == "development" or _env == "dev"

    class Config:
        case_sensitive = True


settings = Settings()
