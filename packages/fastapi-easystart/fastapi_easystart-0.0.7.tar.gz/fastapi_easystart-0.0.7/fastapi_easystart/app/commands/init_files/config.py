import os
from typing import List, ClassVar

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings

from .settings import FASTAPI_ENVIRONMENT, AppSettings, CorsSettings


class Settings(BaseSettings):
    # Define favicon_path with a type annotation as ClassVar
    favicon_path: ClassVar[str] = os.path.join(os.path.dirname(__file__), 'static', 'favicon.ico')

    # General settings
    fastapi_env: str = FASTAPI_ENVIRONMENT

    debug: bool = True if FASTAPI_ENVIRONMENT in ["dev", "local"] else False

    # app and credentials settings
    app: AppSettings = Field(default_factory=AppSettings)

    # CORS configuration settings
    allowed_origins: List[AnyHttpUrl] = ["http://localhost", "http://localhost:3000", ]
    allow_credentials: bool = True

    # Server settings
    server_host: str = "localhost"
    server_port: int = 8000

    # CORS configuration settings
    cors: CorsSettings = Field(default_factory=CorsSettings)


settings = Settings()
