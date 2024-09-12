from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    host: str = "localhost"
    name: str
    password: Optional[str] = None
    username: Optional[str] = None
    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
        env_nested_delimiter="__",
        env_prefix="db_",
    )


class Context:
    settings: Optional[PostgresSettings] = None


__ctx = Context()


def init_settings(root: Path):
    __ctx.settings = PostgresSettings(_env_file=root / ".env")


def get_settings() -> PostgresSettings:
    if __ctx.settings is None:
        msg = "Settings are not initialized -- call init_settings()"
        raise Exception(msg)
    return __ctx.settings
