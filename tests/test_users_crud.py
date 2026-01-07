import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_user():
    unique_name = f"User_{uuid.uuid4().hex[:8]}"
    payload = {"name": unique_name, "gender": "Male"}
    r = client.post("/users/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == unique_name
    r2 = client.get(f"/users/{data['id']}")
    assert r2.status_code == 200
    assert r2.json()["gender"] == "Male"