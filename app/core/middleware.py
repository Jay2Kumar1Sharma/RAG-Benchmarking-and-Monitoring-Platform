import time
import uuid
from collections.abc import Awaitable, Callable

import structlog.contextvars
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.observability.metrics import REQUEST_LATENCY, REQUESTS_TOTAL


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
        start = time.perf_counter()
        structlog.contextvars.bind_contextvars(request_id=request_id, path=request.url.path)
        try:
            response = await call_next(request)
        finally:
            elapsed = time.perf_counter() - start
            REQUEST_LATENCY.labels(method=request.method, path=request.url.path).observe(elapsed)
            REQUESTS_TOTAL.labels(method=request.method, path=request.url.path).inc()
            structlog.contextvars.clear_contextvars()
        response.headers["x-request-id"] = request_id
        return response

