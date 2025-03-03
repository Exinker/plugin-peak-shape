import multiprocessing
from enum import Enum
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from spectrumlab.peaks.shape import Shape


PLUGIN_PATH = Path(__file__).parents[3].resolve()
DEFAULT_SHAPE = Shape(width=2, asymmetry=0, ratio=.1)
DEFAULT_MAX_WORKERS = 1


class LoggingLevel(Enum):

    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'


class Config(BaseSettings):

    logging_level: LoggingLevel = Field(LoggingLevel.INFO, alias='LOGGING_LEVEL')
    default_shape: Shape = Field(None, alias='DEFAULT_SHAPE')
    max_workers: int = Field(None, alias='MAX_WORKERS')

    model_config = SettingsConfigDict(
        env_file=PLUGIN_PATH / '.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    @property
    def plugin_path(self) -> str | Path:
        return PLUGIN_PATH

    @field_validator('default_shape', mode='before')
    @classmethod
    def validate_default_shape(cls, data: str | None) -> Shape:

        if data is None:
            return DEFAULT_SHAPE

        try:
            width, asymmetry, ratio = map(float, data.split(','))
            shape = Shape(width=width, asymmetry=asymmetry, ratio=ratio)
        except Exception:
            shape = DEFAULT_SHAPE
        return shape

    @field_validator('max_workers', mode='before')
    @classmethod
    def validate_max_workers(cls, data: int | None) -> int:

        if data is None:
            return DEFAULT_MAX_WORKERS

        try:
            max_workers = min(max(1, data), multiprocessing.cpu_count())
        except Exception:
            max_workers = DEFAULT_MAX_WORKERS
        return max_workers


CONFIG = Config()
