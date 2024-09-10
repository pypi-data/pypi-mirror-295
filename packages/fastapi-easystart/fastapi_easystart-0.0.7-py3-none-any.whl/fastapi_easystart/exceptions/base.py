from fastapi import HTTPException, status

from fastapi_easystart.utils.enums import ResponseEnum


class BaseHTTPException(HTTPException):
    """
    Custom base exceptions class that overrides the FastAPI HTTPException.

    Attributes:
        status_code (int): HTTP status code for the exceptions. Default is 400 (Bad Request).
        response_code (str): Custom response code from the ResponseEnum.
        message (str): Custom message from the ResponseEnum.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    response_code = ResponseEnum.EXCEPTIONS.RESPONSE.HTTP_EXCEPTION.response_key
    message = ResponseEnum.EXCEPTIONS.RESPONSE.HTTP_EXCEPTION.value

    def __init__(self, detail=None, message=None):
        """
        Initialize the BaseHTTPException with optional detail and message.

        Args:
            detail (str, any, optional): Detailed error message. Defaults to None.
            message (str, optional): Custom error message. Defaults to None.
        """
        # Set the detail attribute if provided
        if detail is not None:
            self.detail = detail

        # Set the message attribute if provided
        if message is not None:
            self.message = message

        # Initialize the parent HTTPException with status code and detail
        super().__init__(
            status_code=self.status_code,
            detail=message if detail is None else detail,
        )
