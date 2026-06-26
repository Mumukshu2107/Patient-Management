from starlette.middleware.base import BaseHTTPMiddleware
from app.tasks.log_tasks import send_log
from app.utils.logger import logger
import time

class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        send_log({
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code
        })

        return response