from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.db import SessionLocal

from app.models.hospital import Hospital

from app.schemas.hospital_schema import (
    HospitalCreate,
    HospitalResponse
)

router = APIRouter(
    tags=["Hospitals"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# ADD HOSPITAL
# -------------------------

@router.post(
    "/hospitals",
    response_model=HospitalResponse
)
def add_hospital(
        hospital: HospitalCreate,
        db: Session = Depends(get_db)
):

    new_hospital = Hospital(
        **hospital.model_dump()
    )

    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital)

    return new_hospital


# -------------------------
# GET ALL HOSPITALS
# -------------------------

@router.get(
    "/hospitals",
    response_model=list[HospitalResponse]
)
def get_hospitals(
        db: Session = Depends(get_db)
):

    return db.query(Hospital).all()


# -------------------------
# GET PATIENTS OF HOSPITAL
# -------------------------

@router.get(
    "/hospitals/{hospital_id}/patients"
)
def get_hospital_patients(
        hospital_id: int,
        db: Session = Depends(get_db)
):

    hospital = db.query(Hospital).filter(
        Hospital.id == hospital_id
    ).first()

    if not hospital:
        raise HTTPException(
            status_code=404,
            detail="Hospital not found"
        )

    return {
        "hospital_id": hospital.id,
        "hospital_name": hospital.name,
        "city": hospital.city,
        "patients": [
            {
                "id": patient.id,
                "name": patient.name,
                "age": patient.age,
                "blood_group": patient.blood_group,
                "status": patient.status
            }
            for patient in hospital.patients
        ]
    }