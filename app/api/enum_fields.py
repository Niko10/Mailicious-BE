from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.enum_fields import create_fields_enum, get_fields_enum, get_fields_enums, get_fields_enum_by_name
from app.schemas.fields_enum import FieldsEnumCreate, FieldsEnum
from app.db.database import get_db
from typing import List

router = APIRouter()

@router.post("/", response_model=FieldsEnum)
def create_field_enum(fields_enum: FieldsEnumCreate, db: Session = Depends(get_db)):
    db_fields_enum = get_fields_enum_by_name(db, name=fields_enum.name)
    if db_fields_enum:
        raise HTTPException(status_code=400, detail="Field already exists")
    return create_fields_enum(db=db, fields_enum=fields_enum)

@router.get("/", response_model=List[FieldsEnum])
def read_fields_enums(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_fields_enums(db=db, skip=skip, limit=limit)

