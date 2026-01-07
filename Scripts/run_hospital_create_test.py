"""Standalone test runner for create hospital endpoint.
Usage: python Scripts/run_hospital_create_test.py
Exits with non-zero status on failure.
"""
import sys
import os
import sys
import uuid
# Ensure project root is on sys.path so we can import app
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import models
from app import database
from fastapi.testclient import TestClient
from app.main import app

# Setup DB schema
# If using PostgreSQL and stored procs are installed, drop them first to avoid dependency errors
if database.engine.dialect.name == "postgresql":
    from sqlalchemy import text
    with database.engine.begin() as conn:
        conn.execute(text("DROP FUNCTION IF EXISTS GetHospital(bigint) CASCADE"))
        conn.execute(text("DROP FUNCTION IF EXISTS SaveHospital(bigint, text, text, text, text, text, text, text, boolean) CASCADE"))

models.Base.metadata.drop_all(bind=database.engine)
models.Base.metadata.create_all(bind=database.engine)

# Install stored procs if using PostgreSQL
if database.engine.dialect.name == "postgresql":
    from sqlalchemy import text
    # Ensure DDL is committed
    with database.engine.begin() as conn:
        sql_save = open("Scripts/StoredProc/SaveHospital.sql").read()
        sql_get = open("Scripts/StoredProc/GetHospital.sql").read()
        conn.execute(text(sql_save))
        conn.execute(text(sql_get))

client = TestClient(app)
unique_code = f"TEST_{uuid.uuid4().hex[:8]}"
payload = {"name": "Test Hospital", "code": unique_code}

r = client.post("/hospitals/", json=payload)
print("POST /hospitals/ ->", r.status_code)
try:
    print(r.json())
except Exception:
    print(r.text)

if r.status_code != 201:
    print("Test failed: create did not return 201", file=sys.stderr)
    sys.exit(2)

# Verify GET
data = r.json()
rid = data.get("id")
r2 = client.get(f"/hospitals/{rid}")
print(f"GET /hospitals/{rid} ->", r2.status_code)
try:
    print(r2.json())
except Exception:
    print(r2.text)

if r2.status_code != 200:
    print("Test failed: get did not return 200", file=sys.stderr)
    sys.exit(3)

print("Create test passed.")
sys.exit(0)
