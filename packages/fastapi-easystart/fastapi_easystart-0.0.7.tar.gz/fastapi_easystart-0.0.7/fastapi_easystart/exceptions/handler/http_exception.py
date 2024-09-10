from fastapi import Request, HTTPException
from fastapi.responses import Response
from starlette.responses import JSONResponse

from fastapi_easystart.utils.enums import ResponseEnum


async def http_exception_error_handler(request: Request, exc: HTTPException) -> Response:
    """Handles HTTPException exceptions with a more specific message."""
    response_code = getattr(exc, ResponseEnum.RESPONSE_KEY.RESPONSE_CODE.value, ResponseEnum.EXCEPTIONS.RESPONSE.HTTP_EXCEPTION.response_key)
    message = getattr(exc, ResponseEnum.RESPONSE_KEY.MESSAGE.value, "Oops! Something went wrong. Please try again later.")

    response_content = {
        ResponseEnum.RESPONSE_KEY.RESPONSE_CODE.value: response_code,
        ResponseEnum.RESPONSE_KEY.MESSAGE.value: message,
        ResponseEnum.RESPONSE_KEY.DETAIL.value: str(exc)
    }
    return JSONResponse(content=response_content, status_code=exc.status_code)
