import json
import uuid
from time import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from fastapi_easystart.helpers.logger import log


class RequestMiddleware(BaseHTTPMiddleware):
    """
    Middleware class to handle request ID generation, logging, and request timing.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Start time for request timing
        start_time = time()

        # Add a unique request ID and process the request
        response = await self.add_request_id_middleware(request, call_next)

        # Calculate processing time and modify response
        response = await self.calculate_request_timing(response, start_time)

        return response

    @staticmethod
    async def add_request_id_middleware(request: Request, call_next: Callable) -> Response:
        """
        Middleware function to generate and set a unique request ID, and process the request.

        :param request: The incoming request object.
        :param call_next: The next middleware or route handler to call.
        :return: The response object with the request ID header set.
        """
        # Generate a unique request ID
        request_id = str(uuid.uuid4())

        try:
            # Set the request ID in the request state for later access
            request.state.request_id = request_id
        except Exception as ex:
            # Handle exceptions if setting request ID fails
            log.error(f"Request failed while setting request ID: {ex}", extra={"request_id": request_id})
            request_id = request.headers.get("X-Request-ID", request_id)

        # Process the request
        response = await call_next(request)

        # Add the request ID to the response headers
        response.headers["X-Request-ID"] = request_id

        return response

    @staticmethod
    async def calculate_request_timing(response: Response, start_time: float) -> Response:
        """
        Calculate the processing time for the request and modify the response.

        :param response: The response object.
        :param start_time: The start time of the request.
        :return: The modified response object.
        """
        process_time = time() - start_time

        if isinstance(response, JSONResponse):
            response_data = response.body.decode("utf-8")
            response_data = json.loads(response_data)
            response_data['process_time'] = f"{process_time:.4f} seconds"
            response.body = json.dumps(response_data).encode("utf-8")

        response.headers["X-Process-Time"] = str(process_time)
        return response
