from typing import Any, Tuple

from fastapi import Request
from fastapi.responses import Response, StreamingResponse
from fastapi_easystart.helpers.encoding import bytes_to_dict, decompress_gzip
from fastapi_easystart.messages import printer
from fastapi_easystart.utils.config import ResponseHeaderTypeEnum
from starlette.middleware.base import BaseHTTPMiddleware


class BaseAPIResponseHTTPMiddleware(BaseHTTPMiddleware):

    async def determine_content_type(self, content_type, response_data: Response) -> Tuple[bool, Any]:
        try:
            charset = response_data.charset

            # Check for content encoding (e.g., gzip)
            content_encoding = response_data.headers.get('content-encoding', '')

            if response_data.media_type is None:
                if content_type == 'application/json':
                    body_content = await self._read_response_content(response_data)
                    if content_encoding == 'gzip':
                        body_content = decompress_gzip(body_content)
                    content = bytes_to_dict(body_content, charset)
                    return False, content if content else body_content

                return True, response_data
            else:
                body_content = await self._read_response_content(response_data)
                if content_encoding == 'gzip':
                    body_content = decompress_gzip(body_content)
                content = bytes_to_dict(body_content, charset)
                return True, content if content else body_content
        except Exception as e:
            return True, {"error": str(e)}

    @staticmethod
    def determine_default_response_return(request: Request, content_type: str, response_data: Response) -> bool:
        content_encoding = response_data.headers.get('content-encoding', '')
        response_type = response_data.headers.get('response-type', None)
        is_json = content_type == 'application/json'
        is_gzip = content_encoding == 'gzip'
        is_api_response = response_type == ResponseHeaderTypeEnum.APIResponse.value

        # If the content type is not application/json or the URL path matches the openapi_url, return the original response
        if not is_json or request.url.path == request.app.openapi_url:
            return True

        # Handle cases where the response is an APIResponse
        if is_api_response:
            if is_gzip:
                printer.warning(
                    title="GZipMiddleware Warning",
                    advice="Please review your app settings and make the necessary adjustments.",
                    details=[
                        "It looks like the response is too large for our gzip compression settings.",
                    ],
                )
            return True

        # Handle cases where the response is not an APIResponse but is gzip-compressed JSON
        if is_gzip and is_json:
            printer.warning(
                title="GZipMiddleware Warning",
                advice="Please review your app settings and make the necessary adjustments.",
                details=[
                    "It looks like the response is too large for our gzip compression settings.",
                    "We were unable to process the API base response because it exceeds the allowed size.",
                    "This might lead to issues such as missing API base responses or display of white screens.",
                    "To resolve this, you can use 'from fastapi_easystart.responses import APIResponse'.",
                    "Alternatively, increase the `minimum_size` setting in GZipMiddleware."
                ],
            )
            return True

        return False

    @staticmethod
    async def _read_streaming_response(response_data: StreamingResponse) -> bytes:
        """Reads and collects content from StreamingResponse."""
        body_content = b''.join([chunk async for chunk in response_data.body_iterator])
        return body_content

    @staticmethod
    async def _read_response_content(response_data: Response) -> bytes:
        """Reads and collects content from any Response."""
        body_content = b''
        if hasattr(response_data, 'body_iterator'):
            async for chunk in response_data.body_iterator:
                body_content += chunk
        else:
            body_content = await response_data.body()
        return body_content
