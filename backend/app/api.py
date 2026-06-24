from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session
from config.db import SessionLocal
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
    Request
)
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer

from models import (
    Patient,
    Hospital,
    patient_hospital,
    User,
    UserRole
)
from app.schemas import (
    PatientCreate,
    PatientResponse,
    HospitalCreate,
    HospitalResponse,
    PatientHospitalLink,
    SearchRequest
)
import pandas as pd
import io

from difflib import get_close_matches

from app.schemas import (
    UserCreate,
    UserResponse
)
from app.security import (
    # get_current_user,
    hash_password,
    verify_password,
    create_access_token
)
from app.schemas import (
    LoginRequest,
    TokenResponse
)
from app.utils.logger import logger
from app.security import decode_access_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/patients",
    response_model=PatientResponse
)
def add_patient(
        patient: PatientCreate,
        request: Request,
        db: Session = Depends(get_db)
):

    require_receptionist(request)

    new_patient = Patient(
        **patient.model_dump()
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


def require_super_admin(request: Request):

    if request.state.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Only Super Admin can perform this action"
        )

    return request.state.user


def require_admin(request: Request):

    if request.state.role not in [
        UserRole.SUPER_ADMIN,
        UserRole.ADMIN
    ]:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return request.state.user


def require_doctor(request: Request):

    if request.state.role not in [
        UserRole.SUPER_ADMIN,
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.RECEPTIONIST
    ]:
        raise HTTPException(
            status_code=403,
            detail="Doctor access required"
        )

    return request.state.user


def require_receptionist(request: Request):

    if request.state.role not in [
        UserRole.SUPER_ADMIN,
        UserRole.ADMIN,
        UserRole.RECEPTIONIST
    ]:
        raise HTTPException(
            status_code=403,
            detail="Receptionist access required"
        )

    return request.state.user


@router.get(
    "/patients",
    response_model=list[PatientResponse]
)
def get_patients(
        request: Request,
        db: Session = Depends(get_db)
):

    require_doctor(request)

    return db.query(Patient).all()

@router.post(
    "/hospitals",
    response_model=HospitalResponse
)
def add_hospital(
        hospital: HospitalCreate,
        request: Request,
        db: Session = Depends(get_db)
):

    current_user = require_admin(request)

    existing_hospital = db.query(Hospital).filter(
        Hospital.name.ilike(hospital.name),
        Hospital.city.ilike(hospital.city)
    ).first()

    if existing_hospital:
        raise HTTPException(
            status_code=400,
            detail=f"Hospital '{hospital.name}' already exists in {hospital.city}"
        )

    new_hospital = Hospital(
        **hospital.model_dump()
    )

    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital)

    logger.info(
        f"{current_user.username} added hospital "
        f"{new_hospital.name}"
    )

    return new_hospital


@router.get(
    "/hospitals",
    response_model=list[HospitalResponse]
)
def get_hospitals(
        request: Request,
        db: Session = Depends(get_db)
):

    current_user = request.state.user

    logger.info(
        f"{current_user.username} viewed hospitals"
    )

    return db.query(Hospital).all()

