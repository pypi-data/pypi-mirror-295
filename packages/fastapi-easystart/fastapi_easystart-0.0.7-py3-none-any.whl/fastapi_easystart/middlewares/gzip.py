import io
from gzip import GzipFile

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class CustomGZipMiddleware(BaseHTTPMiddleware):
    """
    Middleware for compressing HTTP responses using gzip.

    This middleware compresses responses based on their content type and size.
    Responses that exceed the minimum size threshold for their content type will
    be compressed.

    Attributes:
        min_size_text (int): Minimum size (in bytes) for compressing text responses.
        min_size_json (int): Minimum size (in bytes) for compressing JSON responses.
        min_size_other (int): Minimum size (in bytes) for compressing other types of responses.

    Example Usage:
        from fastapi import FastAPI
        from  fastapi_easystart.middlewares.gzip from CustomGZipMiddleware  # Import the middleware from your module

        app = FastAPI()

        # Add the CustomGZipMiddleware to the application
        app.add_middleware(
            CustomGZipMiddleware,
            min_size_text=5000,  # Minimum size (in bytes) for compressing text responses
            min_size_json=5000,  # Minimum size (in bytes) for compressing JSON responses
            min_size_other=5000  # Minimum size (in bytes) for compressing other types of responses
        )

        @app.get("/example")
        async def example_endpoint():
            # This response will be compressed if it meets the size threshold
            return {"message": "This is an example response that might be compressed."}

        @app.get("/text")
        async def text_endpoint():
            # This endpoint returns a long text response
            return "a" * 6000  # Response will be compressed because it's larger than 5000 bytes

    How It Works:
        - The `dispatch` method intercepts the HTTP response after it is generated.
        - It checks the response body and content type.
        - If the body size exceeds the defined minimum size for its content type, it compresses the body using gzip.
        - The compressed response is then returned to the client.

    Args:
        app: The ASGI application to be wrapped by this middleware.
        min_size_text (int): Minimum size (in bytes) for compressing text responses. Default is 10000.
        min_size_json (int): Minimum size (in bytes) for compressing JSON responses. Default is 10000.
        min_size_other (int): Minimum size (in bytes) for compressing other types of responses. Default is 10000.
    """

    def __init__(self, app, min_size_text=10000, min_size_json=10000, min_size_other=10000):
        """
        Initializes the middleware with specified minimum sizes for different content types.

        Args:
            app: The ASGI application to be wrapped by this middleware.
            min_size_text (int): Minimum size (in bytes) for compressing text responses.
            min_size_json (int): Minimum size (in bytes) for compressing JSON responses.
            min_size_other (int): Minimum size (in bytes) for compressing other types of responses.
        """
        super().__init__(app)
        self.min_size_text = min_size_text
        self.min_size_json = min_size_json
        self.min_size_other = min_size_other

    async def dispatch(self, request: Request, call_next):
        """
        Processes the incoming request and handles the response compression if needed.

        Args:
            request (Request): The incoming HTTP request.
            call_next: The next middleware or endpoint to handle the request.

        Returns:
            Response: The HTTP response, potentially compressed.
        """
        response = await call_next(request)
        body = await response.body()
        content_type = response.headers.get('content-type', '')

        if not body:
            return response

        if 'application/json' in content_type:
            min_size = self.min_size_json
        elif 'text/' in content_type:
            min_size = self.min_size_text
        else:
            min_size = self.min_size_other

        if len(body) >= min_size:
            compressed_body = self._compress(body)
            return Response(
                content=compressed_body,
                headers=dict(response.headers),
                status_code=response.status_code,
                media_type=response.media_type
            )

        return response

    @staticmethod
    def _compress(data: bytes) -> bytes:
        """
        Compresses the given byte data using gzip.

        Args:
            data (bytes): The byte data to be compressed.

        Returns:
            bytes: The compressed byte data.
        """
        buffer = io.BytesIO()
        with GzipFile(fileobj=buffer, mode='wb') as gz:
            gz.write(data)
        return buffer.getvalue()
