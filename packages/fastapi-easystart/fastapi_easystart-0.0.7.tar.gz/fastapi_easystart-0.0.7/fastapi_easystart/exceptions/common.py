from fastapi import status

from fastapi_easystart.exceptions.base import BaseHTTPException
from fastapi_easystart.utils.enums import ResponseEnum


# Custom exception for handling invalid input errors
class InvalidInputException(BaseHTTPException):
    """
    Exception raised when the input provided by the user is invalid.
    The response code and message are derived from the ResponseEnum.
    """
    response_code = ResponseEnum.EXCEPTIONS.RESPONSE.VALIDATION_ERROR.response_key
    message = ResponseEnum.EXCEPTIONS.RESPONSE.VALIDATION_ERROR.value


# Custom exception for handling not found errors
class NotFoundException(BaseHTTPException):
    """
    Exception raised when a resource is not found or a user does not have the necessary permissions.
    This exception is mapped to a 404 Not found HTTP status code.
    """
    response_code = ResponseEnum.EXCEPTIONS.RESPONSE.NOT_FOUND.response_key
    status_code = status.HTTP_404_NOT_FOUND
    message = ResponseEnum.EXCEPTIONS.RESPONSE.NOT_FOUND.value


# Custom exception for handling unsupported media type errors
class UnsupportedMediaTypeException(BaseHTTPException):
    """
    Exception raised when the media type of the request is unsupported.
    This exception is mapped to a 405 Method Not Allowed HTTP status code.
    """
    response_code = ResponseEnum.EXCEPTIONS.RESPONSE.UNSUPPORTED_MEDIA_TYPE.response_key
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    message = ResponseEnum.EXCEPTIONS.RESPONSE.UNSUPPORTED_MEDIA_TYPE.value
