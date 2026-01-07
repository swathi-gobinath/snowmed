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


def test_create_and_get_department():
    hosp = create_hospital_helper()
    payload = {"hospital_id": hosp["id"], "name": "Cardiology", "code": "CARDIO", "specialty_model": "cardio"}
    r = client.post("/departments/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Cardiology"

    r2 = client.get(f"/departments/{data['id']}")
    assert r2.status_code == 200
    assert r2.json()["hospital_id"] == hosp["id"]

    # update
    upd = {"name": "Cardio Updated"}
    r3 = client.put(f"/departments/{data['id']}", json=upd)
    assert r3.status_code == 200
    assert r3.json()["name"] == "Cardio Updated"

    # delete (soft)
    r4 = client.delete(f"/departments/{data['id']}")
    assert r4.status_code == 200
    assert r4.json()["is_active"] is False
