from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.db import Base, engine

from models import (
    User,
    Patient,
    Hospital,
    patient_hospital
)

from app.api import router
from app.routers.auth import router as auth_router

# NEW IMPORTS
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.auth_middleware import AuthMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Patient Management API",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware)

# Routers
app.include_router(router)
app.include_router(auth_router)