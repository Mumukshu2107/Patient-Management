from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.db import SessionLocal

from models import (
    Patient,
    Hospital,
    patient_hospital
)

from app.schemas import (
    PatientCreate,
    PatientResponse,
    HospitalCreate,
    HospitalResponse,
    PatientHospitalLink
)
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/patients", response_model=PatientResponse)
def add_patient(
        patient: PatientCreate,
        db: Session = Depends(get_db)
):

    new_patient = Patient(**patient.model_dump())

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


@router.get("/patients", response_model=list[PatientResponse])
def get_patients(
        db: Session = Depends(get_db)
):
    return db.query(Patient).all()

@router.post("/hospitals", response_model=HospitalResponse)
def add_hospital(
        hospital: HospitalCreate,
        db: Session = Depends(get_db)
):

    new_hospital = Hospital(**hospital.model_dump())

    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital)

    return new_hospital


@router.get("/hospitals", response_model=list[HospitalResponse])
def get_hospitals(
        db: Session = Depends(get_db)
):
    return db.query(Hospital).all()

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

    if patient.status == 1:
        raise HTTPException(
            status_code=400,
            detail=f"Patient is already admitted in Hospital ID {patient.current_hospital_id}. Discharge first."
        )

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
        "admit_time": admit_time.strftime("%Y-%m-%d %H:%M:%S"),
        "previously_visited": already_visited
    }

@router.post("/patients/{patient_id}/discharge")
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

    return {
        "message": "Patient discharged successfully",
        "patient_id": patient.id,
        "patient_name": patient.name,
        "hospital_id": hospital_id,
        "discharge_time": discharge_time.strftime("%Y-%m-%d %H:%M:%S")
    }

@router.get("/patients/{patient_id}/hospitals")
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

        hospital_status = 0

        if (
            patient.status == 1 and
            patient.current_hospital_id == hospital.id
        ):
            hospital_status = 1

        hospitals_list.append({
            "hospital_id": hospital.id,
            "hospital_name": hospital.name,
            "status": hospital_status,
            "admit_time": (
                record.admit_time.strftime("%Y-%m-%d %H:%M:%S")
                if record.admit_time
                else None
            ),
            "discharge_time": (
                record.discharge_time.strftime("%Y-%m-%d %H:%M:%S")
                if record.discharge_time
                else "Patient yet to be discharged"
            )
        })

    return {
        "patient_id": patient.id,
        "patient_name": patient.name,
        "hospital_history": hospitals_list
    }

@router.get("/hospitals/{hospital_id}/patients")
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