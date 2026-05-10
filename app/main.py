from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app.api.router import api_router
from app.core.config import get_settings
from app.core.exceptions import install_exception_handlers
from app.core.logging import configure_logging, get_logger
from app.core.middleware import RequestContextMiddleware
from app.observability.metrics import metrics_router

settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    configure_logging(settings.log_level)
    logger.info("application_starting", app=settings.app_name, environment=settings.app_env)
    yield
    logger.info("application_stopped", app=settings.app_name)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )
    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    install_exception_handlers(app)
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    app.include_router(metrics_router)
    return app


app = create_app()

