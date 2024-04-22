from pathlib import Path
from typing import Dict
import dj_database_url
from pydantic import Field, field_validator, model_validator, root_validator, validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FOLDER = Path(__file__).resolve().parent.parent.parent / 'envs'

class Settings(BaseSettings):
    # database_dsn: str
    # debug: bool
    # language_code: str
    # secret_key: str
    # installed_apps: list
    database_dsn: str = Field(init=False, default='')
    database_conn: Dict = Field(init=False, default={})
    debug: bool = False
    language_code: str = 'en-us'
    secret_key: str = ''
    installed_apps: str = Field(init=False, default='')
    apps: list[str] =Field(init=False, default=[]
                           )
    # installed_apps: list = []
    model_config = SettingsConfigDict(env_file=(f'{_ENV_FOLDER}/.env.test'), env_file_encoding='UTF-8')
                
    # class Config:
    #     env_file = f'{_ENV_FOLDER}/.env.test'

    @field_validator('database_conn')
    @classmethod
    def make_database_conn(cls, v, values): # pylint: disable=no-self-argument
        value = values.data['database_dsn']
        return dj_database_url.config(default=value)

    # @model_validator(pre=True)
    # def preprocess(cls, values):
    #     # Example: Modify field2 based on field1 before field validations
    # #     if field_name == 'installed_apps':
    # #         return [app.strip() for app in raw_value.splitlines() if app.strip() != '']
    # #     return cls.json_loads(raw_value) # pylint: disable=no-member
        
    #     if 'installed_apps' in values:
    #         value = values['installed_apps']
    #         values['installed_apps'] = [app.strip() for app in value.splitlines() if app.strip() != '']
    #     return values
    
    @field_validator('apps', mode='before')
    @classmethod
    def split_installed_apps(cls, v, values):
        print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
        print(values)
        print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
        print(v)
        print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
        value = values.data['installed_apps']
        print(value)
        
        return [app.strip() for app in value.splitlines() if app.strip() != '']

    # @validator('installed_apps', pre=True)
    # def split_installed_apps(cls, value):
    #     return [app.strip() for app in value.splitlines() if app.strip() != '']

settings = Settings()