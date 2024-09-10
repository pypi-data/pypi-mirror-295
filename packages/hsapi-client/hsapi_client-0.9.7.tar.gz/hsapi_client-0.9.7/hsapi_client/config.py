import os
from typing import Union

from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='HSAPI_')
    server: str = "http://localhost:8080"
    api_path: str = "/api/v1"
    api_token: Union[str, None] = None
    ssl_verify: Union[bool, str] = True

    def refresh_api_token(self):
        self.api_token = os.environ.get('HSAPI_API_TOKEN', 'default')


class HTTPException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"{status_code} {message}")

    def __str__(self):
        return f"{self.status_code} {self.message}"
