from fastapi import FastAPI
from . import models, schemas
from .database import engine
from .router_factory import create_crud_router

# create tables automatically (no migrations requested)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Entity API")

@app.get("/health")
def health():
    return {"status": "ok"}

# Register routers for entities using the generic CRUD factory
# Example: hospitals
hospitals_router = create_crud_router(
    model=models.Hospital,
    create_schema=schemas.HospitalCreate,
    update_schema=schemas.HospitalUpdate,
    out_schema=schemas.HospitalOut,
    prefix="hospitals",
)
app.include_router(hospitals_router)

# Users entity
users_router = create_crud_router(
    model=models.User,
    create_schema=schemas.UserCreate,
    update_schema=schemas.UserUpdate,
    out_schema=schemas.UserOut,
    prefix="users",
)
app.include_router(users_router)

# Departments entity (belongs to a hospital)
departments_router = create_crud_router(
    model=models.Department,
    create_schema=schemas.DepartmentCreate,
    update_schema=schemas.DepartmentUpdate,
    out_schema=schemas.DepartmentOut,
    prefix="departments",
)
app.include_router(departments_router)

# Doctors entity
# Note: `custom_vocab` is stored as JSONB in the database
doctors_router = create_crud_router(
    model=models.Doctor,
    create_schema=schemas.DoctorCreate,
    update_schema=schemas.DoctorUpdate,
    out_schema=schemas.DoctorOut,
    prefix="doctors",
)
app.include_router(doctors_router)

# Patients
patients_router = create_crud_router(
    model=models.Patient,
    create_schema=schemas.PatientCreate,
    update_schema=schemas.PatientUpdate,
    out_schema=schemas.PatientOut,
    prefix="patients",
)
app.include_router(patients_router)

# Encounters
encounters_router = create_crud_router(
    model=models.Encounter,
    create_schema=schemas.EncounterCreate,
    update_schema=schemas.EncounterUpdate,
    out_schema=schemas.EncounterOut,
    prefix="encounters",
)
app.include_router(encounters_router)

# Dictations
dictations_router = create_crud_router(
    model=models.Dictation,
    create_schema=schemas.DictationCreate,
    update_schema=schemas.DictationUpdate,
    out_schema=schemas.DictationOut,
    prefix="dictations",
)
app.include_router(dictations_router)

# Transcriptions
transcriptions_router = create_crud_router(
    model=models.Transcription,
    create_schema=schemas.TranscriptionCreate,
    update_schema=schemas.TranscriptionUpdate,
    out_schema=schemas.TranscriptionOut,
    prefix="transcriptions",
)
app.include_router(transcriptions_router)

# SNOMED annotations
snomed_router = create_crud_router(
    model=models.SNOMEDAnnotation,
    create_schema=schemas.SNOMEDAnnotationCreate,
    update_schema=schemas.SNOMEDAnnotationUpdate,
    out_schema=schemas.SNOMEDAnnotationOut,
    prefix="snomed_annotations",
)
app.include_router(snomed_router)

# Clinical documents
clinical_documents_router = create_crud_router(
    model=models.ClinicalDocument,
    create_schema=schemas.ClinicalDocumentCreate,
    update_schema=schemas.ClinicalDocumentUpdate,
    out_schema=schemas.ClinicalDocumentOut,
    prefix="clinical_documents",
)
app.include_router(clinical_documents_router)

# To add another entity in future, create model + schemas and register with create_crud_router

