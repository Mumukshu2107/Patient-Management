from pydantic import BaseModel


class PatientHospitalLink(BaseModel):
    patient_id: int
    hospital_id: int