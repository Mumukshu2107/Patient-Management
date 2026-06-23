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
    Form
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
    get_current_user,
    hash_password,
    verify_password,
    create_access_token
)
from app.schemas import (
    LoginRequest,
    TokenResponse
)
from app.security import decode_access_token

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


def require_super_admin(
        current_user: User = Depends(get_current_user)
):

    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Only Super Admin can perform this action"
        )

    return current_user

def require_admin(
        current_user: User = Depends(get_current_user)
):

    if current_user.role not in [
        UserRole.SUPER_ADMIN,
        UserRole.ADMIN
    ]:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user

def require_doctor(
        current_user: User = Depends(get_current_user)
):

    if current_user.role not in [
        UserRole.SUPER_ADMIN,
        UserRole.ADMIN,
        UserRole.DOCTOR
    ]:
        raise HTTPException(
            status_code=403,
            detail="Doctor access required"
        )

    return current_user

def require_receptionist(
        current_user: User = Depends(get_current_user)
):

    if current_user.role not in [
        UserRole.SUPER_ADMIN,
        UserRole.ADMIN,
        UserRole.RECEPTIONIST
    ]:
        raise HTTPException(
            status_code=403,
            detail="Receptionist access required"
        )

    return current_user


@router.get("/patients", response_model=list[PatientResponse])
def get_patients(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return db.query(Patient).all()

@router.post(
    "/hospitals",
    response_model=HospitalResponse
)
def add_hospital(
        hospital: HospitalCreate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):

    existing_hospital = db.query(Hospital).filter(
        Hospital.name.ilike(hospital.name),
        Hospital.city.ilike(hospital.city)
    ).first()

    if existing_hospital:
        raise HTTPException(
            status_code=400,
            detail=f"Hospital '{hospital.name}' already exists in {hospital.city}"
        )

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
        current_user: User = Depends(require_receptionist),
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

    # Force SQLAlchemy to create the row in patient_hospital
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
        current_user: User = Depends(require_receptionist),
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

@router.get("/search/patient")
def search_patient(
        search_by: str,
        search_text: str,
        db: Session = Depends(get_db)
):
    """
    search_by:
        name
        contact_no
    """

    search_by = search_by.lower()

    # =====================================
    # SEARCH BY PATIENT NAME
    # =====================================

    if search_by == "name":

        patients = db.query(Patient).all()

        matched_patients = []

        # Partial Match Search
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
            return {
                "match_found": True,
                "patients": matched_patients
            }

        # =====================================
        # FUZZY SEARCH IF NO MATCH FOUND
        # =====================================

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

    # =====================================
    # INVALID SEARCH TYPE
    # =====================================

    else:
        raise HTTPException(
            status_code=400,
            detail="search_by must be name or contact_no"
        )

@router.post("/upload-data")
async def upload_data(
        current_user: User = Depends(require_admin),
        entity_type: str = Form(...),
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):

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
                Patient.contact_no == str(row["contact_no"])
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
            hospital_name = str(row["name"]).strip()
            hospital_city = str(row["city"]).strip()
            existing_hospital = db.query(Hospital).filter(
                Hospital.name.ilike(hospital_name),
                Hospital.city.ilike(hospital_city)
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

        return {
            "message": "Upload completed",
            "records_inserted": inserted_count,
            "duplicate_records_skipped": len(skipped_hospitals),
            "skipped_hospitals": skipped_hospitals
        }

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
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):

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
    df.to_csv(stream, index=False)

    response = StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv"
    )

    response.headers[
        "Content-Disposition"
    ] = "attachment; filename=hospitals.csv"

    return response

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
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    password_valid = verify_password(
        credentials.password,
        user.password
    )

    if not password_valid:
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

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
@router.post(
    "/users",
    response_model=UserResponse
)
def create_user(
        user: UserCreate,
        current_user: User = Depends(require_super_admin),
        db: Session = Depends(get_db)
):

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
        password=hash_password(user.password),
        role=user.role.value
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/me")
def get_me(
        current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role
    }


@router.get("/users")
def get_users(
    current_user: User = Depends(require_super_admin),
    db: Session = Depends(get_db)
):
    return db.query(User).all()

@router.get("/dashboard")
def dashboard_stats(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):

    total_patients = db.query(Patient).count()

    total_hospitals = db.query(Hospital).count()

    admitted_patients = db.query(Patient).filter(
        Patient.status == 1
    ).count()

    discharged_patients = db.query(Patient).filter(
        Patient.status == 0
    ).count()

    total_users = db.query(User).count()

    return {
        "total_patients": total_patients,
        "total_hospitals": total_hospitals,
        "admitted_patients": admitted_patients,
        "discharged_patients": discharged_patients,
        "total_users": total_users
    }


#I have done a project where frontend written in next.js and backend in FastAPI. Now i need to use middleware and logging in my project. So take out @router.post("/login",response_model=TokenResponse) api from the current folder make seperate file/ folder. using middleware authenticate the login user. Need to add log in the project also. Give an idea first how to do and then i will tell to give code. If you need any information or anything kindly ask



