from fastapi_easystart.utils.enums.base import BaseCustomEnum


class ResponseKeyEnum(BaseCustomEnum):
    RESULTS = 'results'
    CONTEXT = 'context'
    RESPONSE_CODE = 'response_code'
    STATUS_CODE = 'status_code'
    MESSAGE = 'message'
    DETAIL = 'detail'
    TIMESTAMP = 'timestamp'
    CUSTOM_EXCEPTION = 'custom_exception'
    EXCEPTION = 'exceptions'
    INFO = 'info'
    SUCCESS = 'success'
    WARNING = 'warning'
    ERRORS = 'errors'
    ACCESS_TOKEN = 'access_token'
    REFRESH_TOKEN = 'refresh_token'
    TOKEN = 'token'
    TYPE = 'type'
    STATUS = 'status'

    @property
    def response_key(self):
        # Override response_key - convert to lowercase
        return self.name.lower()
