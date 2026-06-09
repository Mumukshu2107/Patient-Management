from pydantic import BaseModel, Field
from typing import Literal


class PatientCreate(BaseModel):
    name: str
    age: int
    contact_no: str = Field(min_length=10, max_length=10)
    height: float
    weight: float

    blood_group: Literal[
        "A+",
        "A-",
        "B+",
        "B-",
        "AB+",
        "AB-",
        "O+",
        "O-"
    ]


class PatientResponse(PatientCreate):
    id: int

    class Config:
        from_attributes = True