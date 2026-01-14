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
    sql_files = [
        "Scripts/StoredProc/SaveHospital.sql",
        "Scripts/StoredProc/GetHospital.sql",
        "Scripts/StoredProc/SaveUser.sql",
        "Scripts/StoredProc/GetUser.sql"
    ]
    for sql_file in sql_files:
        with open(sql_file) as f:
            sql = f.read()
            conn.execute(text(sql))

print("Stored procedures installed.")