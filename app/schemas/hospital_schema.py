from pydantic import BaseModel


class HospitalCreate(BaseModel):
    name: str
    city: str


class HospitalResponse(HospitalCreate):
    id: int

    class Config:
        from_attributes = True