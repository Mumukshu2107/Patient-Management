from fastapi import FastAPI

from config.db import Base, engine

# Import models so SQLAlchemy can detect tables
from models import (
    Patient,
    Hospital,
    patient_hospital
)

# Import API router
from app.api import router


# Create all tables if they do not exist
Base.metadata.create_all(bind=engine)


# FastAPI application
app = FastAPI(
    title="Patient Management API",
    version="1.0.0"
)


# Register all APIs
app.include_router(router)