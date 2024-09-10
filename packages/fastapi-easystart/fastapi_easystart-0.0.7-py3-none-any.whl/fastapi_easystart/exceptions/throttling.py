from fastapi import status

from fastapi_easystart.exceptions.base import BaseHTTPException
from fastapi_easystart.utils.enums import ResponseEnum


# Custom exception for handling rate limit exceeded errors
class RateLimitExceededException(BaseHTTPException):
    """
    Exception raised when the user exceeds the allowed rate limit for API requests.
    This is used to prevent abuse or excessive load on the server.
    """
    response_code = ResponseEnum.EXCEPTIONS.THROTTLING.RATE_LIMIT_EXCEEDED.response_key
    message = ResponseEnum.EXCEPTIONS.THROTTLING.RATE_LIMIT_EXCEEDED.value
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
