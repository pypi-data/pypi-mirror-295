from fastapi_easystart.exceptions.enums import *
from fastapi_easystart.utils.enums.crud import CreateResponseCodeEnum, UpdateResponseCodeEnum, DeleteResponseCodeEnum
from fastapi_easystart.utils.enums.response import ResponseKeyEnum


class ExceptionsType:
    DATABASE = DatabaseExceptionEnum
    RESPONSE = ResponseExceptionTypeEnum
    PERMISSION = PermissionExceptionTypeEnum
    TOKEN = TokenExceptionTypeEnum
    THROTTLING = ThrottlingExceptionTypeEnum
    AUTHENTICATION = AuthenticationExceptionEnum


class ResponseEnum:
    RESPONSE_KEY = ResponseKeyEnum
    EXCEPTIONS = ExceptionsType
    CREATE = CreateResponseCodeEnum
    UPDATE = UpdateResponseCodeEnum
    DELETE = DeleteResponseCodeEnum
