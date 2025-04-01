import multiprocessing
from collections.abc import Sequence
from enum import Enum

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


DEFAULT_MAX_WORKERS = 1


class LoggingLevel(Enum):

    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'


class PluginConfig(BaseSettings):

    logging_level: LoggingLevel = Field(LoggingLevel.INFO, alias='LOGGING_LEVEL')
    max_workers: int = Field(DEFAULT_MAX_WORKERS, ge=1, le=multiprocessing.cpu_count(), alias='MAX_WORKERS')
    select_detectors: Sequence[int] | None = Field(None, alias='SELECT_DETECTORS')

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    @field_validator('select_detectors', mode='before')
    @classmethod
    def validate_select_detectors(cls, data: str | None) -> int | tuple[int] | None:

        if data is None:
            return None

        if isinstance(data, int):
            values = tuple([data])
            return tuple([
                value - 1
                for value in values
            ])

        if isinstance(data, str):

            if data == '':
                return None

            values = map(int, data.replace(' ', '').split(';'))
            return tuple([
                value - 1
                for value in values
            ])

        raise TypeError(f'Type of select_detectors {repr(data)} is not supported yet!')


PLUGIN_CONFIG = PluginConfig()
