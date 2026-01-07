import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_hospital():
    code = f"HOSP_{uuid.uuid4().hex[:8]}"
    r = client.post("/hospitals/", json={"name": "Test Hospital", "code": code})
    assert r.status_code == 201
    return r.json()


def create_department(hospital_id):
    r = client.post("/departments/", json={"hospital_id": hospital_id, "name": "Oncology", "code": "ONC"})
    assert r.status_code == 201
    return r.json()


def create_doctor(hospital_id, department_id=None):
    r = client.post(
        "/doctors/",
        json={
            "hospital_id": hospital_id,
            "department_id": department_id,
            "first_name": "Doc",
            "last_name": "Tor",
            "license_number": f"LIC-{uuid.uuid4().hex[:6]}",
        },
    )
    assert r.status_code == 201
    return r.json()


def create_patient(hospital_id):
    r = client.post(
        "/patients/",
        json={"hospital_id": hospital_id, "external_id": f"MRN-{uuid.uuid4().hex[:6]}", "first_name": "John", "last_name": "Doe"},
    )
    assert r.status_code == 201
    return r.json()


def create_encounter(hospital_id, patient_id, doctor_id=None, department_id=None):
    r = client.post(
        "/encounters/",
        json={"hospital_id": hospital_id, "patient_id": patient_id, "doctor_id": doctor_id, "department_id": department_id, "encounter_type": "OPD"},
    )
    assert r.status_code == 201
    return r.json()


def create_dictation(hospital_id, department_id, doctor_id, patient_id=None, encounter_id=None):
    r = client.post(
        "/dictations/",
        json={
            "hospital_id": hospital_id,
            "department_id": department_id,
            "doctor_id": doctor_id,
            "patient_id": patient_id,
            "encounter_id": encounter_id,
            "status": "recorded",
            "dictation_number": f"D-{uuid.uuid4().hex[:8]}",
        },
    )
    assert r.status_code == 201
    return r.json()


def test_patient_crud():
    hosp = create_hospital()
    patient = create_patient(hosp["id"])

    r = client.get(f"/patients/{patient['id']}")
    assert r.status_code == 200
    assert r.json()["first_name"] == "John"

    upd = {"first_name": "Johnny"}
    r2 = client.put(f"/patients/{patient['id']}", json=upd)
    assert r2.status_code == 200
    assert r2.json()["first_name"] == "Johnny"

    r3 = client.delete(f"/patients/{patient['id']}")
    assert r3.status_code == 200


def test_encounter_and_dictation_workflow():
    hosp = create_hospital()
    dept = create_department(hosp["id"])
    doc = create_doctor(hosp["id"], dept["id"])
    patient = create_patient(hosp["id"])
    enc = create_encounter(hosp["id"], patient["id"], doc["id"], dept["id"])

    d = create_dictation(hosp["id"], dept["id"], doc["id"], patient["id"], enc["id"])
    assert d["status"] == "recorded"

    # transcription
    tr = client.post(
        "/transcriptions/",
        json={"dictation_id": d["id"], "doctor_id": doc["id"], "raw_text": "Test transcription."},
    )
    assert tr.status_code == 201
    trd = tr.json()
    assert trd["raw_text"].startswith("Test")

    # snomed annotation
    sn = client.post(
        "/snomed_annotations/",
        json={
            "dictation_id": d["id"],
            "doctor_id": doc["id"],
            "transcription_id": trd["id"],
            "snomed_concept_id": 12345,
            "term": "myterm",
        },
    )
    assert sn.status_code == 201

    # clinical document
    cd = client.post(
        "/clinical_documents/",
        json={
            "dictation_id": d["id"],
            "hospital_id": hosp["id"],
            "department_id": dept["id"],
            "doctor_id": doc["id"],
            "patient_id": patient["id"],
            "document_type": "discharge_summary",
            "status": "draft",
            "final_text": "Final report text",
        },
    )
    assert cd.status_code == 201
    assert cd.json()["status"] == "draft"
