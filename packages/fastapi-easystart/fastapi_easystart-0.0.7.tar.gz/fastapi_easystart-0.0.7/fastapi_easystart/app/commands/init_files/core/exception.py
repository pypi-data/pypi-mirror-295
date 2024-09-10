from functools import lru_cache

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError

from fastapi_easystart.exceptions.handler import (custom_404_handler, general_exception_handler, http_exception_error_handler,
                                                 validation_exception_handler, value_error_handler)


@lru_cache
def set_exception_handlers(app):
    app.add_exception_handler(HTTPException, http_exception_error_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    app.add_exception_handler(ValueError, value_error_handler)
    app.add_exception_handler(404, custom_404_handler)

    return app
