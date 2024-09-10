from fastapi_easystart.utils.enums.base import BaseCustomEnum


class ThrottlingExceptionTypeEnum(BaseCustomEnum):
    RATE_LIMIT_EXCEEDED = ' Too many requests.'