@router.post("/assign-hospital")
def assign_hospital(
        data: PatientHospitalLink,
        request: Request,
        db: Session = Depends(get_db)
):

    current_user = require_receptionist(request)

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
            detail=(
                f"Patient is already admitted in "
                f"Hospital ID {patient.current_hospital_id}. "
                f"Discharge first."
            )
        )

    already_visited = hospital in patient.hospitals

    if not already_visited:
        patient.hospitals.append(hospital)

    db.flush()

    admit_time = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

    result = db.execute(
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

    print("Rows Updated:", result.rowcount)
    print("Admit Time:", admit_time)

    patient.status = 1
    patient.current_hospital_id = hospital.id

    db.commit()
    db.refresh(patient)

    logger.info(
        f"{current_user.username} admitted "
        f"patient {patient.name} "
        f"to hospital {hospital.name}"
    )

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

@router.post("/patients/{patient_id}/discharge")
def discharge_patient(
        patient_id: int,
        request: Request,
        db: Session = Depends(get_db)
):

    current_user = require_receptionist(request)

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

    discharge_time = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

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

    logger.info(
        f"{current_user.username} discharged "
        f"patient {patient.name}"
    )

    return {
        "message": "Patient discharged successfully",
        "patient_id": patient.id,
        "patient_name": patient.name,
        "hospital_id": hospital_id,
        "discharge_time": discharge_time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }
@router.get("/patients/{patient_id}/hospitals")
def get_patient_hospitals(
        patient_id: int,
        request: Request,
        db: Session = Depends(get_db)
):

    current_user = require_doctor(request)

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
            "hospital_city": hospital.city,
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

    logger.info(
        f"{current_user.username} viewed "
        f"hospital history of patient {patient.id}"
    )

    return {
        "patient_id": patient.id,
        "patient_name": patient.name,
        "hospital_history": hospitals_list
    }
@router.get("/hospitals/{hospital_id}/patients")
def get_hospital_patients(
        hospital_id: int,
        request: Request,
        db: Session = Depends(get_db)
):

    current_user = require_doctor(request)

    hospital = db.query(Hospital).filter(
        Hospital.id == hospital_id
    ).first()

    if not hospital:
        raise HTTPException(
            status_code=404,
            detail="Hospital not found"
        )

    logger.info(
        f"{current_user.username} viewed "
        f"patients of hospital {hospital.name}"
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

@router.get("/search/patient")
def search_patient(
        search_by: str,
        search_text: str,
        request: Request,
        db: Session = Depends(get_db)
):

    current_user = require_doctor(request)

    search_by = search_by.lower()

    # =====================================
    # SEARCH BY PATIENT NAME
    # =====================================

    if search_by == "name":

        patients = db.query(Patient).all()

        matched_patients = []

        for patient in patients:

            if search_text.lower() in patient.name.lower():

                matched_patients.append({
                    "id": patient.id,
                    "name": patient.name,
                    "age": patient.age,
                    "contact_no": patient.contact_no,
                    "height": patient.height,
                    "weight": patient.weight,
                    "blood_group": patient.blood_group,
                    "status": patient.status
                })

        if matched_patients:

            logger.info(
                f"{current_user.username} searched patient "
                f"by name: {search_text}"
            )

            return {
                "match_found": True,
                "patients": matched_patients
            }

        patient_names = [
            patient.name
            for patient in patients
        ]

        suggestions = get_close_matches(
            search_text,
            patient_names,
            n=5,
            cutoff=0.5
        )

        suggested_patients = []

        for patient in patients:

            if patient.name in suggestions:

                suggested_patients.append({
                    "id": patient.id,
                    "name": patient.name,
                    "age": patient.age,
                    "contact_no": patient.contact_no,
                    "height": patient.height,
                    "weight": patient.weight,
                    "blood_group": patient.blood_group,
                    "status": patient.status
                })

        return {
            "match_found": False,
            "message": "No exact match found",
            "did_you_mean": suggestions,
            "patients": suggested_patients
        }

    # =====================================
    # SEARCH BY CONTACT NUMBER
    # =====================================

    elif search_by == "contact_no":

        patients = db.query(Patient).filter(
            Patient.contact_no == search_text
        ).all()

        if not patients:
            return {
                "match_found": False,
                "message": "No patient found"
            }

        logger.info(
            f"{current_user.username} searched "
            f"patient by contact number"
        )

        return {
            "match_found": True,
            "patients": [
                {
                    "id": patient.id,
                    "name": patient.name,
                    "age": patient.age,
                    "contact_no": patient.contact_no,
                    "height": patient.height,
                    "weight": patient.weight,
                    "blood_group": patient.blood_group,
                    "status": patient.status
                }
                for patient in patients
            ]
        }

    else:
        raise HTTPException(
            status_code=400,
            detail="search_by must be name or contact_no"
        )

@router.post("/upload-data")
async def upload_data(
        request: Request,
        entity_type: str = Form(...),
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):

    current_user = require_admin(request)

    df = pd.read_csv(file.file)

    inserted_count = 0

    # -------------------
    # PATIENT UPLOAD
    # -------------------

    if entity_type.lower() == "patient":

        required_columns = [
            "name",
            "age",
            "contact_no",
            "height",
            "weight",
            "blood_group"
        ]

        for col in required_columns:

            if col not in df.columns:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing column: {col}"
                )

        for _, row in df.iterrows():

            existing_patient = db.query(Patient).filter(
                Patient.name == row["name"],
                Patient.age == row["age"],
                Patient.contact_no == str(
                    row["contact_no"]
                )
            ).first()

            if existing_patient:
                continue

            patient = Patient(
                name=row["name"],
                age=int(row["age"]),
                contact_no=str(row["contact_no"]),
                height=float(row["height"]),
                weight=float(row["weight"]),
                blood_group=row["blood_group"]
            )

            db.add(patient)

            inserted_count += 1

        db.commit()

        logger.info(
            f"{current_user.username} uploaded "
            f"{inserted_count} patients"
        )

        return {
            "message": "Upload successful",
            "records_inserted": inserted_count
        }

    # -------------------
    # HOSPITAL UPLOAD
    # -------------------

    elif entity_type.lower() == "hospital":

        required_columns = [
            "name",
            "city"
        ]

        for col in required_columns:

            if col not in df.columns:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing column: {col}"
                )

        skipped_hospitals = []

        for _, row in df.iterrows():

            hospital_name = str(
                row["name"]
            ).strip()

            hospital_city = str(
                row["city"]
            ).strip()

            existing_hospital = db.query(
                Hospital
            ).filter(
                Hospital.name.ilike(
                    hospital_name
                ),
                Hospital.city.ilike(
                    hospital_city
                )
            ).first()

            if existing_hospital:

                skipped_hospitals.append({
                    "name": hospital_name,
                    "city": hospital_city,
                    "reason": "Already exists"
                })

                continue

            hospital = Hospital(
                name=hospital_name,
                city=hospital_city
            )

            db.add(hospital)

            inserted_count += 1

        db.commit()

        logger.info(
            f"{current_user.username} uploaded "
            f"{inserted_count} hospitals"
        )

        return {
            "message": "Upload completed",
            "records_inserted": inserted_count,
            "duplicate_records_skipped": len(
                skipped_hospitals
            ),
            "skipped_hospitals": skipped_hospitals
        }

    else:
        raise HTTPException(
            status_code=400,
            detail="entity_type must be patient or hospital"
        )

