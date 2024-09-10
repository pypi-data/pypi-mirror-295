from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from fastapi_easystart.utils.enums import ResponseEnum


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handles RequestValidationError exceptions with a more specific message."""
    details = exc.errors()

    modified_details = []
    response_code = ResponseEnum.EXCEPTIONS.RESPONSE.VALIDATION_ERROR.response_key  # Default response code
    message = ResponseEnum.EXCEPTIONS.RESPONSE.VALIDATION_ERROR.value  # Default message

    # Process each error detail
    for error in details:
        response_code = error.get("type", response_code)  # Use the existing response_code if 'type' is not present
        message = error.get("msg", message)  # Use the existing message if 'msg' is not present
        modified_detail = {
            "loc": error.get("loc", []),
            "message": error.get("msg", "No message provided"),
            "type": error.get("type", "unknown__error"),
        }

        # Safely handle 'url'
        if "input" in error:
            modified_detail["input"] = error.get("input", None)

        # Safely handle 'url'
        if "url" in error:
            modified_detail["url"] = error["url"]

        modified_details.append(modified_detail)

    response_content = {
        ResponseEnum.RESPONSE_KEY.RESPONSE_CODE.value: ResponseEnum.EXCEPTIONS.RESPONSE.VALIDATION_ERROR.value if response_code == "missing" else response_code,
        ResponseEnum.RESPONSE_KEY.MESSAGE.value: message,
        ResponseEnum.RESPONSE_KEY.DETAIL.value: modified_details
    }
    return JSONResponse(content=response_content, status_code=HTTP_422_UNPROCESSABLE_ENTITY)
