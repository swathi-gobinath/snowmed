import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# These tests assume a reachable DB; run them after the DB is up or mock database sessions.

def test_create_and_get_hospital():
    unique_code = f"APOLLO_{uuid.uuid4().hex[:8]}"
    payload = {"name": "Apollo", "code": unique_code}
    r = client.post("/hospitals/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Apollo"
    r2 = client.get(f"/hospitals/{data['id']}")
    assert r2.status_code == 200