@router.get("/download/patients")
def download_patients(
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):

    patients = db.query(Patient).all()

    data = []

    for patient in patients:
        data.append({
            "id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "contact_no": patient.contact_no,
            "height": patient.height,
            "weight": patient.weight,
            "blood_group": patient.blood_group,
            "status": patient.status
        })

    df = pd.DataFrame(data)

    stream = io.StringIO()
    df.to_csv(stream, index=False)

    response = StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv"
    )

    response.headers[
        "Content-Disposition"
    ] = "attachment; filename=patients.csv"

    return response

@router.get("/download/hospitals")
def download_hospitals(
        request: Request,
        db: Session = Depends(get_db)
):

    current_user = require_admin(request)

    hospitals = db.query(Hospital).all()

    data = []

    for hospital in hospitals:
        data.append({
            "id": hospital.id,
            "name": hospital.name,
            "city": hospital.city
        })

    df = pd.DataFrame(data)

    stream = io.StringIO()

    df.to_csv(
        stream,
        index=False
    )

    response = StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv"
    )

    response.headers[
        "Content-Disposition"
    ] = "attachment; filename=hospitals.csv"

    logger.info(
        f"{current_user.username} downloaded hospitals CSV"
    )

    return response

# @router.post(
#     "/login",
#     response_model=TokenResponse
# )
# def login(
#         credentials: LoginRequest,
#         db: Session = Depends(get_db)
# ):
#
#     user = db.query(User).filter(
#         User.username == credentials.username
#     ).first()
#
#     if not user:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid username or password"
#         )
#
#     password_valid = verify_password(
#         credentials.password,
#         user.password
#     )
#
#     if not password_valid:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid username or password"
#         )
#
#     access_token = create_access_token(
#         {
#             "sub": user.username,
#             "role": user.role,
#             "user_id": user.id
#         }
#     )
#
#     return {
#         "access_token": access_token,
#         "token_type": "bearer"
#     }
@router.post(
    "/users",
    response_model=UserResponse
)
def create_user(
        user: UserCreate,
        request: Request,
        db: Session = Depends(get_db)
):

    current_user = require_super_admin(request)

    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = User(
        username=user.username,
        password=hash_password(
            user.password
        ),
        role=user.role.value
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(
        f"{current_user.username} created user "
        f"{new_user.username}"
    )

    return new_user

@router.get("/me")
def get_me(
        request: Request
):

    current_user = request.state.user

    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role
    }


@router.get("/users")
def get_users(
        request: Request,
        db: Session = Depends(get_db)
):

    current_user = require_super_admin(
        request
    )

    logger.info(
        f"{current_user.username} viewed users list"
    )

    return db.query(User).all()

@router.get("/dashboard")
def dashboard_stats(
        request: Request,
        db: Session = Depends(get_db)
):

    current_user = request.state.user

    total_patients = db.query(
        Patient
    ).count()

    total_hospitals = db.query(
        Hospital
    ).count()

    admitted_patients = db.query(
        Patient
    ).filter(
        Patient.status == 1
    ).count()

    discharged_patients = db.query(
        Patient
    ).filter(
        Patient.status == 0
    ).count()

    total_users = db.query(
        User
    ).count()

    logger.info(
        f"{current_user.username} viewed dashboard"
    )

    return {
        "total_patients": total_patients,
        "total_hospitals": total_hospitals,
        "admitted_patients": admitted_patients,
        "discharged_patients": discharged_patients,
        "total_users": total_users
    }