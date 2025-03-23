from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from plugin.config.utils import PLUGIN_PATH, SEP
from spectrumlab.peaks.shape import Shape


DEFAULT_SHAPE = Shape(width=2, asymmetry=0, ratio=.1)


class RestoreShapeConfig(BaseSettings):

    default_shape: Shape = Field(None, alias='DEFAULT_SHAPE')
    error_max: float = Field(default=.001, alias='ERROR_MAX')
    error_mean: float = Field(default=.0001, alias='ERROR_MEAN')
    n_peaks_min: int = Field(default=10, alias='N_PEAKS_MIN')

    model_config = SettingsConfigDict(
        env_file=PLUGIN_PATH / '.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    @field_validator('default_shape', mode='before')
    @classmethod
    def validate_default_shape(cls, data: str | None) -> Shape:

        if data is None:
            return DEFAULT_SHAPE

        try:
            width, asymmetry, ratio = map(float, data.split(SEP))
            shape = Shape(width=width, asymmetry=asymmetry, ratio=ratio)
        except Exception:
            shape = DEFAULT_SHAPE
        return shape


RESTORE_SHAPE_CONFIG = RestoreShapeConfig()
