import pytest
from app import models
from app.database import engine

@pytest.fixture(scope="session", autouse=True)
def reset_db():
    # Ensure a clean schema for tests (drop then create all tables)
    if engine.dialect.name == "postgresql":
        from sqlalchemy import text
        # Drop stored procs first to avoid dependency errors when dropping tables
        with engine.begin() as conn:
            conn.execute(text("DROP FUNCTION IF EXISTS GetHospital(bigint) CASCADE"))
            conn.execute(text("DROP FUNCTION IF EXISTS SaveHospital(bigint, text, text, text, text, text, text, text, boolean) CASCADE"))

    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    # Create stored procedures required for tests (PostgreSQL only)
    if engine.dialect.name == "postgresql":
        from sqlalchemy import text
        # Create stored procs inside a transaction so DDL is committed
        with engine.begin() as conn:
            sql_save = open("Scripts/StoredProc/SaveHospital.sql").read()
            sql_get = open("Scripts/StoredProc/GetHospital.sql").read()
            conn.execute(text(sql_save))
            conn.execute(text(sql_get))
    yield
    # Optionally clean up after tests
    if engine.dialect.name == "postgresql":
        from sqlalchemy import text
        with engine.begin() as conn:
            conn.execute(text("DROP FUNCTION IF EXISTS GetHospital(bigint) CASCADE"))
            conn.execute(text("DROP FUNCTION IF EXISTS SaveHospital(bigint, text, text, text, text, text, text, text, boolean) CASCADE"))
    models.Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def run_around_tests():
    # small transactional cleanup per-test could be added here in future
    yield
