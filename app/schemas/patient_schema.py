from enum import Enum

from pydantic import BaseModel


class BloodGroup(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"


class PatientCreate(BaseModel):
    name: str
    age: int
    contact_no: str
    height: float
    weight: float
    blood_group: BloodGroup


class PatientResponse(PatientCreate):
    id: int
    status: int
    current_hospital_id: int | None = None

    class Config:
        from_attributes = True


