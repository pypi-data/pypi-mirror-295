from fastapi import Request, status
from fastapi.responses import Response
from starlette.responses import JSONResponse

from fastapi_easystart.utils.enums import ResponseEnum


async def value_error_handler(request: Request, exc: ValueError) -> Response:
    """Handles ValueError exceptions with a more specific message."""

    response_content = {
        ResponseEnum.RESPONSE_KEY.RESPONSE_CODE.value: ResponseEnum.EXCEPTIONS.RESPONSE.VALUE_ERROR.response_key,
        ResponseEnum.RESPONSE_KEY.MESSAGE.value: str(exc),
        ResponseEnum.RESPONSE_KEY.DETAIL.value: str(exc)
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_400_BAD_REQUEST)
