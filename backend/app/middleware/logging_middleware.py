import time
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.logger import logger

class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        logger.info(
            f"{request.method} "
            f"{request.url.path} "
            f"Status={response.status_code} "
            f"Time={process_time:.4f}s"
        )

        return response