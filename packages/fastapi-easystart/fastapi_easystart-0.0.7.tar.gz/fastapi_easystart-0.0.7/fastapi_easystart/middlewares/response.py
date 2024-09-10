import json

from fastapi import Request
from fastapi.responses import Response
from starlette.middleware.base import RequestResponseEndpoint

from fastapi_easystart.middlewares.base import BaseAPIResponseHTTPMiddleware
from fastapi_easystart.schemas.response import APIBaseResponse


class CustomBaseHTTPMiddleware(BaseAPIResponseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response_data = await call_next(request)
        content_type = response_data.headers.get('content-type', '')

        is_default_response_return = self.determine_default_response_return(request=request, content_type=content_type, response_data=response_data)
        if is_default_response_return:
            return response_data

        request_id = getattr(request.state, 'request_id', response_data.headers.get('x-request-id'))
        try:
            status_code = response_data.status_code
            is_binary_content, body_content = await self.determine_content_type(content_type=content_type, response_data=response_data)
            if is_binary_content:
                response_headers = dict(response_data.headers)
                response_headers.pop('content-length', None)  # Remove Content-Length

                return Response(
                    content=body_content,
                    status_code=status_code,
                    headers=response_headers,
                    media_type=response_data.media_type
                )

            response_content = APIBaseResponse.get_structure_results(status_code, request_id, body_content)
            response_headers = dict(response_data.headers)
            response_headers.pop('content-length', None)  # Remove Content-Length

            return Response(
                content=json.dumps(response_content),
                media_type="application/json",
                status_code=status_code,
                headers=response_headers
            )

        except Exception as e:
            error_response = APIBaseResponse.get_structure_results(
                status_code=500,
                request_id=request_id,
                content={
                    "message": "Oops! An unresolved exception occurred.",
                    "detail": str(e),
                }
            )
            response_headers = dict(response_data.headers)
            response_headers.pop('content-length', None)  # Remove Content-Length

            return Response(
                content=json.dumps(error_response),
                media_type="application/json",
                status_code=500,
                headers=response_headers
            )
