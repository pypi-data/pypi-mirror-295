import os

from pydantic import Field
from pydantic_settings import BaseSettings


class SwaggerSettings(BaseSettings):
    username: str = Field(default_factory=lambda: os.getenv('SWAGGER_USERNAME'))
    password: str = Field(default_factory=lambda: os.getenv('SWAGGER_PASSWORD'))

    class Config:
        env_prefix = "SWAGGER_"
        extra = "ignore"
