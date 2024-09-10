from fastapi_easystart.utils.enums.base import BaseCustomEnum


class TokenExceptionTypeEnum(BaseCustomEnum):
    TOKEN_NOT_VALID = "Token is invalid or malformed."
    TOKEN_EXPIRED = "The token has expired and is no longer valid."
    TOKEN_MISSING = "Token is missing from the request."
    TOKEN_REVOKED = "The token has been revoked and is no longer valid."
