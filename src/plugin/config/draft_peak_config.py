from typing import Self

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from plugin.config.utils import PLUGIN_PATH


class DraftPeakConfig(BaseSettings):

    n_counts_min: int = Field(10, ge=1, le=50, alias='N_COUNTS_MIN')
    n_counts_max: int = Field(100, ge=1, le=500, alias='N_COUNTS_MAX')
    except_clipped_peak: bool = Field(True, alias='EXCEPT_CLIPPED_PEAK')
    except_sloped_peak: bool = Field(True, alias='EXCEPT_SLOPED_PEAK')
    except_edges: bool = Field(False, alias='EXCEPT_EDGES')
    amplitude_min: float = Field(0, ge=0, le=1e+3, alias='AMPLITUDE_MIN')
    slope_max: float = Field(.25, ge=0, le=1, alias='SLOPE_MAX')
    noise_level: int = Field(10, ge=3, le=10, alias='NOISE_LEVEL')

    model_config = SettingsConfigDict(
        env_file=PLUGIN_PATH / '.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    @model_validator(mode='after')
    def validate(self) -> Self:
        assert self.n_counts_min < self.n_counts_max

        return self


DRAFT_PEAK_CONFIG = DraftPeakConfig()
