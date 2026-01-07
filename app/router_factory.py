from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import text
from typing import Type, TypeVar
from pydantic import BaseModel
from .database import get_db

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
OutSchemaType = TypeVar("OutSchemaType", bound=BaseModel)


def create_crud_router(
    model: Type[ModelType],
    create_schema: Type[CreateSchemaType],
    update_schema: Type[UpdateSchemaType],
    out_schema: Type[OutSchemaType],
    prefix: str,
):
    """Create an APIRouter providing CRUD endpoints for the given SQLAlchemy model.

    - `model`: SQLAlchemy declarative model class
    - `create_schema`: Pydantic schema for POST body
    - `update_schema`: Pydantic schema for PUT body
    - `out_schema`: Pydantic schema for responses (must have orm_mode)
    - `prefix`: route prefix (e.g., 'hospitals')
    """

    router = APIRouter(prefix=f"/{prefix}", tags=[prefix])

    import re

    def _pg_proc_exists(conn, proc_name: str) -> bool:
        """Return True if a PostgreSQL function named `proc_name` exists in pg_proc.
        Only allow simple identifier names to avoid injection.
        """
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', proc_name):
            return False
        # Postgres stores unquoted identifiers in lowercase; normalize to avoid case-sensitivity issues
        res = conn.execute(text("SELECT 1 FROM pg_catalog.pg_proc WHERE proname = :proc LIMIT 1"), {"proc": proc_name.lower()})
        return res.fetchone() is not None

    # --- Helpers for dynamic stored-proc parameter/statement generation ---
    def _sa_type_to_pg(col):
        """Map SQLAlchemy column type instances to a Postgres type name used for CAST()."""
        from sqlalchemy import String, Text, Integer, BigInteger, Boolean, DateTime, JSON, Numeric

        t = col.type
        if isinstance(t, (String, Text)):
            return "text"
        if isinstance(t, (Integer, BigInteger)):
            return "bigint"
        if isinstance(t, Boolean):
            return "boolean"
        if isinstance(t, DateTime):
            return "timestamptz"
        if isinstance(t, JSON):
            return "jsonb"
        if isinstance(t, Numeric):
            return "numeric"
        # Fallback
        return "text"

    def _proc_columns(model):
        """Return non-auto columns to include in stored-proc parameters (excludes 'id' and timestamps)."""
        return [c for c in model.__table__.columns if c.name not in ("id", "created_at", "updated_at")]

    def build_save_stmt(model, include_id=True):
        cols = _proc_columns(model)
        args = []
        if include_id:
            args.append("CAST(:p_id AS bigint)")
        for c in cols:
            pgtype = _sa_type_to_pg(c)
            args.append(f"CAST(:p_{c.name} AS {pgtype})")
        return text(f"SELECT Save{model.__name__}({', '.join(args)})")

    def build_db_params(schema_or_dict, include_id=False):
        """Build a dict of p_<name>: value pairs from a Pydantic schema or a plain dict."""
        if isinstance(schema_or_dict, dict):
            src = schema_or_dict
        else:
            src = schema_or_dict.dict()
        params = {}
        if include_id:
            params["p_id"] = None
        for k, v in src.items():
            params[f"p_{k}"] = v
        return params

    @router.post("/", response_model=out_schema, status_code=status.HTTP_201_CREATED)
    def create_item(item: create_schema, db: Session = Depends(get_db)):
        # For PostgreSQL, if a Save{Entity} stored procedure exists, use it (merge semantics)
        entity = model.__name__
        if getattr(db.bind.dialect, "name", "") == "postgresql" and _pg_proc_exists(db, f"Save{entity}"):
            params = item.dict()
            try:
                # Build dynamic statement and params from model columns and incoming payload
                stmt = build_save_stmt(model, include_id=True)
                db_params = build_db_params(params, include_id=True)
                res = db.execute(stmt, db_params)
                saved_id = res.scalar()
                db.commit()
                db_obj = db.query(model).filter(model.id == saved_id).first()
                if not db_obj:
                    raise HTTPException(status_code=500, detail=f"Failed to load saved {entity}")
                return db_obj
            except IntegrityError as e:
                db.rollback()
                raise HTTPException(status_code=400, detail=str(e.orig))
            except Exception as e:
                # Log and surface the underlying exception for easier debugging
                db.rollback()
                err_msg = f"Stored procedure {save_proc} error: {e.__class__.__name__}: {str(e)}"
                print(err_msg)
                raise HTTPException(status_code=500, detail=err_msg)
        # Default behavior for other models
        db_obj = model(**item.dict())
        db.add(db_obj)
        try:
            db.commit()
            db.refresh(db_obj)
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e.orig))
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Database error during create")
        return db_obj

    @router.get("/", response_model=list[out_schema])
    def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return db.query(model).offset(skip).limit(limit).all()

    @router.get("/{item_id}", response_model=out_schema)
    def get_item(item_id: int, db: Session = Depends(get_db)):
        # Require a Get{Entity} stored procedure for reads; do not fallback to ORM
        entity = model.__name__
        if getattr(db.bind.dialect, "name", "") == "postgresql" and _pg_proc_exists(db, f"Get{entity}"):
            get_proc = f"Get{entity}"
            res = db.execute(text(f"SELECT * FROM {get_proc}(CAST(:p_id AS bigint))"), {"p_id": item_id})
            row = res.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail=f"{prefix[:-1].capitalize()} not found")
            # return as mapping/dict — Pydantic Out schema with orm_mode will accept this
            return dict(row._mapping)
        # No fallback: explicit configuration error if stored procedure is missing
        raise HTTPException(status_code=500, detail=f"Stored procedure Get{entity} is required for reads but not available on this database")

    @router.put("/{item_id}", response_model=out_schema)
    def update_item(item_id: int, updates: update_schema, db: Session = Depends(get_db)):
        # For PostgreSQL, if a Save{Entity} stored procedure exists, route update through it
        entity = model.__name__
        if getattr(db.bind.dialect, "name", "") == "postgresql" and _pg_proc_exists(db, f"Save{entity}"):
            # Merge values: only consider fields the client explicitly sent (exclude_unset)
            # If the client sent null explicitly, treat that as intent to set null.
            upd = updates.dict(exclude_unset=True)
            try:
                # Build params where unspecified fields are NULL so the stored proc's COALESCE keeps existing values
                merged = {c.name: upd.get(c.name, None) for c in _proc_columns(model)}
                stmt = build_save_stmt(model, include_id=True)
                params_dict = build_db_params(merged, include_id=True)
                params_dict["p_id"] = item_id
                res = db.execute(stmt, params_dict)
                saved_id = res.scalar()
                db.commit()
                db_obj = db.query(model).filter(model.id == saved_id).first()
                if not db_obj:
                    raise HTTPException(status_code=500, detail=f"Failed to load saved {entity}")
                return db_obj
            except IntegrityError as e:
                db.rollback()
                raise HTTPException(status_code=400, detail=str(e.orig))
            except SQLAlchemyError:
                db.rollback()
                raise HTTPException(status_code=500, detail="Database error during update")
        # Default behavior for other models
        db_obj = db.query(model).filter(model.id == item_id).first()
        if not db_obj:
            raise HTTPException(status_code=404, detail=f"{prefix[:-1].capitalize()} not found")
        for k, v in updates.dict().items():
            if v is not None:
                setattr(db_obj, k, v)
        try:
            db.commit()
            db.refresh(db_obj)
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e.orig))
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Database error during update")
        return db_obj

    # DELETE endpoint removed: not required at this time. Re-enable if needed.
    # @router.delete("/{item_id}", response_model=out_schema)
    # def delete_item(item_id: int, db: Session = Depends(get_db)):
    #     db_obj = db.query(model).filter(model.id == item_id).first()
    #     if not db_obj:
    #         raise HTTPException(status_code=404, detail=f"{prefix[:-1].capitalize()} not found")
    #     # default behavior: soft delete if is_active exists, otherwise delete
    #     try:
    #         if hasattr(db_obj, "is_active"):
    #             setattr(db_obj, "is_active", False)
    #             db.commit()
    #             db.refresh(db_obj)
    #             return db_obj
    #         db.delete(db_obj)
    #         db.commit()
    #         return db_obj
    #     except IntegrityError as e:
    #         db.rollback()
    #         raise HTTPException(status_code=400, detail=str(e.orig))
    #     except SQLAlchemyError:
    #         db.rollback()
    #         raise HTTPException(status_code=500, detail="Database error during delete")

    return router