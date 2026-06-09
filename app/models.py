from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    contact_no = Column(String(15), nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    blood_group = Column(String(5), nullable=False)