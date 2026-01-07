# Hospitals API (FastAPI + PostgreSQL)

This project exposes CRUD operations for `hospitals` and `users` entities backed by PostgreSQL.

## Quick start

1. Create and start Postgres (Docker Compose):

   docker compose up -d

2. Create a virtualenv and install deps:

   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt

3. Ensure `.env` has the correct `DATABASE_URL` and run:

   uvicorn app.main:app --reload

The app provides:
- GET /health
- POST /hospitals/
- GET /hospitals/
- GET /hospitals/{id}
- PUT /hospitals/{id}
- DELETE /hospitals/{id} (soft delete — sets `is_active` to `false`)

Stored procedures
- Two PostgreSQL stored procedures are provided in `Scripts/StoredProc`:
  - `SaveHospital.sql` — performs a merge (insert or update) and returns the hospital id
  - `GetHospital.sql` — returns a hospital by id; if called with `p_id` = NULL or `0`, returns all hospitals

To install those procedures in your PostgreSQL database run:

```bash
python Scripts/StoredProc/install_stored_procs.py
```

When running against SQLite (default for local tests), the router falls back to the existing ORM-based behavior.

### Adding new entities (generic router)
You can add additional entities without copying endpoint code — use the provided `create_crud_router` factory in `app/router_factory.py`.

Example (add a `Clinic` model + `ClinicCreate`, `ClinicUpdate`, `ClinicOut` schemas):

```py
from app.router_factory import create_crud_router
from app import models, schemas

clinics_router = create_crud_router(
    model=models.Clinic,
    create_schema=schemas.ClinicCreate,
    update_schema=schemas.ClinicUpdate,
    out_schema=schemas.ClinicOut,
    prefix="clinics",
)
app.include_router(clinics_router)
```

This registers `/clinics/` endpoints automatically (POST/GET/PUT/DELETE).

> Note: No migrations were requested; the app will create tables automatically on startup.
