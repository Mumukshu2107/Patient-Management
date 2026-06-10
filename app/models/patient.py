from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.config.db import Base
from app.models.association import patient_hospital


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)

    name = Column(String(100))
    age = Column(Integer)
    contact_no = Column(String(15))
    height = Column(Float)
    weight = Column(Float)
    blood_group = Column(String(5))

    status = Column(Integer, default=0)

    current_hospital_id = Column(
        Integer,
        ForeignKey("hospitals.id"),
        nullable=True
    )

    hospitals = relationship(
        "Hospital",
        secondary=patient_hospital,
        back_populates="patients"
    )
    