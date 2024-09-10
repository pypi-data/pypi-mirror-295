import json
from datetime import datetime, timezone
from typing import Optional, Any, Dict, Union

from fastapi import HTTPException
from pydantic import BaseModel

from fastapi_easystart.utils.enums import ResponseEnum

RESPONSE_STATUS_CODE = [200, 201, 202]


class SuccessAndErrorResponse(BaseModel):
    """
    A class representing a standardized response format for both success and error messages.

    Attributes:
        detail: The actual content of the response.
        type: The type of the content.
    """
    detail: Optional[Union[Dict[str, Any], list, str, bool, int, float]] = None
    type: Optional[str] = None

    @classmethod
    def create(cls, content: Optional[Union[Dict[str, Any], list, str, bool, int, float]]) -> Any:
        """
        Create a SuccessAndErrorResponse object from a dictionary or other types of content.

        :param content: The content to be included in the response.
        :return: An instance of SuccessAndErrorResponse.
        """
        if content is not None:
            if not isinstance(content, dict):
                content_type = type(content).__name__
                return cls(
                    type=content_type,
                    detail=content
                )

            data = content.pop(ResponseEnum.RESPONSE_KEY.DETAIL.response_key, content)
            content_type = type(data).__name__
            return cls(
                type=content_type,
                detail=data
            )
        return None


class APIBaseResultSchema(BaseModel):
    status: bool
    request_id: Optional[str]
    errors: Optional[SuccessAndErrorResponse] = None
    success: Optional[SuccessAndErrorResponse] = None

    @classmethod
    def create(cls, status: bool, request_id: str, content: Optional[Dict[str, Any]]) -> 'APIBaseResultSchema':
        content = SuccessAndErrorResponse.create(content=content) if content is not None else None

        return cls(
            status=status,
            request_id=request_id,
            success=content if content else None,
            errors=content if not status else None,
        )


class APIBaseResponse(BaseModel):
    status_code: int
    response_code: Optional[str]
    message: str
    timestamp: str = None  # Default to None to avoid the missing field issue
    results: APIBaseResultSchema

    def __init__(self, **data):
        super().__init__(**data)
        self.timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()

    class Config:
        json_encoders = {
            datetime: lambda v: v.replace(tzinfo=timezone.utc).isoformat()
        }
        json_schema_extra = {
            "success_example": {
                ResponseEnum.RESPONSE_KEY.STATUS_CODE.response_key: 200,
                ResponseEnum.RESPONSE_KEY.RESPONSE_CODE.response_key: "OK",
                ResponseEnum.RESPONSE_KEY.MESSAGE.response_key: "Success",
                ResponseEnum.RESPONSE_KEY.TIMESTAMP.response_key: datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
                ResponseEnum.RESPONSE_KEY.RESULTS.response_key: {
                    ResponseEnum.RESPONSE_KEY.STATUS.response_key: True,
                    "request_id": "6ed86d04-7773-4b88-9552-d9081a05822a",
                    ResponseEnum.RESPONSE_KEY.SUCCESS.response_key: {
                        ResponseEnum.RESPONSE_KEY.TYPE.response_key: "value",
                        ResponseEnum.RESPONSE_KEY.DETAIL.response_key: "value"
                    },
                },
            },
            "error_example": {
                ResponseEnum.RESPONSE_KEY.STATUS_CODE.response_key: 400,
                ResponseEnum.RESPONSE_KEY.RESPONSE_CODE.response_key: "Error",
                ResponseEnum.RESPONSE_KEY.MESSAGE.response_key: "Error message",
                ResponseEnum.RESPONSE_KEY.TIMESTAMP.response_key: datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
                ResponseEnum.RESPONSE_KEY.RESULTS.response_key: {
                    ResponseEnum.RESPONSE_KEY.STATUS.response_key: False,
                    "request_id": "6ed86d04-7773-4b88-9552-d9081a05822a",
                    ResponseEnum.RESPONSE_KEY.ERRORS.response_key: {
                        ResponseEnum.RESPONSE_KEY.TYPE.response_key: "value",
                        ResponseEnum.RESPONSE_KEY.DETAIL.response_key: "value"
                    },
                },
            }
        }

    @classmethod
    def create_from_exception(cls, exception: HTTPException):
        """
        Create an APIBaseResponse object from an HTTPException.
        """
        return cls(
            status_code=exception.status_code,
            response_code=None,
            message=str(exception.detail),
            timestamp=datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
            results=APIBaseResultSchema(
                status=False,
                request_id="6ed86d04-7773-4b88-9552-d9081a05822a",
                errors=SuccessAndErrorResponse.create(content={"data": exception.detail})
            )
        )

    @classmethod
    def get_structure_results(cls, status_code: int, request_id: str or None, content: Optional[Dict[str, Any]]) -> json:
        result_status = status_code in RESPONSE_STATUS_CODE

        if isinstance(content, dict):
            # Determine the response code and message
            response_code = content.pop(
                ResponseEnum.RESPONSE_KEY.RESPONSE_CODE.response_key,
                ResponseEnum.RESPONSE_KEY.SUCCESS.response_key if result_status else ResponseEnum.RESPONSE_KEY.ERRORS.response_key
            )
            message = content.pop(
                ResponseEnum.RESPONSE_KEY.MESSAGE.response_key,
                "Operation successful!" if result_status else "An error occurred"
            )
        else:
            response_code = ResponseEnum.RESPONSE_KEY.SUCCESS.response_key if result_status else ResponseEnum.RESPONSE_KEY.ERRORS.response_key
            message = "Operation successful!" if result_status else "An error occurred"

        # Create the results schema
        results_dict = APIBaseResultSchema.create(
            status=result_status,
            request_id=request_id,
            content=content if bool(content) else None
        ).dict()

        # Reconstruct the APIBaseResultSchema object from the filtered dictionary
        filtered_results = APIBaseResultSchema(**results_dict)

        # Construct the APIBaseResponse
        response = cls(
            status_code=status_code,
            response_code=response_code,
            message=message,
            results=filtered_results
        )

        response_dict = response.dict()

        # Remove keys based on the status
        if result_status:
            response_dict[ResponseEnum.RESPONSE_KEY.RESULTS.response_key].pop(ResponseEnum.RESPONSE_KEY.ERRORS.response_key, None)
        else:
            response_dict[ResponseEnum.RESPONSE_KEY.RESULTS.response_key].pop(ResponseEnum.RESPONSE_KEY.SUCCESS.response_key, None)

        # Return the JSON representation of the response
        return response_dict
