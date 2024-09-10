from fastapi_easystart.utils.enums.base import BaseCustomEnum


class ResponseExceptionTypeEnum(BaseCustomEnum):
    NOT_FOUND = 'Resource not found'
    HTTP_EXCEPTION = 'HTTP Exception occurred.'
    GENERAL_EXCEPTION = 'A general exceptions occurred.'
    INVALID_VALUE_ERROR = 'A value error occurred.'
    VALUE_ERROR = 'A value error occurred.'
    VALIDATION_ERROR = 'A validation error occurred.'
    DATABASE_ERROR = 'A database error occurred.'
    AUTHENTICATION_ERROR = 'Authentication failed.'
    AUTHORIZATION_ERROR = 'Authorization failed.'
    RESOURCE_NOT_FOUND = 'Resource not found.'
    DUPLICATE_ENTRY_ERROR = 'Duplicate entry found.'
    TIMEOUT_ERROR = 'A timeout error occurred.'
    SERVER_ERROR = 'A server error occurred.'
    UNSUPPORTED_MEDIA_TYPE = 'Unsupported media type "{media_type}" in request.'



