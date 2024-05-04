from pathlib import Path
from typing import Dict
import os
import dj_database_url
from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic import (
    Field,
    field_validator,
)

_ENV_FOLDER = Path(__file__).resolve().parent.parent.parent / 'envs'

APP_ENV = os.getenv('APP_ENV')

class ConfigService(BaseSettings):

    model_config = SettingsConfigDict(env_file=(f'{_ENV_FOLDER}/.env', f'{_ENV_FOLDER}/.env.{APP_ENV}'), env_file_encoding='UTF-8')

    database_dsn: str = Field(init=False, default='')
    database_conn: Dict = Field(init=False, default={})
    debug: bool = False
    language_code: str = 'en-us'
    secret_key: str = ''
    apps: str = Field(init=False, default='')
    installed_apps: list[str] = Field(init=False, default=[])
    middlewares: str = Field(init=False, default='')
    middlewares_additional: list[str] = Field(init=False, default=[])
    test_keep_db: bool = True
    test_use_migrations: bool = True
    
    @field_validator('database_conn')
    @classmethod
    def make_database_conn(cls, v, values): # pylint: disable=no-self-argument
        value = values.data['database_dsn']
        return dj_database_url.config(default=value)

    @field_validator('installed_apps', mode='before')
    @classmethod
    def split_installed_apps(cls, v, values):
        value = values.data['apps']
        return [app.strip() for app in value.splitlines() if app.strip() != '']

    @field_validator('middlewares_additional', mode='before')
    @classmethod
    def split_middlewares_additional(cls, v, values):
        value = values.data['middlewares']
        return [app.strip() for app in value.splitlines() if app.strip() != '']


config_service = ConfigService()
