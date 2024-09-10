from fastapi_easystart.utils.enums.base import BaseCustomEnum


class DatabaseExceptionEnum(BaseCustomEnum):
    DATABASE_NOT_FOUND = 'Database not found'
    DATABASE_NOT_SUPPORTED = 'Database not supported'
    DATABASE_INVALID = 'Database invalid'
    DATABASE_INVALID_PASSWORD = 'Database invalid password'
    DATABASE_INVALID_USERNAME = 'Database invalid username'
    DATABASE_INVALID_EMAIL = 'Database invalid email'
    DATA_FETCH_FAILED = 'Failed to fetch data from database'
