from contextlib import asynccontextmanager
from time import perf_counter
from typing import AsyncIterator

from app.core.logging import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def trace_span(name: str, **attributes: object) -> AsyncIterator[None]:
    start = perf_counter()
    logger.info("span_start", span=name, **attributes)
    try:
        yield
    finally:
        logger.info("span_end", span=name, elapsed_seconds=perf_counter() - start, **attributes)

