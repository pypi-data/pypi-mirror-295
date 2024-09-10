from functools import lru_cache

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from fastapi_easystart.helpers.logger import log
from fastapi_easystart.middlewares.requests import RequestMiddleware
from fastapi_easystart.middlewares.response import CustomBaseHTTPMiddleware

from ..config import settings


#  Add custom middleware
@lru_cache
def set_app_middleware(app):
    try:
        # Enable TrustedHostMiddleware
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.cors.BACKEND_ALLOWED_CORS_ORIGINS
        )

        # CORS configuration and Set all CORS enabled origins
        app.add_middleware(
            CORSMiddleware,
            # Trailing slash causes CORS failures from these supported domains
            allow_origins=settings.cors.FRONTEND_ALLOWED_CORS_ORIGINS,
            allow_credentials=settings.cors.ALLOW_CREDENTIALS,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Enable GZip
        app.add_middleware(GZipMiddleware, minimum_size=settings.app.gzip_minimum_size)

        # Add Request Middleware
        app.add_middleware(RequestMiddleware)

        # custom base api response
        app.add_middleware(CustomBaseHTTPMiddleware)

    except Exception as e:
        log.critical(f"Failed to set app middleware: {e}")
        raise
