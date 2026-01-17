from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramConfig(BaseSettings):

    token: SecretStr = Field('', alias='TELEGRAM_TOKEN')
    chat_id: str = Field('', alias='TELEGRAM_CHAT_ID')

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


TELEGRAM_CONFIG = TelegramConfig()
