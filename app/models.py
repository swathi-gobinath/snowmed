from sqlalchemy import Column, BigInteger, String, Text, Boolean, TIMESTAMP, func, ForeignKey, Integer, Date, Numeric
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import JSONB, BYTEA

Base = declarative_base()

class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(20), unique=True, index=True)
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(50))
    pincode = Column(String(10))
    abha_facility_id = Column(String(64))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships
    patients = relationship("Patient", back_populates="hospital")
    departments = relationship("Department", back_populates="hospital")
    doctors = relationship("Doctor", back_populates="hospital")
    encounters = relationship("Encounter", back_populates="hospital")
    dictations = relationship("Dictation", back_populates="hospital")
    clinical_documents = relationship("ClinicalDocument", back_populates="hospital")

class Department(Base):
    __tablename__ = "departments"

    id = Column(BigInteger, primary_key=True, index=True)
    hospital_id = Column(BigInteger, ForeignKey("hospitals.id"), nullable=False)
    name = Column(String(100), nullable=False)
    code = Column(String(20))
    specialty_model = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships
    hospital = relationship("Hospital", back_populates="departments")
    doctors = relationship("Doctor", back_populates="department")
    encounters = relationship("Encounter", back_populates="department")
    dictations = relationship("Dictation", back_populates="department")
    clinical_documents = relationship("ClinicalDocument", back_populates="department")


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, index=True)
    phone = Column(String(20))
    gender = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    password= Column(String(50), nullable=False)



class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(BigInteger, primary_key=True, index=True)
    hospital_id = Column(BigInteger, ForeignKey("hospitals.id"), nullable=False)
    department_id = Column(BigInteger, ForeignKey("departments.id"), nullable=True)
    abha_professional_id = Column(String(64))
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(200))
    phone = Column(String(20))
    license_number = Column(String(50))
    specialty = Column(String(100))
    custom_vocab = Column(JSONB)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    userid = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    photo = Column(BYTEA)

    # Relationships
    hospital = relationship("Hospital", back_populates="doctors")
    department = relationship("Department", back_populates="doctors")


# --- New clinical models ---
class Patient(Base):
    __tablename__ = "patients"

    id = Column(BigInteger, primary_key=True, index=True)
    hospital_id = Column(BigInteger, ForeignKey("hospitals.id"))
    external_id = Column(String(64))
    first_name = Column(String(100))
    last_name = Column(String(100))
    date_of_birth = Column(Date)
    sex = Column(String(10))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    hospital = relationship("Hospital", back_populates="patients")
    encounters = relationship("Encounter", back_populates="patient")
    dictations = relationship("Dictation", back_populates="patient")
    clinical_documents = relationship("ClinicalDocument", back_populates="patient")


class Encounter(Base):
    __tablename__ = "encounters"

    id = Column(BigInteger, primary_key=True, index=True)
    hospital_id = Column(BigInteger, ForeignKey("hospitals.id"), nullable=False)
    patient_id = Column(BigInteger, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(BigInteger, ForeignKey("doctors.id"))
    external_id = Column(String(64))
    encounter_type = Column(String(50))
    department_id = Column(BigInteger, ForeignKey("departments.id"))
    started_at = Column(TIMESTAMP(timezone=True))
    ended_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    hospital = relationship("Hospital", back_populates="encounters")
    patient = relationship("Patient", back_populates="encounters")
    doctor = relationship("Doctor")
    department = relationship("Department", back_populates="encounters")
    dictations = relationship("Dictation", back_populates="encounter")


class Dictation(Base):
    __tablename__ = "dictations"

    id = Column(BigInteger, primary_key=True, index=True)
    hospital_id = Column(BigInteger, ForeignKey("hospitals.id"), nullable=False)
    department_id = Column(BigInteger, ForeignKey("departments.id"), nullable=False)
    doctor_id = Column(BigInteger, ForeignKey("doctors.id"), nullable=False)
    patient_id = Column(BigInteger, ForeignKey("patients.id"))
    encounter_id = Column(BigInteger, ForeignKey("encounters.id"))
    dictation_number = Column(String(50), unique=True)
    language = Column(String(10), default="en-IN")
    status = Column(String(20), nullable=False)
    audio_path = Column(Text)
    duration_sec = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    hospital = relationship("Hospital", back_populates="dictations")
    department = relationship("Department", back_populates="dictations")
    doctor = relationship("Doctor")
    patient = relationship("Patient", back_populates="dictations")
    encounter = relationship("Encounter", back_populates="dictations")
    transcriptions = relationship("Transcription", back_populates="dictation")
    snomed_annotations = relationship("SNOMEDAnnotation", back_populates="dictation")
    clinical_documents = relationship("ClinicalDocument", back_populates="dictation")


class Transcription(Base):
    __tablename__ = "transcriptions"

    id = Column(BigInteger, primary_key=True, index=True)
    dictation_id = Column(BigInteger, ForeignKey("dictations.id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(BigInteger, ForeignKey("doctors.id"), nullable=False)
    raw_text = Column(Text, nullable=False)
    model_name = Column(String(100))
    confidence = Column(Numeric(4,3))
    word_count = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    dictation = relationship("Dictation", back_populates="transcriptions")
    doctor = relationship("Doctor")


class SNOMEDAnnotation(Base):
    __tablename__ = "snomed_annotations"

    id = Column(BigInteger, primary_key=True, index=True)
    dictation_id = Column(BigInteger, ForeignKey("dictations.id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(BigInteger, ForeignKey("doctors.id"), nullable=False)
    transcription_id = Column(BigInteger, ForeignKey("transcriptions.id"))
    snomed_concept_id = Column(BigInteger, nullable=False)
    term = Column(Text, nullable=False)
    category = Column(String(50))
    start_char = Column(Integer)
    end_char = Column(Integer)
    confidence = Column(Numeric(4,3))
    model_used = Column(String(50))
    extra = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    dictation = relationship("Dictation", back_populates="snomed_annotations")
    doctor = relationship("Doctor")
    transcription = relationship("Transcription")


class ClinicalDocument(Base):
    __tablename__ = "clinical_documents"

    id = Column(BigInteger, primary_key=True, index=True)
    dictation_id = Column(BigInteger, ForeignKey("dictations.id", ondelete="CASCADE"), nullable=False)
    hospital_id = Column(BigInteger, ForeignKey("hospitals.id"), nullable=False)
    department_id = Column(BigInteger, ForeignKey("departments.id"), nullable=False)
    doctor_id = Column(BigInteger, ForeignKey("doctors.id"), nullable=False)
    patient_id = Column(BigInteger, ForeignKey("patients.id"), nullable=False)
    encounter_id = Column(BigInteger, ForeignKey("encounters.id"))
    document_type = Column(String(50))
    version = Column(Integer, default=1)
    status = Column(String(20), nullable=False)
    final_text = Column(Text, nullable=False)
    fhir_resource_type = Column(String(50))
    fhir_json = Column(JSONB)
    doctor_signature = Column(Text)
    signed_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    dictation = relationship("Dictation", back_populates="clinical_documents")
    hospital = relationship("Hospital", back_populates="clinical_documents")
    department = relationship("Department", back_populates="clinical_documents")
    doctor = relationship("Doctor")
    patient = relationship("Patient", back_populates="clinical_documents")

