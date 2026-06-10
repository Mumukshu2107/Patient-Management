from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.db import SessionLocal
from app.models.patient import Patient
from app.models.hospital import Hospital
from app.models.association import patient_hospital

from app.schemas.patient_schema import (
    PatientCreate,
    PatientResponse
)

router = APIRouter(
    tags=["Patients"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# ADD PATIENT
# -------------------------

@router.post(
    "/patients",
    response_model=PatientResponse
)
def add_patient(
        patient: PatientCreate,
        db: Session = Depends(get_db)
):

    new_patient = Patient(
        **patient.model_dump()
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


# -------------------------
# GET ALL PATIENTS
# -------------------------

@router.get(
    "/patients",
    response_model=list[PatientResponse]
)
def get_patients(
        db: Session = Depends(get_db)
):

    return db.query(Patient).all()


# -------------------------
# GET PATIENT HOSPITAL HISTORY
# -------------------------

@router.get(
    "/patients/{patient_id}/hospitals"
)
def get_patient_hospitals(
        patient_id: int,
        db: Session = Depends(get_db)
):

    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    hospital_history = db.execute(
        patient_hospital.select().where(
            patient_hospital.c.patient_id == patient_id
        )
    ).fetchall()

    hospitals_list = []

    for record in hospital_history:

        hospital = db.query(Hospital).filter(
            Hospital.id == record.hospital_id
        ).first()

        hospital_status = (
            1
            if patient.status == 1
            and patient.current_hospital_id == hospital.id
            else 0
        )

        hospitals_list.append({
            "hospital_id": hospital.id,
            "hospital_name": hospital.name,
            "status": hospital_status,
            "admit_time": (
                record.admit_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if record.admit_time
                else None
            ),
            "discharge_time": (
                record.discharge_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if record.discharge_time
                else None
            )
        })

    return {
        "patient_id": patient.id,
        "patient_name": patient.name,
        "hospital_history": hospitals_list
    }