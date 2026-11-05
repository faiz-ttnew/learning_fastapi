import logging
from time import perf_counter

from fastapi import Request


logger = logging.getLogger("uvicorn.error")


async def log_requests(request: Request, call_next):
    start_time = perf_counter()

    logger.info(
        "Request started: %s %s",
        request.method,
        request.url.path
    )

    try:
        response = await call_next(request)

    except Exception:
        duration = perf_counter() - start_time

        logger.error(
            "Request failed: %s %s duration=%.4fs",
            request.method,
            request.url.path,
            duration
        )

        raise

    duration = perf_counter() - start_time

    response.headers["X-Process-Time"] = f"{duration:.6f}"

    logger.info(
        "Request completed: %s %s status=%s duration=%.4fs",
        request.method,
        request.url.path,
        response.status_code,
        duration
    )

    return response
