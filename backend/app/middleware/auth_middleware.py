from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from config.db import SessionLocal
from models import User

from app.security import decode_access_token
from app.utils.logger import logger


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        if request.method == "OPTIONS":
            return await call_next(request)

        public_paths = [
            "/auth/login",
            "/docs",
            "/redoc",
            "/openapi.json"
        ]

        if request.url.path in public_paths:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Authorization token missing"
                }
            )

        token = auth_header.split(" ")[1]

        payload = decode_access_token(token)

        if not payload:
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Invalid token"
                }
            )

        username = payload.get("sub")

        db = SessionLocal()

        try:
            user = db.query(User).filter(
                User.username == username
            ).first()

            if not user:
                return JSONResponse(
                    status_code=401,
                    content={
                        "detail": "User not found"
                    }
                )

            request.state.user = user
            request.state.user_id = user.id
            request.state.username = user.username
            request.state.role = user.role

        finally:
            db.close()

        response = await call_next(request)

        return response