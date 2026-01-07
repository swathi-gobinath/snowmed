from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HospitalBase(BaseModel):
    name: str
    code: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    abha_facility_id: Optional[str] = None
    is_active: Optional[bool] = True

class HospitalCreate(HospitalBase):
    pass

class HospitalUpdate(BaseModel):
    name: Optional[str]
    code: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    pincode: Optional[str]
    abha_facility_id: Optional[str]
    is_active: Optional[bool]

class HospitalOut(HospitalBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

# --- Departments schemas ---
class DepartmentBase(BaseModel):
    hospital_id: int
    name: str
    code: Optional[str] = None
    specialty_model: Optional[str] = None
    is_active: Optional[bool] = True

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    hospital_id: Optional[int]
    name: Optional[str]
    code: Optional[str]
    specialty_model: Optional[str]
    is_active: Optional[bool]

class DepartmentOut(DepartmentBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


# --- Users schemas ---
class UserBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    is_active: Optional[bool]

class UserOut(UserBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


# --- Doctors schemas ---
class DoctorBase(BaseModel):
    hospital_id: int
    department_id: Optional[int] = None
    abha_professional_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    license_number: Optional[str] = None
    specialty: Optional[str] = None
    custom_vocab: Optional[dict] = None
    is_active: Optional[bool] = True

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(BaseModel):
    hospital_id: Optional[int]
    department_id: Optional[int]
    abha_professional_id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    license_number: Optional[str]
    specialty: Optional[str]
    custom_vocab: Optional[dict]
    is_active: Optional[bool]

class DoctorOut(DoctorBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


# --- Patients schemas ---
from datetime import date

class PatientBase(BaseModel):
    hospital_id: Optional[int]
    external_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    sex: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    hospital_id: Optional[int]
    external_id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[date]
    sex: Optional[str]

class PatientOut(PatientBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


# --- Encounters schemas ---
class EncounterBase(BaseModel):
    hospital_id: int
    patient_id: int
    doctor_id: Optional[int] = None
    external_id: Optional[str] = None
    encounter_type: Optional[str] = None
    department_id: Optional[int] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None

class EncounterCreate(EncounterBase):
    pass

class EncounterUpdate(BaseModel):
    hospital_id: Optional[int]
    patient_id: Optional[int]
    doctor_id: Optional[int]
    external_id: Optional[str]
    encounter_type: Optional[str]
    department_id: Optional[int]
    started_at: Optional[datetime]
    ended_at: Optional[datetime]

class EncounterOut(EncounterBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


# --- Dictations schemas ---
class DictationBase(BaseModel):
    hospital_id: int
    department_id: int
    doctor_id: int
    patient_id: Optional[int] = None
    encounter_id: Optional[int] = None
    dictation_number: Optional[str] = None
    language: Optional[str] = "en-IN"
    status: str
    audio_path: Optional[str] = None
    duration_sec: Optional[int] = None

class DictationCreate(DictationBase):
    pass

class DictationUpdate(BaseModel):
    hospital_id: Optional[int]
    department_id: Optional[int]
    doctor_id: Optional[int]
    patient_id: Optional[int]
    encounter_id: Optional[int]
    dictation_number: Optional[str]
    language: Optional[str]
    status: Optional[str]
    audio_path: Optional[str]
    duration_sec: Optional[int]

class DictationOut(DictationBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


# --- Transcriptions schemas ---
class TranscriptionBase(BaseModel):
    dictation_id: int
    doctor_id: int
    raw_text: str
    model_name: Optional[str] = None
    confidence: Optional[float] = None
    word_count: Optional[int] = None

class TranscriptionCreate(TranscriptionBase):
    pass

class TranscriptionUpdate(BaseModel):
    dictation_id: Optional[int]
    doctor_id: Optional[int]
    raw_text: Optional[str]
    model_name: Optional[str]
    confidence: Optional[float]
    word_count: Optional[int]

class TranscriptionOut(TranscriptionBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


# --- SNOMED annotations schemas ---
class SNOMEDAnnotationBase(BaseModel):
    dictation_id: int
    doctor_id: int
    transcription_id: Optional[int] = None
    snomed_concept_id: int
    term: str
    category: Optional[str] = None
    start_char: Optional[int] = None
    end_char: Optional[int] = None
    confidence: Optional[float] = None
    model_used: Optional[str] = None
    extra: Optional[dict] = None

class SNOMEDAnnotationCreate(SNOMEDAnnotationBase):
    pass

class SNOMEDAnnotationUpdate(BaseModel):
    dictation_id: Optional[int]
    doctor_id: Optional[int]
    transcription_id: Optional[int]
    snomed_concept_id: Optional[int]
    term: Optional[str]
    category: Optional[str]
    start_char: Optional[int]
    end_char: Optional[int]
    confidence: Optional[float]
    model_used: Optional[str]
    extra: Optional[dict]

class SNOMEDAnnotationOut(SNOMEDAnnotationBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


# --- Clinical documents schemas ---
class ClinicalDocumentBase(BaseModel):
    dictation_id: int
    hospital_id: int
    department_id: int
    doctor_id: int
    patient_id: int
    encounter_id: Optional[int] = None
    document_type: Optional[str] = None
    version: Optional[int] = 1
    status: str
    final_text: str
    fhir_resource_type: Optional[str] = None
    fhir_json: Optional[dict] = None
    doctor_signature: Optional[str] = None
    signed_at: Optional[datetime] = None

class ClinicalDocumentCreate(ClinicalDocumentBase):
    pass

class ClinicalDocumentUpdate(BaseModel):
    dictation_id: Optional[int]
    hospital_id: Optional[int]
    department_id: Optional[int]
    doctor_id: Optional[int]
    patient_id: Optional[int]
    encounter_id: Optional[int]
    document_type: Optional[str]
    version: Optional[int]
    status: Optional[str]
    final_text: Optional[str]
    fhir_resource_type: Optional[str]
    fhir_json: Optional[dict]
    doctor_signature: Optional[str]
    signed_at: Optional[datetime]

class ClinicalDocumentOut(ClinicalDocumentBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
