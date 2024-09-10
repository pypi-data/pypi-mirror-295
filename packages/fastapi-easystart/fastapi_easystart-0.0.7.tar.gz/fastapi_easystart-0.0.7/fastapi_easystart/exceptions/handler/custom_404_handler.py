from fastapi import Request
from fastapi.exceptions import HTTPException as BaseHTTPException
from fastapi.responses import JSONResponse

from fastapi_easystart.utils.enums import ResponseEnum


async def custom_404_handler(request: Request, exc: BaseHTTPException) -> JSONResponse:
    response_code = getattr(exc, ResponseEnum.RESPONSE_KEY.RESPONSE_CODE.value, ResponseEnum.EXCEPTIONS.RESPONSE.NOT_FOUND.response_key)
    message = getattr(exc, ResponseEnum.RESPONSE_KEY.MESSAGE.value, exc.detail)

    response_content = {
        ResponseEnum.RESPONSE_KEY.RESPONSE_CODE.value: response_code,
        ResponseEnum.RESPONSE_KEY.MESSAGE.value: message or ResponseEnum.EXCEPTIONS.RESPONSE.NOT_FOUND.value,
        ResponseEnum.RESPONSE_KEY.DETAIL.value: exc.detail or "The requested resource was not found"
    }
    return JSONResponse(content=response_content, status_code=404)
