from fastapi import status

from fastapi_easystart.exceptions.base import BaseHTTPException
from fastapi_easystart.utils.enums import ResponseEnum


class DataFetchingException(BaseHTTPException):
    """
    Exception raised when a user does not have the necessary permissions.py.
    """
    response_code = ResponseEnum.EXCEPTIONS.DATABASE.DATA_FETCH_FAILED.response_key
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = ResponseEnum.EXCEPTIONS.DATABASE.DATA_FETCH_FAILED.value
