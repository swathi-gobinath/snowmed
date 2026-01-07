import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_hospital_helper():
    unique_code = f"HOSP_{uuid.uuid4().hex[:8]}"
    payload = {"name": "Test Hospital", "code": unique_code}
    r = client.post("/hospitals/", json=payload)
    assert r.status_code == 201
    return r.json()


def create_department_helper(hospital_id: int):
    payload = {"hospital_id": hospital_id, "name": "Dermatology", "code": "DERM", "specialty_model": "derm"}
    r = client.post("/departments/", json=payload)
    assert r.status_code == 201
    return r.json()


def test_create_and_get_doctor():
    hosp = create_hospital_helper()
    dept = create_department_helper(hosp["id"]) if True else None

    payload = {
        "hospital_id": hosp["id"],
        "department_id": dept["id"],
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
        "license_number": f"LIC-{uuid.uuid4().hex[:6]}",
        "specialty": "Dermatology",
        "custom_vocab": {"greeting": "hello", "terms": ["acne", "eczema"]},
    }

    r = client.post("/doctors/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["first_name"] == "Alice"
    assert data["custom_vocab"]["greeting"] == "hello"

    r2 = client.get(f"/doctors/{data['id']}")
    assert r2.status_code == 200
    assert r2.json()["hospital_id"] == hosp["id"]

    # update
    upd = {"first_name": "Alicia", "custom_vocab": {"greeting": "hi"}}
    r3 = client.put(f"/doctors/{data['id']}", json=upd)
    assert r3.status_code == 200
    assert r3.json()["first_name"] == "Alicia"
    assert r3.json()["custom_vocab"]["greeting"] == "hi"

    # delete (soft)
    r4 = client.delete(f"/doctors/{data['id']}")
    assert r4.status_code == 200
    assert r4.json()["is_active"] is False
