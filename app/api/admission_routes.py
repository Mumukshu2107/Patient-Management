from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.db import SessionLocal

from app.models.patient import Patient
from app.models.hospital import Hospital
from app.models.association import patient_hospital

from app.schemas.admission_schema import (
    PatientHospitalLink
)

router = APIRouter(
    tags=["Admissions"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# ASSIGN / ADMIT PATIENT
# -------------------------

@router.post("/assign-hospital")
def assign_hospital(
        data: PatientHospitalLink,
        db: Session = Depends(get_db)
):

    patient = db.query(Patient).filter(
        Patient.id == data.patient_id
    ).first()

    hospital = db.query(Hospital).filter(
        Hospital.id == data.hospital_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    if not hospital:
        raise HTTPException(
            status_code=404,
            detail="Hospital not found"
        )

    # Patient already admitted
    if patient.status == 1:
        raise HTTPException(
            status_code=400,
            detail=f"Patient is already admitted in Hospital ID {patient.current_hospital_id}. Discharge first."
        )

    # Check if hospital already exists in history
    already_visited = hospital in patient.hospitals

    if not already_visited:
        patient.hospitals.append(hospital)

    admit_time = datetime.now()

    db.execute(
        patient_hospital.update()
        .where(
            patient_hospital.c.patient_id == patient.id,
            patient_hospital.c.hospital_id == hospital.id
        )
        .values(
            admit_time=admit_time,
            discharge_time=None
        )
    )

    patient.status = 1
    patient.current_hospital_id = hospital.id

    db.commit()
    db.refresh(patient)

    return {
        "message": "Patient admitted successfully",
        "patient_id": patient.id,
        "patient_name": patient.name,
        "hospital_id": hospital.id,
        "hospital_name": hospital.name,
        "admit_time": admit_time.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "previously_visited": already_visited
    }


# -------------------------
# DISCHARGE PATIENT
# -------------------------

@router.post(
    "/patients/{patient_id}/discharge"
)
def discharge_patient(
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

    if patient.status == 0:
        raise HTTPException(
            status_code=400,
            detail="Patient is already discharged"
        )

    hospital_id = patient.current_hospital_id

    discharge_time = datetime.now()

    db.execute(
        patient_hospital.update()
        .where(
            patient_hospital.c.patient_id == patient.id,
            patient_hospital.c.hospital_id == hospital_id
        )
        .values(
            discharge_time=discharge_time
        )
    )

    patient.status = 0
    patient.current_hospital_id = None

    db.commit()
    db.refresh(patient)

    return {
        "message": "Patient discharged successfully",
        "patient_id": patient.id,
        "patient_name": patient.name,
        "hospital_id": hospital_id,
        "discharge_time": discharge_time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }