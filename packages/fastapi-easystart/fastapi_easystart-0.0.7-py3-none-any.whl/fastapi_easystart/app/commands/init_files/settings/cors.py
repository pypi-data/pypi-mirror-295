import os
from typing import List, Union, Any

from pydantic import AnyHttpUrl, Field, validator
from pydantic_settings import BaseSettings


class CorsSettings(BaseSettings):
    # Define backend CORS origins, which can be a list or a comma-separated string with a default value
    BACKEND_ALLOWED_CORS_ORIGINS: Union[List[AnyHttpUrl], str] = Field(
        default_factory=lambda: os.getenv(
            'CORS_ALLOW_BACKEND_ORIGINS',
            'http://localhost,http://localhost:8000,http://127.0.0.1,http://127.0.0.1:8000,*'
        ),
        alias="BACKEND_CORS_ORIGINS",
    )

    # Define frontend allowed origins with default development URLs
    FRONTEND_ALLOWED_CORS_ORIGINS: Union[List[AnyHttpUrl], str] = Field(
        default_factory=lambda: os.getenv(
            'CORS_ALLOW_FRONTEND_ORIGINS',
            'http://localhost,http://localhost:3000,http://127.0.0.1,http://127.0.0.1:3000'
        ),
        alias="FRONTEND_CORS_ORIGINS",
    )

    # Allow credentials flag, defaulting to True
    ALLOW_CREDENTIALS: bool = Field(
        default_factory=lambda: os.getenv('CORS_ALLOW_CREDENTIALS', 'True').lower() in ('true', '1')
    )

    class Config:
        # Prefix for environment variables related to CORS settings
        env_prefix = "CORS_"
        # Ignore extra fields in environment variables
        extra = "ignore"

    @validator('BACKEND_ALLOWED_CORS_ORIGINS', 'FRONTEND_ALLOWED_CORS_ORIGINS')
    def parse_cors_origins(cls, v: Any) -> Union[List[str], str]:
        # Parse the CORS origins from a string or list
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError(
            f"Invalid value for CORS origins: {v}. "
            f"Expected a list of URLs or a comma-separated string of URLs. "
            f"Example: 'http://example.com,http://another.com' or ['http://example.com', 'http://another.com']."
        )
