from sqlalchemy import (
    Column,
    Integer,
    String
)

from sqlalchemy.orm import relationship

from app.config.db import Base
from app.models.association import patient_hospital


class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True)

    name = Column(String(100))
    city = Column(String(100))

    patients = relationship(
        "Patient",
        secondary=patient_hospital,
        back_populates="hospitals"
    )