from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime
from datetime import datetime

from app.config.db import Base

patient_hospital = Table(
    "patient_hospital",
    Base.metadata,

    Column(
        "patient_id",
        Integer,
        ForeignKey("patients.id")
    ),

    Column(
        "hospital_id",
        Integer,
        ForeignKey("hospitals.id")
    ),

    Column(
        "admit_time",
        DateTime,
        default=datetime.utcnow
    ),

    Column(
        "discharge_time",
        DateTime,
        nullable=True
    )
)