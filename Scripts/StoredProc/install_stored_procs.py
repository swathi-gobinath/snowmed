"""Install stored procedures in the database referenced by DATABASE_URL env var.
Usage: python Scripts/StoredProc/install_stored_procs.py
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise SystemExit("DATABASE_URL not set; aborting")

engine = create_engine(DATABASE_URL)

# Execute in a BEGIN/COMMIT block so DDL is persisted
with engine.begin() as conn:
    sql_save = open("Scripts/StoredProc/SaveHospital.sql").read()
    sql_get = open("Scripts/StoredProc/GetHospital.sql").read()
    conn.execute(text(sql_save))
    conn.execute(text(sql_get))

print("Stored procedures installed.")