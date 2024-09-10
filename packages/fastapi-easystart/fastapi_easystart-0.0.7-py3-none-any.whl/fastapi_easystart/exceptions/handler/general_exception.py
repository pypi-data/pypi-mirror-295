import json

from fastapi import Request, status
from fastapi.exceptions import HTTPException as BaseHTTPException
from fastapi.logger import logger
from fastapi.responses import Response

from fastapi_easystart.schemas.response import APIBaseResponse


async def general_exception_handler(request: Request, exc: Exception) -> Response:
    """Handles uncaught exceptions and provides a more informative response."""

    base_response = APIBaseResponse()
    base_response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    base_response.results.status = False

    if isinstance(exc, BaseHTTPException):  # Handle known HTTP exceptions gracefully
        # Use the existing HTTPException status code and message if possible
        base_response.status_code = exc.status_code
        base_response.message = exc.reason or "An error occurred."
    else:  # Handle unknown exceptions with a generic message
        base_response.message = "Internal Server Error."

    # Log the exceptions for debugging purposes
    logger.error(f"An error occurred: {exc}")

    return Response(
        content=json.dumps(base_response.dict()),
        media_type="application/json",
        status_code=base_response.status_code,
    )
