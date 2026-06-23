from starlette.middleware.base import BaseHTTPMiddleware

from app.security import decode_access_token

from app.utils.logger import logger


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        public_paths = [
            "/auth/login",
            "/docs",
            "/redoc",
            "/openapi.json"
        ]

        if request.url.path in public_paths:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):

            token = auth_header.split(" ")[1]

            payload = decode_access_token(token)

            if payload:

                request.state.user_id = payload.get("user_id")
                request.state.username = payload.get("sub")
                request.state.role = payload.get("role")

                logger.info(
                    f"Authenticated user: "
                    f"{payload.get('sub')}"
                )

        response = await call_next(request)

        return response