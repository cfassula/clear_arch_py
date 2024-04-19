from pathlib import Path
from typing import Dict
import os
import dj_database_url
from pydantic_settings import BaseSettings
from pydantic import (
    Field,
    field_validator,
)

_ENV_FOLDER = Path(__file__).resolve().parent.parent.parent / 'envs'

APP_ENV = os.getenv('APP_ENV')

class ConfigService(BaseSettings):

    # model_config = SettingsConfigDict(env_file=(f'{_ENV_FOLDER}/.env', f'{_ENV_FOLDER}/.env.{APP_ENV}'))

    database_dsn: str = Field(init=False, default='')
    database_conn: Dict = Field(init=False, default={})
    debug: bool = False
    language_code: str = 'en-us'
    secret_key: str = ''
    
    class Config:
        
        env_file = f'{_ENV_FOLDER}/.env', f'{_ENV_FOLDER}/.env.{APP_ENV}'
        
        @classmethod
        def parse_env_var(cls, field_name, raw_value: str):
            if field_name == 'installed_apps':
                return [app.strip() for app in raw_value.splitlines() if app.strip() != '']
            return cls.json_loads(raw_value) # pylint: disable=no-member


    @field_validator('database_conn')
    @classmethod
    def make_database_conn(cls, v, values): # pylint: disable=no-self-argument
        value = values.data['database_dsn']
        return dj_database_url.config(default=value)

config_service = ConfigService()
