from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse

from fastapi_easystart.messages import printer
from fastapi_easystart.schemas.response import APIBaseResponse
from fastapi_easystart.utils.config import ResponseHeaderTypeEnum

EXAMPLE_DOCS = """
# FastAPI EasyStart - Code Sample

from fastapi import Request, APIRouter
from fastapi_easystart.responses import APIResponse

router = APIRouter()

@router.get("/")
async def sample_code(request: Request):
    return APIResponse(request=request, content={"message": "Hello FastAPI"})
"""


class APIResponse(JSONResponse):
    """
    Custom response class for FastAPI that formats the response content
    according to the `APIBaseResponse` schema.

    This class extends FastAPI's `JSONResponse` to include additional formatting
    for API responses, specifically structuring the response content to include
    metadata such as a request ID.

    Args:
        request (Request): The FastAPI request object to extract request-specific information.
        content (Any): The main content to be included in the response body.
        status_code (int, optional): HTTP status code for the response. Defaults to 200.
        **kwargs: Additional keyword arguments passed to the `JSONResponse` initializer.

    Attributes:
        request_id (str): A unique identifier for the request, extracted from the request state or headers.
    """

    def __init__(self, request: Request, content: Any = None, status_code: int = 200, **kwargs):
        if not isinstance(request, Request):
            printer.error(
                title="APIResponse Error",
                details=[
                    "The request parameter must be an instance of FastAPI Request.",
                    "This indicates that the provided parameter does not meet the expected type requirement.",
                    "Ensure that you are passing the correct type of parameter as expected by the API endpoint.",
                ],
                advice=f"Verify the parameter being passed to the API endpoint and ensure it is an instance of FastAPI Request.\n{EXAMPLE_DOCS}"
            )
            # Raise an exception to prevent further execution
            raise TypeError("The 'request' parameter must be an instance of FastAPI Request.")

        # Extract request ID from request state or headers
        request_id = getattr(request.state, 'request_id')

        # Add custom header
        headers = {"response-type": ResponseHeaderTypeEnum.APIResponse.value}

        # Structure the response content using APIBaseResponse schema
        response_content = APIBaseResponse.get_structure_results(
            status_code=status_code,
            content=content,
            request_id=request_id if request_id else None,
        )

        # Initialize the JSONResponse with the structured content
        super().__init__(content=response_content, status_code=status_code, headers=headers, **kwargs)
