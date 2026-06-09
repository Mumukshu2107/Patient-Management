from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app.models import Patient
from app.schemas import PatientCreate, PatientResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Patient Management API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/patients", response_model=PatientResponse)
def add_patient(
        patient: PatientCreate,
        db: Session = Depends(get_db)
):
    new_patient = Patient(
        name=patient.name,
        age=patient.age,
        contact_no=patient.contact_no,
        height=patient.height,
        weight=patient.weight,
        blood_group=patient.blood_group
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


@app.get("/patients", response_model=list[PatientResponse])
def get_patients(
        db: Session = Depends(get_db)
):
    return db.query(Patient).all()