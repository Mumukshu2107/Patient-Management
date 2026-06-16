from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Table,
    DateTime
)
from sqlalchemy.orm import relationship
from config.db import Base


# =====================================================
# PATIENT-HOSPITAL ASSOCIATION TABLE
# =====================================================

patient_hospital = Table(
    "patient_hospital",
    Base.metadata,

Column("patient_id",Integer,ForeignKey("patients.id")),
    Column("hospital_id",Integer,ForeignKey("hospitals.id")),
    Column("admit_time",DateTime,default=datetime.utcnow),
    Column("discharge_time",DateTime,nullable=True)
)


# =====================================================
# PATIENT MODEL
# =====================================================

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100),nullable=False)
    age = Column(Integer,nullable=False)
    contact_no = Column(String(15),nullable=False)
    height = Column(Float,nullable=False)
    weight = Column(Float,nullable=False)
    blood_group = Column(String(5),nullable=False)
    status = Column(Integer,default=0)
    current_hospital_id = Column(Integer,ForeignKey("hospitals.id"),nullable=True)
    hospitals = relationship("Hospital",secondary=patient_hospital,back_populates="patients")


# =====================================================
# HOSPITAL MODEL
# =====================================================

class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100),nullable=False)
    city = Column(String(100),nullable=False)
    patients = relationship("Patient",secondary=patient_hospital,back_populates="hospitals")