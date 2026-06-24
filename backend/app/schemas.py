from enum import Enum
from pydantic import BaseModel, field_validator


# -------------------------
# BLOOD GROUP ENUM
# -------------------------

class BloodGroup(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"


# -------------------------
# PATIENT SCHEMAS
# -------------------------

class PatientCreate(BaseModel):
    name: str
    age: int
    contact_no: str
    height: float
    weight: float
    blood_group: BloodGroup

    @field_validator("contact_no")
    @classmethod
    def validate_contact_no(cls, value):

        if not value.isdigit():
            raise ValueError(
                "Contact number must contain only digits"
            )

        if len(value) != 10:
            raise ValueError(
                "Contact number must be 10 digits"
            )

        return value

class PatientResponse(PatientCreate):
    id: int
    status: int
    current_hospital_id: int | None = None

    class Config:
        from_attributes = True



# -------------------------
# HOSPITAL SCHEMAS
# -------------------------

class HospitalCreate(BaseModel):
    name: str
    city: str


class HospitalResponse(HospitalCreate):
    id: int

    class Config:
        from_attributes = True


# -------------------------
# ADMISSION SCHEMAS
# -------------------------

class PatientHospitalLink(BaseModel):
    patient_id: int
    hospital_id: int

class SearchRequest(BaseModel):
    search_type: str
    search_text: str

class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    RECEPTIONIST = "RECEPTIONIST"

#Create User
class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole

#User Response
class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole

    model_config = {
        "from_attributes": True
    }


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str