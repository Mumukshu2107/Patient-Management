from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.db import get_db
from models import User

from app.schemas import (
    LoginRequest,
    TokenResponse
)

from app.security import (
    verify_password,
    create_access_token
)

from app.utils.logger import logger


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == credentials.username
    ).first()

    if not user:

        logger.warning(
            f"Invalid login attempt for username: "
            f"{credentials.username}"
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    password_valid = verify_password(
        credentials.password,
        user.password
    )

    if not password_valid:

        logger.warning(
            f"Invalid password attempt for user: "
            f"{credentials.username}"
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        {
            "sub": user.username,
            "role": user.role,
            "user_id": user.id
        }
    )

    logger.info(
        f"User '{user.username}' logged in successfully "
        f"with role '{user.role}'"
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }