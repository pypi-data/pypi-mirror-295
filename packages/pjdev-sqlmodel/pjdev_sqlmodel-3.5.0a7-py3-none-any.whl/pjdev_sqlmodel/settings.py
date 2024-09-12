from pathlib import Path
from typing import (
    Optional,
)

from pydantic_settings import BaseSettings, SettingsConfigDict


class SqlModelSettings(BaseSettings):
    data_path: Path
    sqlite_filename: str = "data.db"

    model_config = SettingsConfigDict(
        case_sensitive=False, extra="ignore", env_prefix="PJDEV_"
    )


class Context:
    settings: Optional[SqlModelSettings] = None


__ctx = Context()


def init_settings(root: Path, data_directory_name: str = ".data") -> None:
    __ctx.settings = SqlModelSettings(
        _env_file=root / ".env", data_path=root / data_directory_name
    )


def get_settings() -> SqlModelSettings:
    if __ctx.settings is None:
        msg = "Settings are not initialized -- call init_settings()"
        raise Exception(msg)
    return __ctx.settings
