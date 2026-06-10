from fastapi import FastAPI

from app.config.db import (
    Base,
    engine
)

from app.api.patient_routes import (
    router as patient_router
)

from app.api.hospital_routes import (
    router as hospital_router
)

from app.api.admission_routes import (
    router as admission_router
)

# Import models so SQLAlchemy registers them
from app.models.patient import Patient
from app.models.hospital import Hospital
from app.models.association import patient_hospital

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Patient Management API"
)

app.include_router(patient_router)
app.include_router(hospital_router)
app.include_router(admission_router)