import multiprocessing
from enum import Enum

from pydantic import Field
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
    skip_data_exceptions: bool = Field(False, alias='SKIP_DATA_EXCEPTIONS')

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


PLUGIN_CONFIG = PluginConfig()
