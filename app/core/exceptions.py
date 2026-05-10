from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse

from app.core.logging import get_logger

logger = get_logger(__name__)


class AppError(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def install_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError) -> ORJSONResponse:
        return ORJSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception) -> ORJSONResponse:
        logger.exception("unhandled_error", path=request.url.path, error=str(exc))
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )

